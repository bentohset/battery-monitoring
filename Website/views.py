from flask import Blueprint, render_template, request, flash, jsonify, url_for,redirect,session
from flask_login import login_required, current_user
from .models import *
from . import db
from sqlalchemy import or_
import sqlite3 as sql


conn=sql.connect('database.db')
c=conn.cursor()

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method=='POST':
        battery_id=request.form.get('battery_id')
        temperature=request.form.get('temperature')
        new_entry=Batteries(id=battery_id, temperature=temperature)
        db.session.add(new_entry)
        db.session.commit()
        print("yay")

    return render_template("home.html", user=current_user)