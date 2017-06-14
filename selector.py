import pickle
from sklearn.externals import joblib
import fileinput
import sys
import os
import sklearn.tree
import sklearn.neighbors.typedefs
import sklearn.tree._utils

def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))


dir=get_script_path()
clf = joblib.load(os.path.join(dir,"selector_model.pkl"))

row=""
for line in fileinput.input():
    row=row+line
row=row.strip()

data1=row.split(" ")
data=[]
data.append(data1)

res=clf.predict(data)
print(res)
