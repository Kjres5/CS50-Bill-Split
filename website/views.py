from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, Transaction
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
  if request.method == 'POST':
    name = request.form.get("user_name")
    expense = request.form.get("expense")
    cost = request.form.get("cost")
    if not cost.isnumeric(): flash('Cost is not numeric', category='error')
  
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

  return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
  note = json.loads(request.data)
  noteId = note['noteId']
  note = Note.query.get(noteId)
  if note:
    if note.user_id == current_user.id:
      db.session.delete(note)
      db.session.commit()

    return jsonify({})
