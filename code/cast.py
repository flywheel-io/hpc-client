#!/usr/bin/env python3

# Cast.py - dispatch FW jobs to HPC

import cluster
from util import frame

import os

if __name__ == '__main__':

	print("CWD", os.getcwd())

	try:

		start  = frame.timer()
		log    = frame.log
		config = frame.run_cmd()

		cluster.run_cast(start, config, log)

	except KeyboardInterrupt:
		frame.log.error('Aborted by Ctrl-C')
