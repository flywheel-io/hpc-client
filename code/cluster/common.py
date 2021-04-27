import copy, os, stat

from jinja2 import Template
import flywheel

from util import defn, frame, net


class Common:
	"""
	The common class holds functionality that you should not override.

	These implementations are subject to change as Flywheel changes.
	"""

	config = None
	log = None
	fw = None

	# Populated on demand
	uid_whitelist = None

	def __init__(self, config, log):
		"""
		Constructor.
		"""

		self.config = config
		self.log    = log
		self.fw     = config.sdk

	def confirm_config_defaults_loaded(self):
		"""
		Confirm that the sub-class has filled out the config settings.
		"""

		optional_keys = [
			'command',
			'command_script_stdin',
			'script',
			'script_executable'
		]

		for key in optional_keys:
			if self.config.cast.dict()[key] is None:
				frame.fatal('config.cast.' + key + ' not populated. Modify your set_config_defaults implementation.')

	def get_jobs(self):
		"""
		Fetch matching jobs to be cast.
		"""

		raw_match = self.config.cast.job_match
		match, search = net.prepare_match_and_search(raw_match)

		# self.log.debug('Match ' + str(match))
		# self.log.debug('search ' + str(search))

		try:
			jobs = []

			cursor = self.fw.jobs.iter_find(filter=search)

			for job in cursor:
				jobs.append(job)

		except flywheel.rest.ApiException as e:
			frame.fw_fatal('Could not fetch FW jobs.', e)

		return jobs

	def determine_singularity_settings(self, job):
		"""
		These config values do not vary by cluster type.

		Keeping this func in Common thus avoids copy-pasting problems.
		"""

		s_debug = job.config.get('singularity-debug',    False)
		s_write = job.config.get('singularity-writable', False)

		if type(s_debug) is not bool:
			self.log.warn('Invalid singularity-debug type on job. Ignoring.')
			s_debug = False

		if type(s_write) is not bool:
			self.log.warn('Invalid singularity-writable type on job. Ignoring.')
			s_write = False

		return s_debug, s_write

	def load_whitelist(self):
		"""
		Load the user whitelist, if enabled.
		"""

		if self.uid_whitelist is None and self.config.cast.group_whitelist:
			self.log.debug('Loading whitelist...')
			t = frame.timer()

			try:
				self.uid_whitelist = net.load_user_id_whitelist(self.fw)
			except flywheel.rest.ApiException as e:
				frame.fw_fatal('Could not fetch HPC whitelist.', e)

			if len(self.uid_whitelist) == 0:
				self.log.warn('HPC whitelist is active, but empty! No jobs will run.')

			ms = str(frame.elapsed_ms(t))
			self.log.debug('Loaded whitelist in ' + ms + ' ms.')

	def reject_whitelist(self, job, job_user):
		"""
		Reject a job due to whitelist mistmatch.
		"""

		# Write a short rejection to stderr
		msg = 'User ' + str(job_user) + ' is not on the HPC whitelist.'
		self.log.warn(msg + ' Dropping job.')

		# Write a long rejection to FW job logs
		msg += '\nOnly white-listed users are allowed to run Gears on the HPC at this time.\nFor more information please contact' + self.config.cast.admin_contact_email

		t = frame.timer()

		try:
			net.add_system_log(self.fw, job.id, msg)
			net.cancel_job(self.fw, job.id)
		except flywheel.rest.ApiException as e:
			frame.fw_fatal('Could not cancel FW job.', e)

		ms = str(frame.elapsed_ms(t))
		self.log.debug('Rejected job ' + job.id + ' in ' + ms + ' ms.')

	def check_whitelist(self, job):
		"""
		Check if a job should run based on the user whitelist, if enabled.

		Return true IFF the job should run.
		"""

		if self.config.cast.group_whitelist:
			self.load_whitelist()

			# Job origins are not guaranteed to exist, and are not always humans
			if job.origin is not None and job.origin.type == 'user':
				job_user = job.origin.id

				if job_user not in self.uid_whitelist:
					self.reject_whitelist(job, job_user)

					return False

		return True

	def run_templating(self, job, values):
		"""
		Generate the script and command templates.
		"""

		self.log.debug("Handling job " + job.id)

		if self.config.cast.show_script_template_values:
			self.log.debug("Template values:\n" + frame.pretty_json(values.dict()))

		# Generate the script
		script_text = Template(self.config.cast.script).render(values)

		if self.config.cast.show_script_template_result:
			self.log.debug("Script contents:\n" + script_text)

		# Write the script to disk
		handle = open(values.script_path, "w")
		handle.write(script_text)
		handle.close()

		if self.config.cast.script_executable:
			st = os.stat(values.script_path)
			os.chmod(values.script_path, st.st_mode | stat.S_IEXEC)

		# Generate the command
		command = copy.deepcopy(self.config.cast.command)
		command = list(map(lambda x: Template(x).render(values), command))

		if self.config.cast.dry_run:
			command.insert(0, 'echo')

		if self.config.cast.show_commnd_template_result:
			self.log.debug("Command to execute:\n" + frame.pretty_json(command))

		return script_text, command

	def report_results(self, start, jobs_launched, jobs_skipped, jobs_rejected):
		"""
		Record total runtime and print useful results.
		"""

		ms = str(frame.elapsed_ms(start))
		msg = ''

		if (jobs_launched + jobs_rejected + jobs_skipped) == 0:
			msg += 'No jobs to handle.'

		else:
			msg = 'Launched ' + str(jobs_launched)

			if jobs_rejected > 0:
				msg += ', rejected ' + str(jobs_rejected)

			if jobs_skipped > 0:
				msg += ', skipped ' + str(jobs_skipped)

			msg += ' jobs.'

		msg += ' Runtime: ' + ms + ' ms.'

		self.log.info(msg)

	def handle_all(self, start):
		"""
		Main handler loop.
		"""

		# Note: some functions are defined in BaseCluster:
		#
		#   determine_job_settings
		#   determine_script_patch
		#   handle_each
		#   set_config_defaults
		#
		# As such, using a Common class directly is invalid.

		# Load any cluster-specific settings
		self.set_config_defaults()
		self.confirm_config_defaults_loaded()

		# Load candidate jobs into memory
		self.log.debug('Looking for jobs to cast...')
		t = frame.timer()
		jobs = self.get_jobs()
		ms = str(frame.elapsed_ms(t))
		count = str(len(jobs))
		self.log.debug('Found ' + count + ' jobs in ' + ms + ' ms.')

		# Track results
		jobs_launched = 0
		jobs_skipped  = 0
		jobs_rejected = 0

		# Invoke cluster-specific logic
		for job in jobs:

			# Cast uses the existence of a script file
			# to determine if a job should be cast.
			script_path = self.determine_script_patch(job)

			if os.path.exists(script_path):
				jobs_skipped += 1
				continue

			if not self.check_whitelist(job):
				jobs_rejected += 1
				continue

			# Collect information
			script_log_path = self.determine_log_patch(job)
			job_settings    = self.determine_job_settings(job)

			# Prepare templating values
			values = defn.ScriptTemplate(
				job             = job_settings,
				script_path     = script_path,
				script_log_path = script_log_path,
				cast_path       = self.config.paths.cast_path,
				engine_run_path = self.config.paths.engine_run_path,
			)

			# Job is fit to cast
			self.handle_each(job, values)
			jobs_launched += 1

		# Finish
		self.report_results(start, jobs_launched, jobs_skipped, jobs_rejected)
