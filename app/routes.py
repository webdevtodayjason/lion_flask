from flask import Blueprint, render_template, redirect, url_for, request, flash, abort, send_file
from . import db
from .models import User, LIONEntry, DailyLog, Report
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from weasyprint import HTML
import io
from flask_wtf.csrf import generate_csrf  # Import generate_csrf if used in this file
from .forms import RegistrationForm, LoginForm, DailyLogForm
from urllib.parse import urlparse, urljoin
from datetime import datetime, timedelta
from flask_mail import Message
from . import mail  # Import the Mail instance

# Initialize Blueprint
main = Blueprint('main', __name__)

@main.route('/')
@login_required
def home():
    return render_template('home.html')  # Ensure 'home.html' exists

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Access form data using form.username.data, form.email.data, etc.
        username = form.username.data
        email = form.email.data
        password = form.password.data
        # Add validation as needed

        if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
            flash('Username or Email already exists.', 'danger')
            return redirect(url_for('main.register'))

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Registration successful! You are now logged in.', 'success')
        return redirect(url_for('main.home'))
    return render_template('register.html', form=form)

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return (
        test_url.scheme in ("http", "https")
        and ref_url.netloc == test_url.netloc
    )

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        username_or_email = form.username_or_email.data
        password = form.password.data
        user = User.query.filter(
            (User.username == username_or_email) | (User.email == username_or_email)
        ).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully.', 'success')
            next_page = request.args.get('next')
            if next_page and is_safe_url(next_page):
                return redirect(next_page)
            else:
                return redirect(url_for('main.home'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')
    return render_template('login.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.login'))

@main.route('/entries')
@login_required
def entries():
    lion_entries = LIONEntry.query.filter_by(author=current_user).all()
    return render_template('entries.html', entries=lion_entries)

@main.route('/entry/new', methods=['GET', 'POST'])
@login_required
def new_entry():
    if request.method == 'POST':
        last_week = request.form['last_week']
        issues = request.form['issues']
        opportunities = request.form['opportunities']
        next_week = request.form['next_week']

        entry = LIONEntry(
            author=current_user,
            last_week_achievements=last_week,
            issues=issues,
            opportunities=opportunities,
            next_week_commitments=next_week
        )
        db.session.add(entry)
        db.session.commit()
        flash('New L.I.O.N entry created successfully.', 'success')
        return redirect(url_for('main.entries'))
    return render_template('new_entry.html')

@main.route('/entry/<int:entry_id>')
@login_required
def view_entry(entry_id):
    entry = LIONEntry.query.get_or_404(entry_id)
    if entry.author != current_user:
        abort(403)
    return render_template('view_entry.html', entry=entry)

@main.route('/entry/<int:entry_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_entry(entry_id):
    entry = LIONEntry.query.get_or_404(entry_id)
    if entry.author != current_user:
        abort(403)
    if request.method == 'POST':
        entry.last_week_achievements = request.form['last_week']
        entry.issues = request.form['issues']
        entry.opportunities = request.form['opportunities']
        entry.next_week_commitments = request.form['next_week']
        db.session.commit()
        flash('L.I.O.N entry updated successfully.', 'success')
        return redirect(url_for('main.entries'))
    return render_template('edit_entry.html', entry=entry)

@main.route('/entry/<int:entry_id>/delete', methods=['POST'])
@login_required
def delete_entry(entry_id):
    entry = LIONEntry.query.get_or_404(entry_id)
    if entry.author != current_user:
        abort(403)
    db.session.delete(entry)
    db.session.commit()
    flash('L.I.O.N entry deleted successfully.', 'info')
    return redirect(url_for('main.entries'))

def get_previous_work_week_logs(user_id):
    today = datetime.utcnow().date()
    last_monday = today - timedelta(days=today.weekday() + 7)
    last_friday = last_monday + timedelta(days=4)
    logs = DailyLog.query.filter(
        DailyLog.user_id == user_id,
        DailyLog.date >= last_monday,
        DailyLog.date <= last_friday
    ).all()
    return logs

def generate_ai_summary(logs):
    # Placeholder function for AI summary generation
    # In practice, integrate with an AI API or service
    summary = {
        'last_week': 'AI-generated summary of last week achievements.',
        'issues': 'AI-generated summary of issues faced.',
        'opportunities': 'AI-generated summary of opportunities.',
        'next_week': 'AI-generated summary of next week commitments.'
    }
    return summary

@main.route('/generate_report', methods=['GET', 'POST'])
@login_required
def generate_report():
    if request.method == 'POST':
        # User has edited the AI-generated content and submitted the form
        last_week = request.form['last_week']
        issues = request.form['issues']
        opportunities = request.form['opportunities']
        next_week = request.form['next_week']
        # Save the report content or proceed to sending email
        # For now, we'll render the preview
        return render_template('report_preview.html', last_week=last_week, issues=issues,
                               opportunities=opportunities, next_week=next_week)
    else:
        # Generate AI summary based on previous work week logs
        logs = get_previous_work_week_logs(current_user.id)
        ai_summary = generate_ai_summary(logs)
        return render_template('edit_report.html', ai_summary=ai_summary)

@main.route('/daily_logs', methods=['GET', 'POST'])
@login_required
def daily_logs():
    today = datetime.utcnow().date()
    current_date = today.strftime('%A, %B %d, %Y')

    # Check if a log for today already exists
    existing_log = DailyLog.query.filter_by(user_id=current_user.id, date=today).first()

    show_modal = False  # Default value
    if existing_log:
        show_modal = True  # Trigger modal in template
        form = DailyLogForm(obj=existing_log)  # Pre-populate form with existing data
    else:
        form = DailyLogForm()  # Empty form for new entry

    if form.validate_on_submit():
        if existing_log:
            # Update existing log
            existing_log.achievements = form.achievements.data
            existing_log.issues = form.issues.data
            existing_log.opportunities = form.opportunities.data
            existing_log.next_day_tasks = form.next_day_tasks.data
            db.session.commit()
            flash('Daily log updated successfully.', 'success')
        else:
            # Create new daily log
            daily_log = DailyLog(
                user_id=current_user.id,
                date=today,
                achievements=form.achievements.data,
                issues=form.issues.data,
                opportunities=form.opportunities.data,
                next_day_tasks=form.next_day_tasks.data
            )
            db.session.add(daily_log)
            db.session.commit()
            flash('Daily log submitted successfully.', 'success')
        return redirect(url_for('main.view_daily_logs'))

    return render_template('daily_logs.html', form=form, current_date=current_date, show_modal=show_modal, existing_log=existing_log)

# Add a new route for editing daily logs
@main.route('/daily_logs/edit/<int:log_id>', methods=['GET', 'POST'])
@login_required
def edit_daily_log(log_id):
    log = DailyLog.query.get_or_404(log_id)
    if log.user_id != current_user.id:
        abort(403)
    form = DailyLogForm(obj=log)
    if form.validate_on_submit():
        log.achievements = form.achievements.data
        log.issues = form.issues.data
        log.opportunities = form.opportunities.data
        log.next_day_tasks = form.next_day_tasks.data
        db.session.commit()
        flash('Daily log updated successfully.', 'success')
        return redirect(url_for('main.view_daily_logs'))
    current_date = log.date.strftime('%A, %B %d, %Y')
    return render_template('edit_daily_log.html', form=form, current_date=current_date)

@main.route('/daily_logs/view')
@login_required
def view_daily_logs():
    logs = DailyLog.query.filter_by(user_id=current_user.id).order_by(DailyLog.date.desc()).all()
    print(f"Current user: {current_user.username}, ID: {current_user.id}")
    print(f"Number of logs retrieved: {len(logs)}")
    return render_template('view_daily_logs.html', logs=logs)

@main.route('/send_report', methods=['POST'])
@login_required
def send_report():
    last_week = request.form['last_week']
    issues = request.form['issues']
    opportunities = request.form['opportunities']
    next_week = request.form['next_week']

    # Generate PDF using WeasyPrint
    rendered = render_template('report_template.html', last_week=last_week, issues=issues,
                               opportunities=opportunities, next_week=next_week)
    pdf = HTML(string=rendered).write_pdf()

    # Prepare email
    recipients = [current_user.email]
    if current_user.manager_email:
        recipients.append(current_user.manager_email)

    msg = Message('Weekly L.I.O.N Report', sender='noreply@example.com', recipients=recipients)
    msg.body = 'Please find the attached weekly L.I.O.N report.'
    msg.attach('LION_Report.pdf', 'application/pdf', pdf)

    # Send email
    try:
        mail.send(msg)
        flash('Report sent successfully.', 'success')
        # Store report record
        report = Report(
            user_id=current_user.id,
            recipients=', '.join(recipients),
            last_week=last_week,
            issues=issues,
            opportunities=opportunities,
            next_week=next_week
        )
        db.session.add(report)
        db.session.commit()
    except Exception as e:
        flash('Failed to send report. Please try again later.', 'danger')
        # Log the exception e if needed

    return redirect(url_for('main.home'))
