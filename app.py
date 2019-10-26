import pandas as pd
from flask import Flask, render_template, url_for, request
from flask_bootstrap import Bootstrap
from googletrans import Translator
from grammarbot import GrammarBotClient
# from similarity import model_similarity

app = Flask(__name__)
Bootstrap(app)

#function to modify string with stylen transfer according  to the personality

translator=Translator()
checker = GrammarBotClient(api_key='KS9C5N3Y')
def paraphrased(in_text):
    phrased = []
    for i in ['ko', 'ja', 'el', 'fr', 'tl', 'ar', 'ht','af', 'sq', 'am']:
        par_text = translator.translate(in_text, dest=i).text
        phrased.append(translator.translate(par_text, dest='en').text.capitalize())
    t = [i for i in phrased if i.lower() != in_text.lower()]
    return "No possible phrases" if not list(set(t)) else list(set(t))
def grammar_check(alist):
    final_list = []
    #print(alist)
    for i in alist:
        x = [j.corrections for j in checker.check(i).matches]
        if len(x) < 1:
            final_list.append(i)
        else:
            final_list.append(x)
    return final_list
# add a rule for the index page.
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_data', methods=['POST'])
def get_data():
    if request.method == 'POST':
        text = request.form['nlg']
        trans = paraphrased(text)
        altertext = grammar_check(trans)
    return render_template('engine.html',your_list=altertext,prediction=[text,altertext,len(altertext)])

# run the app.
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=80)