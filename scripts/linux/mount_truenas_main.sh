#!/bin/bash
mount -t cifs -o rw,vers=3.0,credentials=/root/.smbcredentials //192.168.1.200/main_S24 /mnt/truenas_main