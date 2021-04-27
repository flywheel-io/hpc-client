# Tracking your changes

When using Cast in your environment, you may have to modify settings or code.<br/>
Keeping this tracked in version control, outside the HPC, will save a lot of headaches later.

Because this repository is open-source, the normal "fork" button won't do the job. <br/>
This is very important if you choose to version your credentials, which is recommended.

1. [Create a new github repository](https://github.com/new). Set it to private.

2. Click "Settings" -> "Manage access" -> add any desired collaborators.<br/>
In particular, whichever Flywheel staff member(s) you may be working with.

3. Switch to the "Deploy keys" section, then generate a new ssh key on the terminal. Leave the passphrase blank:

```
ssh-keygen -t ed25519 -C fw-cast-deploy-key -f ./fw-cast-deploy-key

cat fw-cast-deploy-key.pub
```

4. Click "Add deploy key", and paste the public key's contents into the page. You may want to tick the box to give it write access also.

5. Copy this key to your HPC for use later:

```
scp fw-cast-deploy-key <your-hpc-host>:
```

6. Move Flywheel Cast to your private copy:

```
git clone https://github.com/flywheel-io/fw-cast

cd fw-cast

git remote add private <your-github-location>

git push private --all
```

7. If you are tracking your settings (recommended), remove `/settings` from `.gitignore`, then add your files and make a commit:

```
git add ./settings

git commit -m "Track setting files"

git push private
```
