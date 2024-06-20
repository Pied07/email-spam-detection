from flask import Flask, render_template, request
import joblib
import pandas as pd

app = Flask(__name__)
trans = joblib.load('Model_ml.pkl')

data = []

prediction=[]

err_msg = "Type a mail or enter a csv file first to check for Spam!!!"

@app.route('/')

def home():
    return render_template('index.html')


@app.route('/predict',methods=['POST'])
def predict():	

	if request.method == 'POST':
		message = request.form['message']
		if message == '':
			dataf = []
			predictionf = []
			file = request.form['file']
			
			try:
				dataf = pd.read_csv(file)
				data_predict = [dataf.Message]
				temp = []
				for i in dataf.Message:
					temp.append(i)
			except:
				return render_template('index.html', err_msg = err_msg)
			for item in data_predict:
				filePredict = trans.predict(item)
				predictionf.append(filePredict)

			return render_template('index.html', file_content=temp, file_Values = zip(temp,filePredict))
			
		temp = [message]
		my_prediction = trans.predict(temp)
		prediction.append(my_prediction)
		data.append(message)	
		
	return render_template('index.html', message=message, printing_Values = zip(data,prediction))
	

if __name__ =='__main__':
    app.run(debug=True)