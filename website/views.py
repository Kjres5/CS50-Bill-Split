from flask import Blueprint, render_template, request, flash, jsonify, session, redirect
from flask_login import login_required, current_user
from .models import Transaction, User
from . import db
import json
from .bill import calculate
import re

def valid_dollar_amount(amt_str):
  if re.match("\d+(.\d+)?", amt_str):
    # checks for "X" or "X.X+" with minimum of 1 digit after period
    return True
  if re.match("\.\d+(\d+)?", amt_str):
    # checks for ".X+" with minimum of 1 digit after period
    return True
  return False

views = Blueprint('views', __name__)

@views.route('/users', methods=['GET', 'POST'])
@login_required
def users():
  if request.method == 'POST':
    user = request.form.get('new_user')
    if len(user.strip()) > 0:
      friends = current_user.friends
      if len(friends) > 0: 
        friends += ","
      friends += user.strip()
      current_user.friends = friends
      db.session.commit()
    else:
      flash(' Please input user', category='error')
    
  if len(current_user.friends) == 0:
    users = list()
  else:
    users = current_user.friends.split(",")
  return render_template("users.html", user=current_user, users = users)

@views.route('/', methods=['GET', 'POST'])
@login_required 
def home():
  if len(current_user.friends) == 0:
    flash('Please input user', category='error')
    return redirect('/users')
  users = current_user.friends.split(",")
  if request.method == 'POST':
    name = request.form.get("user_name")
    expense = request.form.get("expense")
    cost_str = request.form.get("cost")

    if name not in users:
      flash('Please select valid payer using the dropdown', category='error')
      return render_template("home.html", user=current_user, users = users)

    # checks if cost fits decimal
    if not valid_dollar_amount(cost_str):
      flash('Cost is not numeric', category='error')  
      return render_template("home.html", user=current_user, users = users)
    cost = cost_str
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
  new_bill = calculate(transaction_list, users) if len(transaction_list) > 0 else {}

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

@views.route('/delete-user', methods=['POST'])
def delete_user():
  print("deleting user now")
  if len(current_user.friends) == 0:
    users = list()
  else:
    users = current_user.friends.split(",")
  data = json.loads(request.data)

  try:
    users.remove(data["user_name"])
    current_user.friends = ",".join(users)
    db.session.commit()
  except ValueError:
    flash("User doesn't exist", category="error")

  return jsonify({})


@views.route('/flash-copied-text', methods=['POST'])
def flash_copied_text():
  flash("Copied! Share now!", category="success")

  return jsonify({})
