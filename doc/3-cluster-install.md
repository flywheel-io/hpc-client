## Set up your environment

### Install python

First, connect to your interactive HPC node.

You will need python 3, and how this is done may vary per cluster.<br/>
For example, if your cluster has a `module` system, the command may be something like this:

```
module load python/3
```

You may also directly be able to install python with the following if you have root privileges:

```
sudo apt-get update
sudo apt-get install python3.8
```

Check with your sysadmin or documentation for more information.<br/>
Record any commands required, then check the command is healthy and in your path:

```
python3 --version
```

#### Symlink python to python3

To prevent calling python2 instead of python3, it is recommended that a symlink be created for the command 
`python` so that any calls default to `python3`. To do so, simply install the package 
`python-is-python3` with the following:

```
sudo apt install python-is-python3
```

### Clone the Cast repo and set up a virtual environment

Add pipenv, which isolates our script dependencies, to your homedir:

```
python -m pip install pipenv
```

Snag a copy of this repository:

```
# If you are tracking your settings as shown previously,
# add the following to your HPC user's ~/ssh/config:
Host github.com
  IdentityFile ~/fw-cast-st-jude-key

git clone <your-github-location> fw-cast

cd fw-cast
```

Setup the pipenv for the fw-cast project:
```
cd code
python -m pipenv install
cd ../
```

### Run the `setup` script
Prepare your cluster-specific files by running the setup script. You may have to 
prepend `bash` or `sh`.

```
./process/setup.sh
```

Important - in a shared environment, protect your credentials:

```
chmod 0600 ./settings/credentials.sh
```

## Configure

A new `settings` folder was just generated.<br/>
You need to edit each of these files in turn to configure it for your cluster:

| Filename         | Purpose               |
| -----------------| ----------------------|
| `cast.yml`       | High-level settings   |
| `credentials.sh` | Sensitive information and Singularity environment config options |
| `start-cast.sh`  | Bootstrap script      |

Each file has a variety of comments to guide you through the process.<br/>
Work with your collaborating Flywheel employee on these settings, particularly the <br/>
connection credential (i.e., `SCITRAN_CORE_DRONE_SECRET` in `credentials.sh`).
