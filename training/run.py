#!/usr/bin/python3
#Given a folder with ecoding, instances and list of instances run IDLV for each instances and
#    run all encodings and save the running time

import sys
import os
import multiprocessing as mp

from datetime import datetime

PROCESS = 2

PROBLEMS_DIR="problems"
SYSTEMS_DIR="systems"
IDLV = "../idlv-lpopt-portable/idlv"
STATS = "../freader/NumericOut"
INSTANCES = "all"

OUT_SYSTEM_NAME="result_"

PID = os.getpid()

import runner
TO = "TIMEOUT"

def getSystemRun(s):
    return SYSTEMS_DIR+"/"+s+"/run"

def runProblem(systems, problem, out_dir):
    for s in systems:
        outfile = out_dir+"/"+OUT_SYSTEM_NAME+s
        run = "./%s %s %s %s %s" % ("runner.py", getSystemRun(s), problem, outfile, INSTANCES)
        print(run)
        os.system(run)

def processProblem(p):
    runProblem(p[2], p[0], p[1])

now = datetime.utcnow().strftime("%Y%m%d%H%M%S")
root_logdir = "training-results"
logdir = "{}/run-{}-{}".format(root_logdir, now, PID)
os.makedirs(logdir)
problems = [f for f in os.listdir(PROBLEMS_DIR)]

print("GENERATE STATS")
for p in problems:
    dir = logdir+"/" + p
    os.makedirs(dir)
    outfile = dir+"/stats"
    run = "./%s %s %s %s %s all" % ("genstats.py", IDLV, STATS, PROBLEMS_DIR+"/"+p, outfile)
    print(run)
    os.system(run)

print("GENERATE TIME")
systems = [f for f in os.listdir(SYSTEMS_DIR)]


problems_dir_systems = [(PROBLEMS_DIR+"/"+p,logdir+"/"+p, systems) for p in problems]
pool = mp.Pool(processes=PROCESS)
pool.map(processProblem, problems_dir_systems)

problems_result = {}

for pds in problems_dir_systems:
    out_problem = pds[1]
    inst_result = {}
    for s in systems:
        resfile = open(out_problem+"/"+OUT_SYSTEM_NAME+s, "r")
        for l in resfile:
            l = l.rstrip()
            l_split = l.split(";")
            inst = l_split[1]
            time = l_split[2]
            
            if inst in inst_result:
                inst_result[inst].append((s, time))
            else:
                r = [(s, time)]
                inst_result[inst] = r
        resfile.close()
    problems_result[out_problem] = inst_result

for p in problems_result:
    for i in problems_result[p]:
        res_time = problems_result[p][i]
        best = "NONE"
        best_time = sys.maxsize
        for sr in res_time:
            if "TIMEOUT" not in sr[1] and float(sr[1]) < best_time:
                best_time = float(sr[1])
                best = sr[0]
        problems_result[p][i] = [best]


resfile = open(logdir+"/result","w")
for p in problems_result:
    stats = open(p+"/stats","r")
    for l in stats:
        l = l.rstrip()
        i = l.split(";")[1]
        if i not in problems_result[p]:
            continue
        system = problems_result[p][i]
        if len(system) < 1:
            continue
        l = l+";"+system[0]
        resfile.write(l+"\n")
    stats.close()
resfile.close()
