import flywheel

from . import frame


def add_system_log(fw, job_id, msg):
	"""
	Add a system log message to a FW job log.
	"""

	if not msg.endswith('\n'):
		msg = msg + '\n'

	return fw.add_job_logs(job_id, [{'fd': -1, 'msg': msg + '\n'}])


def cancel_job(fw, job_id):
	"""
	Cancel a FW job.
	"""

	fw.modify_job(job_id, flywheel.Job(state='cancelled'))


def prepare_search(cast_config):
	"""
	Prepare search syntax for use with the API.
	"""

	search = ''

	use_hpc_tag = cast_config.cast_on_tag
	gears       = cast_config.cast_gear_whitelist

	if cast_config.use_hold_engine:
		search += 'state=running'
	else:
		search += 'state=pending'

	# Check for invalid config
	if use_hpc_tag and len(gears) > 0:
		frame.fatal('Invalid configuration - cast_on_tag and cast_gear_whitelist are mutually exclusive')

	if not use_hpc_tag and len(gears) <= 0:
		frame.fatal('Invalid configuration - one of cast_on_tag or cast_gear_whitelist must be in use')

	# Search syntax ands conditions together
	if use_hpc_tag:
		search += ",tags=hpc"

	if len(gears) > 0:
		search += ',gear_info.name=~' + '|'.join(gears)

	return search


def load_user_id_whitelist(fw):
	"""
	Load user IDs from a FW-group-defined whitelist.
	"""

	# Group name is intentionally not configurable.
	group_name  = 'hpc-whitelist'
	group_perms = fw.get_group(group_name)['permissions']

	return list(map(lambda x: x.id, group_perms))
