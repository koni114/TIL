import os
os.getcwd()
data = ""

f = open("/dev/urandom", "r")
data += f.read(10000000)

