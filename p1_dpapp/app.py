from flask import *
import pickle

app=Flask(__name__)
@app.route("/",methods=["GET","POST"])
def home():
	if request.method=="POST":
		f=open("db.model","rb")
		model=pickle.load(f)
		f.close()
		fs=float(request.form["fs"])
		fu=request.form["fu"]
		if fu=="yes":
			d=[[fs,0,1]]
		else:
			d=[[fs,1,0]]
		result=model.predict(d)
		return render_template("home.html",m=result[0])
	else:
		return render_template("home.html")
if __name__ =="__main__":
	app.run(debug=True,use_reloader=True)