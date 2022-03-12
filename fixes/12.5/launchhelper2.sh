#!/usr/bin/env sh

if [ "$(cat /proc/sys/abi/vsyscall32)" -eq 0 ]; then
    exit 0
fi

pkexec sh -c 'sysctl -w abi.vsyscall32=0'

python launchhelper2.py