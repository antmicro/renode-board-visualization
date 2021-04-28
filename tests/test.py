#!/usr/bin/env python3

from pyrenode import *

import os
os.chdir("../")

connect_renode()

def cli_or_die(text):
    ret = expect_cli(text)
    assert ret.match is not None, "Got: " + ret.text + " instead of: " + text

PORT = 8000

tell_renode("i @script.resc")
cli_or_die("Starting emulation...\n")
cli_or_die("(machine-0)")

tell_renode(f"serveVisualization {PORT}")
cli_or_die("Serving interactive")

import subprocess
os.chdir("tests/")
p = subprocess.call('./cleanup-and-grab-screencast.sh', shell=True)

