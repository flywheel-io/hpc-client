# Flywheel HPC Client

The HPC Client is a self-service solution that allows Flywheel jobs and gears to run on a High Performance Computing environment. Use on-premise hardware that's already available for highly-concurrent scientific workloads!

**Project Status:** Prototype. You may run into some rough edges, and will need to work in tandem with Flywheel staff.

## Architecture

![hpc-client-architecture 20210726](https://user-images.githubusercontent.com/75435671/127048966-af0582f7-10dc-451c-b955-4d5ab50eaf08.png)

## HPC types

The client, also called Cast, supports several queue mechanisms out of the box:

| Common name              | Code name |
| -------------------------| ----------|
| IBM spectrum LSF         | `lsf`     |
| Oracle / Sun Grid Engine | `sge`     |
| Slurm                    | `slurm`   |

If your site uses one of these, it may well just need a config file to get running.<br/>
Otherwise, some light python development will be required.

## Getting started

1. Before using Cast, you need to decide how it will run on your cluster.<br/>
[Choose an integration method](doc/1-choose-an-integration-method.md) and keep it in mind for later.

2. It is strongly recommended that you [make a private github repo](doc/2-tracking-changes-privately.md) to track your changes.<br/>
This will make Cast much easier to manage.

3. Perform the [initial cluster setup](doc/3-cluster-install.md).

4. If your queue type is not in the above table, or is sufficiently different, review the guide for [adding a queue type](doc/4-development-guide.md).

5. Collaborate with Flywheel staff to install an Engine binary and run your first HPC job tests.

6. Complete the integration method you chose in step one.<br/>
Confirm Cast is running regularly by monitoring `logs/cast.log` and the Flywheel user interface.

7. Enjoy!
