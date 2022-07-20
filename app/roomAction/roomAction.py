from flask import Flask, Blueprint, session, redirect, url_for, render_template, request
from . import roomAction
from .forms import LoginForm

@roomAction.route('/createRoom', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        session['room'] = form.room.data
        return redirect(url_for('.listen'))
    elif request.method == 'GET':
        form.name.data = session.get('name', '')
        form.room.data = session.get('room', '')
    return render_template('createRoom.html', form=form)


