from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy.exc import SQLAlchemyError
import logging

from website.forms import NoteForm
from website.models import Note
from website import db

views = Blueprint('views', __name__)
logger = logging.getLogger(__name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    form = NoteForm()
    
    try:
        if request.method == 'POST' and form.validate_on_submit():
            # Create new note
            new_note = Note(
                data=form.data.data.strip(),  # Clean whitespace
                user_id=current_user.id
            )
            
            db.session.add(new_note)
            db.session.commit()
            
            flash('Note added successfully!', 'success')
            logger.info(f'User {current_user.id} added a new note')
            return redirect(url_for('views.home'))
            
        # Get all notes for the current user
        notes = Note.query.filter_by(user_id=current_user.id)\
                   .order_by(Note.date_created.desc())\
                   .all()
                   
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f'Database error in home route: {str(e)}')
        flash('An error occurred while processing your request', 'error')
        notes = []  # Return empty list if there's an error
    
    return render_template(
        'home.html',
        form=form,
        user=current_user,
        notes=notes
    )

@views.route('/delete-note/<int:note_id>', methods=['POST'])
@login_required
def delete_note(note_id):
    try:
        note = Note.query.filter_by(id=note_id, user_id=current_user.id).first()
        
        if not note:
            flash('Note not found or you don\'t have permission', 'error')
            logger.warning(f'User {current_user.id} attempted to delete invalid note {note_id}')
        else:
            db.session.delete(note)
            db.session.commit()
            flash('Note deleted successfully!', 'success')
            logger.info(f'User {current_user.id} deleted note {note_id}')
            
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f'Error deleting note: {str(e)}')
        flash('Failed to delete note', 'error')
    
    return redirect(url_for('views.home'))

@views.route('/edit-note/<int:note_id>', methods=['GET', 'POST'])
@login_required
def edit_note(note_id):
    note = Note.query.filter_by(id=note_id, user_id=current_user.id).first()
    
    if not note:
        flash('Note not found or you don\'t have permission', 'error')
        return redirect(url_for('views.home'))
    
    form = NoteForm(obj=note)  # Pre-populate form with existing note data
    
    if request.method == 'POST' and form.validate_on_submit():
        try:
            note.data = form.data.data.strip()
            db.session.commit()
            flash('Note updated successfully!', 'success')
            logger.info(f'User {current_user.id} updated note {note_id}')
            return redirect(url_for('views.home'))
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f'Error updating note: {str(e)}')
            flash('Failed to update note', 'error')
    
    return render_template('edit_note.html', form=form, note_id=note_id)