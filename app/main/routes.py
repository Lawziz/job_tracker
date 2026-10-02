from flask import Blueprint, render_template, request, redirect, url_for, abort
from flask_login import login_required, current_user
from app import db
from app.models import JobApplication

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        company = request.form.get('company')
        role = request.form.get('role')
        new_job = JobApplication(company=company, role=role, user_id=current_user.id)
        db.session.add(new_job)
        db.session.commit()
        return redirect(url_for('main.index'))
    
    # Filter only show records belong to the active user session
    jobs = JobApplication.query.filter_by(user_id=current_user.id).order_by(JobApplication.date_applied.desc()).all()
    return render_template('index.html', jobs=jobs)

@main_bp.route('/job/update/<int:job_id>', methods=['POST'])
@login_required
def update_job(job_id):
    job = JobApplication.query.get_or_404(job_id)
    if job.user_id != current_user.id:
        abort(403)
    
    job.status = request.form.get('status')
    db.session.commit()
    return redirect(url_for('main.index'))

@main_bp.route('/job/delete/<int:job_id>', methods=['POST'])
@login_required
def delete_job(job_id):
    job = JobApplication.query.get_or_404(job_id)
    if job.user_id != current_user.id:
        abort(403)
        
    db.session.delete(job)
    db.session.commit()
    return redirect(url_for('main.index'))
