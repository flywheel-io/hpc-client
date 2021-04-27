# Choose your integration method

Each time cast is launched, it moves any eligible Flywheel jobs into the HPC scheduler.<br/>
This should be a fairly quick process, and it is likely a good idea to run it fairly frequently.

Depending on your cluster admins, you may want to launch Cast a variety of different ways.<br/>
Check with your admin as to the best option for you.

## Option 1 - cron

If cron is enabled, this is probably the best choice. The below example would run Cast once a minute:

```
*/1 * * * * ~/fw-cast/settings/start-cast.sh
```

For further options, check out [crontab guru](https://crontab.guru/#*/1_*_*_*_*) or your system documentation.

## Option 2 - tmux

If tmux is enabled, this is a very simple way to regularly run cast. Simply launch a named tmux session:

```
tmux new -s cast
```

Then, a simple bash loop can take care of the rest:

```
while true; do ~/fw-cast/settings/start-cast.sh; sleep 60; done
```

By default, `Ctrl+B` then `d` exits. See the [tmux cheatsheet](https://tmuxcheatsheet.com/) or your system documentation for more.

## Option 3 - ssh

If neither option is available, it may be possible to further run Cast on a separate device, and SSH into the cluster when there are jobs available. This would require additional development work to be feasible, and may not work for your cluster, in particular if there are MFA constraints on SSH sessions.

If exploring this option, let us know, we'd be interested to hear about it.
