from flask_mail import Message
from . import mail  # Import the Mail instance

def send_weekly_reports():
    users = User.query.all()
    for user in users:
        # Generate report content
        logs = get_previous_work_week_logs(user.id)
        ai_summary = generate_ai_summary(logs)
        # Generate PDF and send email (similar to send_report route)
        # Include manager_email from user's team
