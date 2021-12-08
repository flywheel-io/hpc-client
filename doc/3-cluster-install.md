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


### Folder settings
There are four different directories/folders that one might consider changing.  The <br/>
default folders can be changed by exporting/setting the corresponding environment <br/>
variable in `fw-cast/settings/credentials.sh`


#### [SINGULARITY_WORKDIR](https://sylabs.io/guides/latest/user-guide/appendix.html)
"The working directory to be used for `/tmp`, `/var/tmp` and `$HOME` (if -c or --contain was also used)".<br/>
Instead of mounting to the default directory of the OS--i.e., `tmp` (not to be confused <br/>
with the singularity image's `tmp` directory)--one can mount a drive that can handle intermediate <br/>
files generated when the singularity image is run.

Note: when the singularity container is built and Cast executes singularity, it passes [the flag](https://sylabs.io/guides/latest/user-guide/bind_paths_and_mounts.html?highlight=containall#containall) <br/>
`--containall`, which does not mount a user's `$HOME` directory and additionally contains <br/>
PID, IPC, and environment. One can set this flag when developing and testing singularity <br/> 
images to simulate similar conditions. 

#### [SINGULARITY_CACHEDIR](https://sylabs.io/guides/latest/user-guide/build_env.html#sec-cache)
When a gear is pulled and converted to a sif file, this folder is where both docker and <br/>
sif images are stored. The cache is created at `$HOME/.singularity/cache` by default. </br>


#### Engine folders
The folders `ENGINE_CACHE_DIR` and `ENGINE_TEMP_DIR` are where gear inputs and output files <br/>
will be stored. These should be set to a location that will be able to handle the size of both
<br/> input and output files, and both should be set to the same directory.

#### Log folders
When Cast finds a job from a Flywheel instance, it creates an executable script (`.sh`) for the <br/>
job and its associated log file. The job id will be the in the title of executable and <br/>
its `.txt` log file; they are stored in the directories `fw-cast/logs/generated` and <br/>
`fw-cast/logs/queue`, respectively.  

The executable job script is created from a `SCRIPT_TEMPLATE` (found in `fw-cast/code/cluster`), <br/>
depending on the HPC's job scheduler/cluster type (e.g., slurm). The `start-cast.sh` file <br/>
logs this template in `fw-cast/logs/cast.log`. When troubleshooting an HPC gear, it is <br/>
convenient to use the command `tail -60 fw-cast/logs/cast.log` to print out the last 60 lines from the <br/>
log file, since this can get quite long.
  