from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from app import app, db
from app.forms import LoginForm, RegistrationForm, ContactForm, SubmitForm
from app.models import User, Contact, Submit
from datetime import datetime
import os


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('private')
        return redirect(url_for('private'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/private', methods=['GET', 'POST'])
@login_required
def private():
    contact = Contact.query.all()
    submit = Submit.query.all()
    return render_template('private.html', title='Private', contact=contact, submit=submit,)

@app.route('/private_delete_admin', methods=['GET', 'POST'])
@login_required
def private_delete_admin():
    user = User.query.all()
    return render_template('private_delete_admin.html', title='private_delete_admin', user=user)

@app.route('/private_delete_admin_go/<uid>', methods=['GET', 'POST'])
@login_required
def private_delete_admin_go(uid):
    u = User.query.get(uid)
    db.session.delete(u)
    db.session.commit()
    return redirect(url_for('private_delete_admin'))

@app.route('/private_contact_delete/<cid>', methods=['GET', 'POST'])
@login_required
def private_contact_delete(cid):
    c = Contact.query.get(cid)
    db.session.delete(c)
    db.session.commit()
    return redirect(url_for('private'))

@app.route('/private_submit_delete/<cid>', methods=['GET', 'POST'])
@login_required
def private_submit_delete(cid):
    s = Submit.query.get(cid)
    os.remove('app/static/musictemp/' + s.trackname)
    db.session.delete(s)
    db.session.commit()
    return redirect(url_for('private'))

@app.route('/private_move_submit/<cid>', methods=['GET', 'POST'])
@login_required
def private_move_submit(cid):
    s = Submit.query.get(cid)
    os.rename('app/static/musictemp/' + s.trackname, 'app/static/music/' + s.trackname)
    db.session.delete(s)
    db.session.commit()
    return redirect(url_for('private'))

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        contact = Contact(name=form.name.data,
                          email=form.email.data,
                          message=form.message.data)
        db.session.add(contact)
        db.session.commit()
        flash('Message submitted')
        return redirect(url_for('index')) 
    return render_template('contact.html', title='Contact', form=form)
    
@app.route('/listen')
def listen():
    return render_template('listen.html', title="Listen")

@app.route("/submit", methods=['GET', 'POST'])
def submit():
    form = SubmitForm()
    if form.validate_on_submit():
        static_dir = os.path.join(
            os.path.dirname(app.instance_path), 'app/static'
        )
        a = form.audiofile.data
        audiofile = secure_filename(a.filename)
        a.save(os.path.join(static_dir, 'musictemp', audiofile))
        submit = Submit(title=form.title.data,
                        description=form.description.data,
                        artistname=form.artistname.data,
                        artistemail=form.artistemail.data,
                        trackname=audiofile)
        db.session.add(submit)
        db.session.commit()
        flash("Audio saved successfully.")
        return render_template('submit.html', title="Submit", form=form)
    return render_template('submit.html', title="Submit", form=form)
