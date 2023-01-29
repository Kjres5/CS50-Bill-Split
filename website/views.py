from flask import Blueprint, render_template, request, flash, jsonify, session, redirect
from flask_login import login_required, current_user
from .models import Note, Transaction
from . import db
import json
from .bill import calculate

views = Blueprint('views', __name__)

@views.route('/users', methods=['GET', 'POST'])
@login_required
def users():
  if request.method == 'POST':
    users = request.form.getlist('users')
    session["users"] = users
    return redirect("/")
  users = session.get("users")
  if users is None: 
    users = list()
  return render_template("users.html", user=current_user, users = users)

@views.route('/', methods=['GET', 'POST'])
@login_required 
def home():
  users = session.get("users")
  if users is None or users == []:
    flash('Please input user', category='error')
    return redirect('/users')
  if request.method == 'POST':
    name = request.form.get("user_name")
    expense = request.form.get("expense")
    cost = request.form.get("cost")
    if not cost.isnumeric():
      flash('Cost is not numeric', category='error')  
      return render_template("home.html", user=current_user, users = users)
    if expense == "":
      flash('Please input expense', category='error')
      return render_template("home.html", user=current_user, users = users)
  
    new_transaction = Transaction(
      user_id = current_user.id,
      name = name,
      remarks = expense,
      cost = cost
    )
    print(name, expense, cost)
    db.session.add(new_transaction)
    db.session.commit()

    flash('Transaction added!', category='success')

  # format to bill.py requirements
  transaction_list = []
  for tx in current_user.transactions:
    '''
    name -> user
    remarks -> remarks
    cost -> cost
    '''
    new_tx = {
      "user": tx.name,
      "remarks": tx.remarks,
      "cost": tx.cost
    }
    transaction_list.append(new_tx)
  new_bill = calculate(transaction_list, session.get("users")) if len(transaction_list) > 0 else {}

  return render_template("home.html", user=current_user, payments = new_bill, users = users)


@views.route('/delete-transaction', methods=['POST'])
def delete_transaction():
  print("deleting transaction now")
  transaction = json.loads(request.data)
  transactionId= transaction['transactionId']
  transaction = Transaction.query.get(transactionId)
  if transaction:
    if transaction.user_id == current_user.id:
      db.session.delete(transaction)
      db.session.commit()

    return jsonify({})
