from flask import Blueprint, request, jsonify
from datetime import datetime
from .models import Task
from . import db
from .ai import predict_risk, suggest_action

main = Blueprint("main", __name__)

@main.route("/")
def home():
    return {"message": "SmartTask API running"}

@main.route("/tasks", methods=["POST"])
def create_task():
    data = request.json

    task = Task(
        title=data["title"],
        description=data.get("description"),
        deadline=datetime.fromisoformat(data["deadline"]),
        status=data.get("status", "pending")
    )

    db.session.add(task)
    db.session.commit()

    return jsonify(task.to_dict()), 201

@main.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()

    result = []
    for task in tasks:
        task_data = task.to_dict()

        risk = predict_risk({
            "deadline": task.deadline,
            "status": task.status
        })

        task_data["risk"] = risk
        task_data["suggestion"] = suggest_action(risk)

        result.append(task_data)

    return jsonify(result)