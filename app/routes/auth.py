from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import mysql, bcrypt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    return render_template('index.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm  = request.form.get('confirm_password', '')

        # Basic validation
        if not username or not email or not password:
            flash('All fields are required.', 'error')
            return render_template('auth/register.html')

        if password != confirm:
            flash('Passwords do not match.', 'error')
            return render_template('auth/register.html')

        if len(password) < 6:
            flash('Password must be at least 6 characters.', 'error')
            return render_template('auth/register.html')

        cur = mysql.connection.cursor()

        # Check if username or email already exists
        cur.execute("SELECT id FROM users WHERE username = %s OR email = %s", (username, email))
        existing = cur.fetchone()
        if existing:
            flash('Username or email already taken.', 'error')
            cur.close()
            return render_template('auth/register.html')

        # Hash password and insert
        hashed = bcrypt.generate_password_hash(password).decode('utf-8')
        cur.execute(
            "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
            (username, email, hashed)
        )
        mysql.connection.commit()
        cur.close()

        flash('Account created! Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        if not username or not password:
            flash('All fields are required.', 'error')
            return render_template('auth/login.html')

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()

        if not user or not bcrypt.check_password_hash(user['password'], password):
            flash('Invalid username or password.', 'error')
            return render_template('auth/login.html')

        session['user_id'] = user['id']
        session['username'] = user['username']

        flash(f"Welcome back, {user['username']}!", 'success')
        return redirect(url_for('dashboard.index'))

    return render_template('auth/login.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.index'))