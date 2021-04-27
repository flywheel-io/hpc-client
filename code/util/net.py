import copy

import flywheel


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


def prepare_match_and_search(raw_match):
	"""
	Given a raw match object from cast.yml,
	prepare an actual match & search syntax for use with the API.

	This is not yet updated to handle a full job match.
	"""

	match = copy.deepcopy(raw_match)

	# Job match syntax; capabilities are not configurable
	match['capabilities'] = [
		'networking',
		'singularity',
	]

	gears = match['whitelist']['gear-name']

	# Queue regex search syntax
	# search = 'state=running,gear_info.name=~' + '|'.join(gears)
	search = 'state=pending,gear_info.name=~' + '|'.join(gears)

	return match, search


def load_user_id_whitelist(fw):
	"""
	Load user IDs from a FW-group-defined whitelist.
	"""

	# Group name is intentionally not configurable.
	group_name  = 'hpc-whitelist'
	group_perms = fw.get_group(group_name)['permissions']

	return list(map(lambda x: x.id, group_perms))
