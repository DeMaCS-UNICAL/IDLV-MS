#!/usr/bin/python3
#Given a folder with ecoding, instances and list of instances run IDLV for each instances and
#    run all encodings and save the running time

import sys
import os
import re


PID = os.getpid()

def getLast(s):
    if "/" in s:
        return s.split("/")[-1]
    return s


def runSystem(system, system_stat, encoding, instances, errorfile):
    print("Run %s on %s" % (system, instances))
    os.system("./%s %s %s | ./%s /dev/null > %s" % (system, encoding, instances, system_stat, errorfile))
    result = ""
    file = open(errorfile, "r")
    for line in file:
        result = line
        break
    result = result.replace("\t", ";")
    result = result.rstrip()
    file.close()
#    os.system("rm %s" % errorfile)
    return result


def main(system, system_stats, directory, outfile, instances_file):
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
    dname =directory
    if directory[-1] == "/":
        dname = directory[:-1]
    for i in instances:
        err_file = outfile+"_err_time_"+getLast(i)+"_"+str(PID)
        stats = runSystem(system, system_stats, e, i, err_file)
        file.write(getLast(dname)+";"+getLast(i)+";"+stats+"\n")
    file.close()

if __name__ == "__main__":
    system = sys.argv[1]
    system_stats = sys.argv[2]
    folder = sys.argv[3]
    outfile = sys.argv[4]
    instances = sys.argv[5]
    if folder[-1] != '/':
        folder += '/'

    main(system, system_stats, folder, outfile, instances)
