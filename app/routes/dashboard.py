from flask import Blueprint, render_template, session, redirect, url_for
from app import mysql

dashboard_bp = Blueprint('dashboard', __name__)

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('user_id'):
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated

@dashboard_bp.route('/dashboard')
@login_required
def index():
    user_id = session['user_id']
    cur = mysql.connection.cursor()

    # Events the user is hosting
    cur.execute("""
        SELECT * FROM events 
        WHERE host_id = %s 
        ORDER BY start_datetime ASC
    """, (user_id,))
    hosted_events = cur.fetchall()

    # Events the user has registered for
    cur.execute("""
        SELECT e.*, r.registered_at 
        FROM events e
        JOIN registrations r ON e.id = r.event_id
        WHERE r.user_id = %s
        ORDER BY e.start_datetime ASC
    """, (user_id,))
    registered_events = cur.fetchall()

    cur.close()
    return render_template('dashboard/index.html',
                           hosted_events=hosted_events,
                           registered_events=registered_events)