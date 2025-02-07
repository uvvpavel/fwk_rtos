#!/usr/bin/env python3
# Copyright (c) 2023, XMOS Ltd, All rights reserved
# This Software is subject to the terms of the XMOS Public Licence: Version 1.

import getpass
import struct
import argparse
import os

s = bytearray()

parser = argparse.ArgumentParser()

parser.add_argument(
    "--ssid",
    help="network SSID",
)
parser.add_argument(
    "--password",
    help="network password",
)
parser.add_argument(
    "--security",
    help="security",
)

args = parser.parse_args()

if not (args.ssid):
    ssid = input("Enter the WiFi network SSID: ")
else:
    ssid = args.ssid

if not (args.password):
    password = getpass.getpass("Enter the WiFi network password: ")
else:
    password = args.password

if not (args.security):
    security = eval(input("Enter the security (0=open, 1=WEP, 2=WPA): "))
else:
    security = eval(args.security)

bssid = b"\x00\x00\x00\x00\x00\x00"

s += struct.pack(
    "<32sxB6s32sxBxxi",
    bytearray(ssid, "ascii"),
    min(len(ssid), 32),
    bssid,
    bytearray(password, "ascii"),
    min(len(password), 32),
    security,
)

file = open(f"{os.path.realpath(os.path.dirname(__file__))}/networks.dat", "wb")
file.write(s)
file.close()

