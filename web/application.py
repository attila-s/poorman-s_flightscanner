from flask import render_template
from flask import Flask
from momentjs import momentjs
from datetime import datetime
from flask import request


app = Flask(__name__)

app.jinja_env.globals['momentjs'] = momentjs

items = []
for i in range(1, 11):
  i = str(i)
  an_item = dict(src = "BUD", dst = "ACE", date = "2017-08-02", day = "Tuesday", price = "20000")
  items.append(an_item)

@app.route('/handle_data', methods=['POST'])
def handle_data():
  projectpath = request.form['projectFilepath']
  print projectpath#your code
  return ""

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', date=datetime.now(), name=name, items=items)
