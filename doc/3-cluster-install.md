# Download

First, connect to your interactive HPC node.

You will need python 3, and how this is done may vary per cluster.<br/>
For example, if your cluster has a `module` system, the command may be something like this:

```
module load python/3
```

Check with your sysadmin or documentation for more information.<br/>
Record any commands required, then check the command is healthy and in your path:

```
python3 --version
```

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

Prepare your cluster-specific files:

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
| `credentials.sh` | Sensitive information |
| `start-cast.sh`  | Bootstrap script      |

Each file has a variety of comments to guide you through the process.<br/>
Work with your collaborating Flywheel employee on these settings, particularly the connection credential.
