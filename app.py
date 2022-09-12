from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
db = SQLAlchemy(app)

class Todo(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	note = db.Column(db.String(80), unique=True, nullable=False)

	def __repr__(self):
		return "<Todo " + self.note + ">"
db.create_all()
db.session.commit()


@app.route('/', methods=['get'])
def index():
	todos = Todo.query.all()
	data = []
	for todo in todos:
		data.append({
			"note": todo.note
		})
	return render_template("todo.html", todos=data)


@app.route('/api/todos/add', methods=["post"])
def add_todo():
	errors = []
	note = request.form.get("note")
	if not note:
		errors.append("Oops! Looks like you forgot a to fill out the todo field!")
	todo = Todo.query.filter_by(note=note).first()
	if todo:
		errors.append("Oops! A Todo with that name already exists!")
	if errors:
		return jsonify({"errors": errors})
	else:
		new_note = Todo(note=note)
		db.session.add(new_note)
		db.session.commit()
	todos = Todo.query.all()
	return render_template('todo.html', todos=todos)

	@app.route('/api/todos/d', methods=['POST'])
	def inject_todo():
		print("delete")

@app.route('/api/todos/delete', methods=['POST'])
def delete_todo():
	note = request.form.get("note")
	todo = Todo.query.filter_by(note=note).first()
	if todo:
		db.session.delete(todo)
		db.session.commit()
	todos = Todo.query.all()
	return render_template('todo.html', todos=todos)

app.run(host='0.0.0.0', port=5000)