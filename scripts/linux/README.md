# Linux Scripts

Index:
- [Mount TrueNAS Main Share](#mount-truenas-main-share)
- [Folders for Files](#folders-for-files)

## Mount TrueNAS Main Share

Mounts `//192.168.1.200/main` to `/mnt/truenas_main` over SMB.

- Script file: `mount_truenas_admin.sh`
- Parameters: `none`
- Requirements:
    1. Credentials file in `/root/.smbcredentials`
    1. Mount folder created at `/mnt/truenas_main`
    1. SMB share on `//192.168.1.200/main`

## Folders for Files

Creates an individual folder for each file in the provided path and moves it into that folder. The folder will have the same name as the file, without the extension. Useful to structure loose media into separate folders, as typically required by media managers.

- Script file: `folders_for_files.sh`
- Parameters:
    1. Path to folder with target files
- Requirements:
    1. Write access to the provided folder