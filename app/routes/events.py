from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import mysql
import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app

events_bp = Blueprint('events', __name__)

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('user_id'):
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@events_bp.route('/events')
def browse():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT e.*, u.username as host_name 
        FROM events e
        JOIN users u ON e.host_id = u.id
        WHERE e.is_public = 1
        ORDER BY e.start_datetime ASC
    """)
    events = cur.fetchall()
    cur.close()
    return render_template('events/browse.html', events=events)


@events_bp.route('/events/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        title        = request.form.get('title', '').strip()
        description  = request.form.get('description', '').strip()
        location     = request.form.get('location', '').strip()
        start_dt     = request.form.get('start_datetime')
        end_dt       = request.form.get('end_datetime')
        capacity     = request.form.get('capacity', 0)
        is_public    = 1 if request.form.get('is_public') == 'on' else 0
        banner_url   = request.form.get('banner_url', '').strip()
        banner_image = None

        # Validation
        if not title or not start_dt or not end_dt or not capacity:
            flash('Please fill in all required fields.', 'error')
            return render_template('events/create.html')

        if int(capacity) < 1:
            flash('Capacity must be at least 1.', 'error')
            return render_template('events/create.html')

        # Handle file upload
        file = request.files.get('banner_image')
        if file and file.filename != '' and allowed_file(file.filename):
            ext = file.filename.rsplit('.', 1)[1].lower()
            filename = f"{uuid.uuid4().hex}.{ext}"
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            banner_image = filename
            banner_url = None  # prefer uploaded file over URL

        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO events 
            (title, description, location, start_datetime, end_datetime, capacity, is_public, banner_url, banner_image, host_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (title, description, location, start_dt, end_dt, capacity, is_public, banner_url, banner_image, session['user_id']))
        mysql.connection.commit()
        event_id = cur.lastrowid
        cur.close()

        flash('Event created successfully!', 'success')
        return redirect(url_for('events.detail', event_id=event_id))

    return render_template('events/create.html')


@events_bp.route('/events/<int:event_id>')
def detail(event_id):
    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT e.*, u.username as host_name 
        FROM events e
        JOIN users u ON e.host_id = u.id
        WHERE e.id = %s
    """, (event_id,))
    event = cur.fetchone()

    if not event:
        flash('Event not found.', 'error')
        return redirect(url_for('events.browse'))

    # Check if current user is registered
    is_registered = False
    if session.get('user_id'):
        cur.execute("""
            SELECT id FROM registrations 
            WHERE user_id = %s AND event_id = %s
        """, (session['user_id'], event_id))
        is_registered = cur.fetchone() is not None

    # Get attendees count
    cur.execute("SELECT COUNT(*) as count FROM registrations WHERE event_id = %s", (event_id,))
    attendee_count = cur.fetchone()['count']

    cur.close()
    return render_template('events/detail.html',
                           event=event,
                           is_registered=is_registered,
                           attendee_count=attendee_count)


@events_bp.route('/events/<int:event_id>/register', methods=['POST'])
@login_required
def register(event_id):
    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM events WHERE id = %s", (event_id,))
    event = cur.fetchone()

    if not event:
        flash('Event not found.', 'error')
        return redirect(url_for('events.browse'))

    # Check capacity
    if event['registered_count'] >= event['capacity']:
        flash('Sorry, this event is full.', 'error')
        return redirect(url_for('events.detail', event_id=event_id))

    # Check already registered
    cur.execute("""
        SELECT id FROM registrations 
        WHERE user_id = %s AND event_id = %s
    """, (session['user_id'], event_id))
    if cur.fetchone():
        flash('You are already registered for this event.', 'error')
        return redirect(url_for('events.detail', event_id=event_id))

    # Register
    cur.execute("""
        INSERT INTO registrations (user_id, event_id) VALUES (%s, %s)
    """, (session['user_id'], event_id))

    # Update count
    cur.execute("""
        UPDATE events SET registered_count = registered_count + 1 WHERE id = %s
    """, (event_id,))

    mysql.connection.commit()
    cur.close()

    flash('Successfully registered for the event!', 'success')
    return redirect(url_for('events.detail', event_id=event_id))


