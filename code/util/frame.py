import argparse, datetime, logging, json, os, warnings, yaml

import flywheel, requests

from . import defn

# Suppress (some) FW SDK version spam
logging.getLogger('Flywheel').setLevel(logging.ERROR)
warnings.filterwarnings('ignore')

# Slightly less of an eyesore: log15 strings
logging.addLevelName(logging.CRITICAL, 'CRIT')
logging.addLevelName(logging.ERROR,    'EROR')
logging.addLevelName(logging.WARNING,  'WARN')
logging.addLevelName(logging.INFO,     'INFO')
logging.addLevelName(logging.DEBUG,    'DBUG')

logging.basicConfig(

	format="%(asctime)s %(levelname)s %(message)s",
	datefmt="%m-%d %H:%M:%S",

	handlers=[
		logging.StreamHandler()
	],

	# This level could be configurable.
	level=logging.DEBUG,
)

log = logging


def fatal(*args):
	log.critical(*args)
	log.critical('Exiting.')
	exit(1)


def fw_fatal(msg, e):
	log.critical(msg + ' HTTP error follows:')
	fatal(e)


def pretty_json(obj):
	return json.dumps(obj, indent=4, sort_keys=True)


def ez_path(*args):
	return os.path.abspath(os.path.join(*args))


def timer():
	return datetime.datetime.now()


def elapsed_ms(start):
	elapsed = datetime.datetime.now() - start

	return int(elapsed.total_seconds() * 1000)


def check_paths():
	"""
	Determine and check the various paths needed by the application.
	"""

	p = defn.Paths(
		cast_path       = ez_path(os.getcwd(), ".."                         ),
		yaml_path       = ez_path(os.getcwd(), "..", "settings", "cast.yml" ),
		scripts_path    = ez_path(os.getcwd(), "..", "logs",     "generated"),
		hpc_logs_path   = ez_path(os.getcwd(), "..", "logs",     "queue"    ),
		engine_run_path = ez_path(os.getcwd(), "..", "logs",     "temp"     ),
	)

	for path in [
		p.cast_path, p.yaml_path, p.scripts_path, p.hpc_logs_path, p.engine_run_path
	]:
		if not os.path.exists(path):
			fatal("Path " + path + " is missing; run setup.sh")

	return p


def load_yaml_settings(yaml_path):
	"""
	Parse cast.yml into a pydantic struct.
	"""

	with open(yaml_path) as handler:
		raw_map = yaml.full_load(handler)

	result = defn.ConfigFile.parse_obj(raw_map)

	return result


def load_env_settings():
	"""
	Load sensitive settings that were sourced from credentials.sh
	"""

	return defn.CredentialEnv(
		host        =     os.environ['SCITRAN_RUNTIME_HOST'],
		port        = int(os.environ['SCITRAN_RUNTIME_PORT']),
		credential  =     os.environ['SCITRAN_CORE_DRONE_SECRET'],
	)


def prepare_config():
	paths = check_paths()
	cast = load_yaml_settings(paths.yaml_path).cast
	creds = load_env_settings()

	return defn.Config(
		cast  = cast,
		paths = paths,
		creds = creds,
	)


def create_client(creds):

	log.info('Connecting to FW...')
	t = timer()

	try:
		client = flywheel.drone_login.create_drone_client(
			creds.host, creds.credential, 'python', 'hpc queue', port=creds.port
		)
	except requests.exceptions.ConnectionError as e:
		fw_fatal('Could not connect to FW.', e)

	ms = str(elapsed_ms(t))
	log.debug('Connected in ' + ms + ' ms.')

	return client


def cmd_parser():
	"""
	Build the command-line arg parser.
	"""

	args = argparse.ArgumentParser()

	args.description = 'Cast Flywheel jobs onto --> HPC'

	args.add_argument('--show-match', action='store_true', help='JSON export: job match syntax')
	args.add_argument('--show-config', action='store_true', help='JSON export: all configs')

	return args


def run_cmd():
	"""
	Run the cast command.
	"""

	args   = cmd_parser().parse_args()
	config = prepare_config()

	# Print all settings in JSON
	if args.show_config:
		log.debug("Printing config")

		c = config.dict()
		del c['sdk']
		c['creds']['credential'] = '<omitted>'

		print(pretty_json(c))
		exit(0)

	# Print job match in JSON
	if args.show_match:
		log.debug("Printing gear match")

		print(pretty_json(config.dict()['cast']['job_match']))
		exit(0)

	config.sdk = create_client(config.creds)

	# if args.match:
	# 	gears, match, search = Basics.load_gear_whitelist()
	# 	print(json.dumps(match))
	# else:
	# 	dispatch(args.dry_run, args.cluster)

	return config
