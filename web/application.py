from flask import render_template
from flask import Flask

app = Flask(__name__)



items = []
for i in range(1, 11):
  i = str(i)
  an_item = dict(src = "BUD", dst = "ACE", date = "2017-08-02", day = "Tuesday", price = "20000")
  items.append(an_item)




@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
		    return render_template('hello.html', name=name, items=items)
