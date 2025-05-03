from flask import Blueprint, render_template, request, flash, redirect, url_for
from website.forms import NoteForm
from .models import Note
from flask_login import login_required, current_user
from website import db

views = Blueprint('views', __name__)

@views.route('/', methods=['POST', 'GET'])
@login_required
def home():
    form = NoteForm()
    if request.method == 'POST' and form.validate_on_submit():
        new_note = Note(data=form.data.data, user_id=current_user.id)
        db.session.add(new_note)
        db.session.commit()
        flash('Note added!', category='success')
        return redirect(url_for('views.home'))
    return render_template('home.html', form=form, user=current_user)

