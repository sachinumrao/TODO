from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class TODO(db.Model):
    sid = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(300), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % sid


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method=='POST':
        task_content = request.form['content']
        new_task = TODO(content = task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "THERE WAS AN ISSUE IN CREATING NEW TASK!"

    else:
        tasks = TODO.query.order_by(TODO.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:sid>')
def delete(sid):
    task_to_delete = TODO.query.get_or_404(sid)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "THERE WAS AN ERROR IN DELETING THE TASK!" 

@app.route('/update/<int:sid>', methods=['POST', 'GET'])
def update(sid):
    task = TODO.query.get_or_404(sid)
    if request.method=='POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "THERE WAS A PROBLEM IN UPDATING THE TASK!"

    else:
        return render_template('update.html', task=task)

if __name__ == "__main__":
    app.run(debug=True)

