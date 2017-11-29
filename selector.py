import pickle
from sklearn.externals import joblib
import fileinput
import sys
import os
import sklearn.tree
import sklearn.neighbors.typedefs
import sklearn.tree._utils
import sklearn.svm
import numpy as np
from sklearn.preprocessing import Normalizer

def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))


dir=get_script_path()
clf = joblib.load(os.path.join(dir,"selector_model.pkl"))

norm = Normalizer()
norm = joblib.load(os.path.join(dir,"norm_classes.pkl"))

row=""
for line in fileinput.input():
    row=row+line
row=row.strip()

data1=row.split(" ")
data=[]
data.append(data1)
data = [ [float(s) for s in d] for d in data] 
data = norm.transform(data)

res=clf.predict(data)
if len(res)>0:
	print([res[0].lower()])
else:
	print(res.lower())
