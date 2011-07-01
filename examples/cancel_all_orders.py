#!/usr/bin/env python

"""Cancel all outstanding Sell orders."""

robot = pygox.RobotConnection().cancelAllOrders()


