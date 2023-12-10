from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' # 3 slashes relative (proj loc) path 4 - absolute (exact loc)
db = SQLAlchemy(app)


class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']  # z utworzonego form w index.html
        new_task = ToDo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except Exception as exc:
            return 'There was issue adding your task {}'.format(exc)
    else:
        tasks = ToDo.query.order_by(ToDo.date_created).all()  # first() etc
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = ToDo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except Exception as exc:
        return f'Error: {exc}'


@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    task = ToDo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except Exception as exc:
            return f'Error: {exc}'
    else:
        return render_template('update.html', task=task)


if __name__ == '__main__':
    app.run(debug=True)


# console python3
# from app import db, app
# app.app_context().push()
#db.create_all()
#