@events_bp.route('/events/<int:event_id>/unregister', methods=['POST'])
@login_required
def unregister(event_id):
    cur = mysql.connection.cursor()

    cur.execute("""
        DELETE FROM registrations WHERE user_id = %s AND event_id = %s
    """, (session['user_id'], event_id))

    cur.execute("""
        UPDATE events SET registered_count = GREATEST(registered_count - 1, 0) WHERE id = %s
    """, (event_id,))

    mysql.connection.commit()
    cur.close()

    flash('You have unregistered from the event.', 'info')
    return redirect(url_for('events.detail', event_id=event_id))

@events_bp.route('/events/<int:event_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(event_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM events WHERE id = %s", (event_id,))
    event = cur.fetchone()

    if not event:
        flash('Event not found.', 'error')
        return redirect(url_for('dashboard.index'))

    if event['host_id'] != session['user_id']:
        flash('You are not authorized to edit this event.', 'error')
        return redirect(url_for('events.detail', event_id=event_id))

    if request.method == 'POST':
        title       = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        location    = request.form.get('location', '').strip()
        start_dt    = request.form.get('start_datetime')
        end_dt      = request.form.get('end_datetime')
        capacity    = request.form.get('capacity', 0)
        is_public   = 1 if request.form.get('is_public') == 'on' else 0
        banner_url  = request.form.get('banner_url', '').strip()
        banner_image = event['banner_image']

        if not title or not start_dt or not end_dt or not capacity:
            flash('Please fill in all required fields.', 'error')
            return render_template('events/edit.html', event=event)

        if int(capacity) < event['registered_count']:
            flash(f'Capacity cannot be less than current registrations ({event["registered_count"]}).', 'error')
            return render_template('events/edit.html', event=event)

        # Handle new file upload
        file = request.files.get('banner_image')
        if file and file.filename != '' and allowed_file(file.filename):
            # Delete old image if exists
            if event['banner_image']:
                old_path = os.path.join(current_app.config['UPLOAD_FOLDER'], event['banner_image'])
                if os.path.exists(old_path):
                    os.remove(old_path)

            ext = file.filename.rsplit('.', 1)[1].lower()
            filename = f"{uuid.uuid4().hex}.{ext}"
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            banner_image = filename
            banner_url = None

        cur.execute("""
            UPDATE events SET
                title = %s,
                description = %s,
                location = %s,
                start_datetime = %s,
                end_datetime = %s,
                capacity = %s,
                is_public = %s,
                banner_url = %s,
                banner_image = %s
            WHERE id = %s
        """, (title, description, location, start_dt, end_dt, capacity,
              is_public, banner_url, banner_image, event_id))
        mysql.connection.commit()
        cur.close()

        flash('Event updated successfully!', 'success')
        return redirect(url_for('events.detail', event_id=event_id))

    cur.close()
    return render_template('events/edit.html', event=event)


@events_bp.route('/events/<int:event_id>/delete', methods=['POST'])
@login_required
def delete(event_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM events WHERE id = %s", (event_id,))
    event = cur.fetchone()

    if not event or event['host_id'] != session['user_id']:
        flash('Not authorized.', 'error')
        return redirect(url_for('dashboard.index'))

    # Delete banner image if exists
    if event['banner_image']:
        path = os.path.join(current_app.config['UPLOAD_FOLDER'], event['banner_image'])
        if os.path.exists(path):
            os.remove(path)

    cur.execute("DELETE FROM events WHERE id = %s", (event_id,))
    mysql.connection.commit()
    cur.close()

    flash('Event deleted.', 'info')
    return redirect(url_for('dashboard.index'))