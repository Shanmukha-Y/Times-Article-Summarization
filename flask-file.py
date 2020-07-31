
from flask import Flask, render_template, request


app = Flask(__name__)

from transformers import pipeline
#from transformers import PreTrainedModel
#from transformers import  TFT5Model, TFBertModel
import requests
import pprint
import time

summarizer_bart = pipeline("summarization")
summarizer_t5 = pipeline("summarization", model="t5-base")

class models:
   
    def __init__(self, text, length):
        self.length = length
        self.text = text


    def bart(self):
        return(list(summarizer_bart(self.text, min_length=self.length, max_length=self.length+10)[0].values())[0])

    def t5(self):
        return(list(summarizer_t5(self.text, min_length=self.length, max_length=self.length+10)[0].values())[0])

@app.route('/')
def student():
   return render_template('student.html')

@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form
      text = request.form['news entered']
      length = request.form['size']
      model = request.form['model']
      model_ob = models(text, int(length))
      if model=='bart':
          out = model_ob.bart()
      else:
          out = model_ob.t5()
      
      print(out)
      return render_template("result.html",result = result,out=out)

if __name__ == '__main__':
   app.run(debug = True)
