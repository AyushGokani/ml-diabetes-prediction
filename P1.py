import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import pickle

data=pd.read_csv("diabetes_m2023.csv")
print(data)

print(data.isnull().sum())

features=data[["FS","FU"]]
target=data["Diabetes"]

nfeatures=pd.get_dummies(features)
print(features)
print(nfeatures)

x_train,x_test,y_train,y_test=train_test_split(nfeatures,target)

model=LogisticRegression()
model.fit(x_train,y_train)

cr=classification_report(y_test,model.predict(x_test))
print(cr)

f=open("db.model","wb")
pickle.dump(model,f)
f.close()


