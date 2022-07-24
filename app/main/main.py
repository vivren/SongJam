from flask import session, redirect, url_for, render_template, request
from . import mainBP

@mainBP.route('/')
def home():
    return render_template('main/home.html')
