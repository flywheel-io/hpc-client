import re

from .base import Base
from util import defn


class Sge(Base):

	def set_config_defaults(self):

		c = self.config.cast

		if c.command is None:
			c.command = ['qsub', '{{script_path}}']

		if c.command_script_stdin is None:
			c.command_script_stdin = False

		if c.script is None:
			c.script = SCRIPT_TEMPLATE

		if c.script_executable is None:
			c.script_executable = True

	def determine_job_settings(self, job):

		s_debug, s_write = self.determine_singularity_settings(job)

		ram = job.config.get('sge-ram', '4G')
		cpu = job.config.get('sge-cpu', '4-8')

		# Force alphanum, with dashes for cpu range
		ram = re.sub(r'\W+', '', str(ram))
		cpu = re.sub(r'[^a-zA-Z0-9\-]+', '', str(cpu))

		return defn.JobSettings(
			fw_id = str(job.id),

			singularity_debug    = s_debug,
			singularity_writable = s_write,

			ram = ram,
			cpu = cpu,
		)


SCRIPT_TEMPLATE = """
#!/usr/bin/env bash

#$ -j y
#$ -o {{script_log_path}}
#$ -S /bin/bash
#$ -l h_vmem={{job.ram}}
#$ -pe threaded {{job.cpu}}

set -euo pipefail

source "{{cast_path}}/settings/credentials.sh"
cd "{{engine_run_path}}"

set -x
./engine run --single-job {{job.fw_id}}

"""
