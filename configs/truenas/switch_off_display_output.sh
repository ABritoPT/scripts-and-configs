#!/bin/bash

# source: https://forums.truenas.com/t/is-there-a-way-to-turn-off-the-screen-on-truenas-scale/4212/7 

midclt call system.advanced.update '{ "kernel_extra_options": "consoleblank=60" }'