import pickle
import warnings
warnings.filterwarnings("ignore")

f=open("db.model","rb")
model=pickle.load(f)
f.close()

fs=float(input("enter fasting sugar "))
fu=input("frequent urination y/n ")
if fu=="y":
	d=[[fs,0,1]]
else:
	d=[[fs,1,0]]
result=model.predict(d)
print(result[0])