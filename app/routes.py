from flask import render_template, redirect, url_for, request
from . import db
from .models import User, LIONEntry
from . import create_app

app = create_app()

@app.route('/')
def home():
    return render_template('base.html')
