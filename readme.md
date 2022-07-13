# Flywheel HPC Client

The HPC Client is a self-service solution that allows Flywheel jobs and gears to run on a High Performance Computing environment. Use on-premise hardware that's already available for highly-concurrent scientific workloads!

**Project Status:** Prototype. You may run into some rough edges, and will need to work in tandem with Flywheel staff.

[![Build Status](https://github.com/flywheel-io/hpc-client/actions/workflows/build.yml/badge.svg)](https://github.com/flywheel-io/hpc-client/actions)

## Architecture

![hpc-client-architecture 20210726](https://user-images.githubusercontent.com/75435671/127048966-af0582f7-10dc-451c-b955-4d5ab50eaf08.png)

## HPC types

The client, also called Cast, can support several queue mechanisms out of the box. Flywheel, however, currently only
provides support for Slurm. If you require assistance with other schedulers, contact Flywheel.

| Common name              | Code name |
| -------------------------| ----------|
| IBM spectrum LSF         | `lsf`     |
| Oracle / Sun Grid Engine | `sge`     |
| Slurm                    | `slurm`   |

If your site uses one of these, it may well just need a config file to get running.<br/>
Otherwise, some light python development will be required.

## Minimum requirements
Reference [this article](https://docs.flywheel.io/hc/en-us/articles/7563372636563) for 
the minimum software and computing requirements of the system where the HPC Client 
will be installed.

## Getting started

1. Before using Cast, you need to decide how it will run on your cluster.<br/>
[Choose an integration method](doc/1-choose-an-integration-method.md) and keep it in mind for later.
   This sets how frequently Cast with look for, pull, and queue hpc jobs to your HPC from your Flywheel site.

2. It is strongly recommended that you [make a private GitHub repo](doc/2-tracking-changes-privately.md) to track your changes.<br/>
This will make Cast much easier to manage.

3. Perform the [initial cluster setup](doc/3-cluster-install.md). If you are unfamiliar with <br/>
singularity, it is recommended that you read--at a minimum--SingularityCE's [introduction](https://sylabs.io/guides/latest/user-guide/introduction.html) <br/>
   and [quick start](https://sylabs.io/guides/latest/user-guide/quick_start.html) guides.
   
4. [Create an authorization token](doc/Flywheel%20HPC%20Client%20-%20Singularity%20api%20key%20configuration.pdf) 
   so Singularity and Flywheel can work with each other.

5. If your queue type is not in the above table, or is sufficiently different, review the guide for [adding a queue type](doc/4-development-guide.md).

6. Collaborate with Flywheel staff to [install an Engine binaries](doc/Flywheel%20HPC%20Client%20-%20engine%20configuration.pdf).
   They will also configure the hold engine on your Flywheel site
   to ensure that other engines do not pick up gear jobs that are tagged with "hpc".

7. Complete the integration method you chose in step one.<br/>
   Confirm Cast is running regularly by monitoring `logs/cast.log` and the Flywheel user interface.
   
8. Test and run your first HPC job tests in collaboration with Flywheel. It is recommended
   that you test with MRIQC (non-BIDS version), a gear that's available from Flywheel's [Gear Exchange](https://flywheel.io/gear-exchange/).
   Note: as of 11 May 2022, Flywheel will have to change the rootfs-url (location of where the Docker image resides) for
   any gears installed from the Gear Exchange. For more about how Cast uses a rootfs-url, see Background/Motivation
   of [this article](https://docs.flywheel.io/hc/en-us/articles/4607520806547-Using-pre-built-singularity-images-sif-with-your-HPC).

8. Enjoy!
