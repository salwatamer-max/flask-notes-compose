from flask import Flask, render_template, request, redirect, flash, url_for
from app.db import get_notes, add_note, delete_note, update_note

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Add this for flash messages

@app.route('/')
def index():
    try:
        notes = get_notes()
        print(f"Retrieved {len(notes)} notes from database")  # Debug print
        return render_template('index.html', notes=notes)
    except Exception as e:
        print(f"Error in index route: {e}")
        flash('Error loading notes', 'error')
        return render_template('index.html', notes=[])

@app.route('/add', methods=['POST'])
def add():
    try:
        content = request.form.get('content')
        print(f"Adding note with content: {content[:50]}...")  # Debug print
        if content:
            success = add_note(content)
            if success:
                flash('Note added successfully!', 'success')
            else:
                flash('Error adding note', 'error')
        else:
            flash('Note content cannot be empty', 'error')
    except Exception as e:
        print(f"Error in add route: {e}")
        flash('Error adding note', 'error')
    
    return redirect(url_for('index'))

@app.route('/delete/<int:note_id>', methods=['POST'])
def delete(note_id):
    try:
        print(f"Attempting to delete note with ID: {note_id}")  # Debug print
        success = delete_note(note_id)
        if success:
            flash('Note deleted successfully!', 'success')
            print(f"Successfully deleted note {note_id}")
        else:
            flash('Error deleting note', 'error')
            print(f"Failed to delete note {note_id}")
    except Exception as e:
        print(f"Error in delete route: {e}")
        flash('Error deleting note', 'error')
    
    return redirect(url_for('index'))

@app.route('/edit/<int:note_id>', methods=['POST'])
def edit(note_id):
    try:
        new_content = request.form.get('content')
        print(f"Attempting to edit note {note_id} with content: {new_content[:50]}...")  # Debug print
        
        if new_content:
            success = update_note(note_id, new_content)
            if success:
                flash('Note updated successfully!', 'success')
                print(f"Successfully updated note {note_id}")
            else:
                flash('Error updating note', 'error')
                print(f"Failed to update note {note_id}")
        else:
            flash('Note content cannot be empty', 'error')
            print("Edit failed: empty content")
    except Exception as e:
        print(f"Error in edit route: {e}")
        flash('Error updating note', 'error')
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)  # Enable debug mode
