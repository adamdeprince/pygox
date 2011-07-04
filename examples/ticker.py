#!/usr/bin/env python 

"""A demonstation "Read Time" feed with pygox."""

import pygox
import sys

robo = pygox.RobotConnection()
pretick = ""


print("WARNING: This is very demanding of MtGox's bandwidth."
      "  This is a demonstration ONLY.")

for tick in robo.ticker(delay=1, history = {}):
    if tick:
        sys.stdout.write("%s%s\n" % (pretick, tick,))
        pretick = ""
    else:
        pretick = "\n"
        sys.stdout.write(".")
        sys.stdout.flush()

