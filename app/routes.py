from flask import Blueprint, request, jsonify
from .models import Task
from .ai import predict_risk, suggest_action
from . import db
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return jsonify({"message": "Welcome to SmartTask AI Ops Platform"})

@main.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks])

@main.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    if not data or 'title' not in data or 'deadline' not in data:
        return jsonify({"error": "Title and deadline are required"}), 400
    
    try:
        deadline = datetime.fromisoformat(data['deadline'])
    except ValueError:
        return jsonify({"error": "Invalid deadline format"}), 400
    
    task = Task(
        title=data['title'],
        description=data.get('description', ''),
        deadline=deadline,
        status=data.get('status', 'pending')
    )
    
    db.session.add(task)
    db.session.commit()
    
    return jsonify(task.to_dict()), 201

@main.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get_or_404(task_id)
    risk = predict_risk({
        "deadline": task.deadline,
        "status": task.status
    })
    suggestion = suggest_action(risk)
    task_dict = task.to_dict()
    task_dict['risk'] = risk
    task_dict['suggestion'] = suggestion
    return jsonify(task_dict)