from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime
import requests
from newsapi import NewsApiClient

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.String(200), nullable = False)
    date_creted = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return f'Task: {self.id}'


# with app.app_context():
#     db.create_all()

@app.route('/', methods=['POST','GET'])
def index():
    if request.method == "POST":
        task_content = request.form['content']
        new_task = Todo(text = task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'problem'
    else:
        # newsapi = NewsApiClient(api_key='5c2a5bc7fbfe41b299b89c97e1ad58c4')
        # top_headlines = newsapi.get_top_headlines(q='bitcoin',
        #                                   category='business',
        #                                   language='en',
        #                                   country='us')

        # print(top_headlines)

        # url = ('https://newsapi.org/v2/everything?'
        #     'q=Apple&'
        #     'from=2023-06-23&'
        #     'sortBy=popularity&'
        #     'apiKey=5c2a5bc7fbfe41b299b89c97e1ad58c4')

        # r = requests.get(url)
        # import pymongo
        # from pymongo import InsertOne
        # myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        # mydb = myclient["test_database"]
        # print("here",mydb)
        # col = mydb.create_collection( "mycollection")
        # mydb.mycol.insert_one({"name":"omer"})
        # print(r.content)
        tasks = Todo.query.order_by(Todo.date_creted).all()
        return render_template("index.html", tasks = tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        print('here')
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'problem delete'

@app.route('/update/<int:id>')
def update(id):
    task = Todo.query.get_or_404(id)
    
    if request.method == 'POST':
        task.text = request.form['content']
        
        try:
            db.session.commit()
            return redirect('/ ')
        except:
            return 'problem update'
    else:
        return render_template('update.html', task=task)

if __name__ == "__main__":
    app.run(debug = True)