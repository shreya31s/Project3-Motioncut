from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

# Configure SQLite Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Expense model
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.String(10), nullable=False)

# Create the database
with app.app_context():
    db.create_all()

# Get all expenses
@app.route('/api/expenses', methods=['GET'])
def get_expenses():
    expenses = Expense.query.all()
    return jsonify([{'id': e.id, 'description': e.description, 'amount': e.amount, 'date': e.date} for e in expenses])

# Add a new expense
@app.route('/api/expenses', methods=['POST'])
def add_expense():
    data = request.json
    new_expense = Expense(description=data['description'], amount=data['amount'], date=data['date'])
    db.session.add(new_expense)
    db.session.commit()
    return jsonify({'id': new_expense.id, 'description': new_expense.description, 'amount': new_expense.amount, 'date': new_expense.date}), 201

# Delete an expense
@app.route('/api/expenses/<int:id>', methods=['DELETE'])
def delete_expense(id):
    expense = Expense.query.get_or_404(id)
    db.session.delete(expense)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)

