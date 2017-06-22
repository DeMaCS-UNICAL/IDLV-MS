#!/usr/bin/python3
#Given a folder with ecoding, instances and list of instances run IDLV for each instances and
#    run all encodings and save the running time

import sys
import os
import re


PID = os.getpid()

TIMEOUT = 600
MEMOUT = 15 * 1024 * 1024


def getLast(s):
    if "/" in s:
        return s.split("/")[-1]
    return s


def runSystem(system, encoding, instances, errorfile):
    os.system("perl timeout -t %d -m %d ./%s %s %s > /dev/null 2> %s" % (TIMEOUT, MEMOUT, system, encoding, instances, errorfile))
    time = "TIMEOUT"
    file = open(errorfile, "r")
    for line in file:
        mo = re.search(r'FINISHED CPU (.+?) MEM', line)
        if mo:
            time = float(mo.group(1))
            break
    file.close()
#    os.system("rm %s" % errorfile)
    return time


def main(system, directory, outfile, instances_file):
    print("Run %s" % directory)
    resfile = "%s" % (outfile)
    os.system("rm -rf %s" % resfile)
    file = open(resfile, "w")
    encodings = []
    instances = []
    for f in os.listdir(directory):
        if f.startswith("encoding."):
            encodings.append(directory+"/"+f)

    if instances_file == "all":
        for f in os.listdir(directory):
            if directory+"/"+f not in encodings:
                instances.append(directory+"/"+f)
    else:
        fileI = open(directory+"/"+instances_file, "r")
        for line in fileI:
            line = line.rstrip()
            instances.append(directory+"/"+line)
        fileI.close()

    
    e = encodings[0]
    dname = directory
    if directory[-1] == "/":
        dname = directory[:-1]
    for i in instances:
        err_file = outfile+"_err_time_"+getLast(i)+"_"+str(PID)
        time = runSystem(system, e, i,err_file)
        file.write(getLast(dname)+";"+getLast(i)+";"+str(time)+"\n")
    file.close()

if __name__ == "__main__":
    system = sys.argv[1]
    folder = sys.argv[2]
    outfile = sys.argv[3]
    instances = sys.argv[4]
    if folder[-1] != '/':
        folder += '/'

    main(system, folder, outfile, instances)
