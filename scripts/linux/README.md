# Linux Scripts

## Mount TrueNAS Main Share

Mounts `//192.168.1.200/main` to `/mnt/truenas_main` over SMB.

- Script file: `mount_truenas_admin.sh`
- Parameters: `none`
- Requirements:
    1. Credentials file in `/root/.smbcredentials`
    1. Mount folder created at `/mnt/truenas_main`
    1. SMB share on `//192.168.1.200/main`