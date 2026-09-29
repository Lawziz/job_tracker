from flask import jsonify, request, abort
from app.api import api_bp
from app import db
from app.models import JobApplication

@api_bp.route('/jobs', methods=['GET'])
def get_jobs():
    """GET: Fetch all tracked jobs from the database and return them as JSON."""
    jobs = JobApplication.query.all()
    
    # Serialize Python database objects into a list of plain Python dictionaries
    jobs_list = []
    for job in jobs:
        jobs_list.append({
            "id": job.id,
            "company": job.company,
            "role": job.role,
            "status": job.status,
            "date_applied": job.date_applied.strftime('%Y-%m-%d')
        })
        
    return jsonify({"jobs": jobs_list}), 200


@api_bp.route('/jobs', methods=['POST'])
def create_job():
    """POST: Accept JSON data from a client to track a new job application."""
    data = request.get_json() or {}
    
    # API Validation: Ensure required JSON payloads exist
    if 'company' not in data or 'role' not in data or 'user_id' not in data:
        return jsonify({"error": "Missing required fields: company, role, user_id"}), 400
        
    new_job = JobApplication(
        company=data['company'],
        role=data['role'],
        user_id=data['user_id'],
        status=data.get('status', 'Applied') # Default value fallback
    )
    
    db.session.add(new_job)
    db.session.commit()
    
    return jsonify({
        "message": "Job tracked successfully!",
        "job_id": new_job.id
    }), 201


@api_bp.route('/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    """DELETE: Remove a specific job entry by its unique database ID."""
    job = JobApplication.query.get_or_404(job_id)
    
    db.session.delete(job)
    db.session.commit()
    
    return jsonify({"message": f"Job application {job_id} deleted successfully"}), 200
