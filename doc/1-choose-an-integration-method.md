# Choose your integration method

Each time cast is launched, it moves any eligible Flywheel jobs into the HPC scheduler.<br/>
This should be a fairly quick process, and it is likely a good idea to run it fairly frequently.

Depending on your cluster admins, you may want to launch Cast a variety of different ways.<br/>
Check with your admin as to the best option for you.

## Option 1 - cron

If cron is enabled, this is probably the best choice. The below example would run Cast once a minute.

1. Create a new crontab file. Note: you may have to prepend `sudo` if there are any permission issues.

```
crontab -e
```

2. Select a text editor if prompted.

```
Select an editor.  To change later, run 'select-editor'.
  1. /bin/nano        <---- easiest
  2. /usr/bin/vim.basic
  3. /usr/bin/vim.tiny
  4. /bin/ed

Choose 1-4 [1]:
```

3. Enter the task for cron to run (at bottom of the file).  

```
*/1 * * * * ~/fw-cast/settings/start-cast.sh
```

If the script does not run, try using `bash` or `sh` in the command:

```
*/1 * * * * bash ~/fw-cast/settings/start-cast.sh
```

4. Save and exit. If you're using nano, save the file with `control + O`, and hit enter <br/>
   when prompted about the file name and location. Exit with `control + X`
   
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
