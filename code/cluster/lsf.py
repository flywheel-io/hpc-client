import re

from .base import Base
from util import defn


class Lsf(Base):

	def set_config_defaults(self):

		c = self.config.cast

		if c.command is None:
			c.command = [
				'bsub',
				'-P', 'flywheel',
				'-J', 'fw-{{job.fw_id}}',
				'-oo', '{{script_log_path}}',
				'-eo', '{{script_log_path}}'
			]

		# Unlike qsub, bsub does not like being passed the file as a param.
		# It will superficially appear to work, but actually drop some of its parameters.
		if c.command_script_stdin is None:
			c.command_script_stdin = True

		if c.script is None:
			c.script = SCRIPT_TEMPLATE

		if c.script_executable is None:
			c.script_executable = False

	def determine_job_settings(self, job):

		s_debug, s_write = self.determine_singularity_settings(job)

		ram = job.config.get('lsf-ram', 'rusage[mem=1000]')
		cpu = job.config.get('lsf-cpu', '1')

		# Force alphanum, with some extra chars for ram syntax
		ram = re.sub(r'[^a-zA-Z0-9\[\]\=]+', '', str(ram))
		cpu = re.sub(r'\W+', '', str(cpu))

		return defn.JobSettings(
			fw_id = str(job.id),

			singularity_debug    = s_debug,
			singularity_writable = s_write,

			ram = ram,
			cpu = cpu,
		)


SCRIPT_TEMPLATE = """
#!/bin/bash

#BSUB -P flywheel
#BSUB -J fw-{{job.fw_id}}
#BSUB -n {{job.cpu}}
#BSUB -R {{job.ram}}
#BSUB -oo {{script_log_path}}
#BSUB -eo {{script_log_path}}

set -euo pipefail

source "{{cast_path}}/settings/credentials.sh"
cd "{{engine_run_path}}"

set -x
./engine run --single-job {{job.fw_id}}

"""
