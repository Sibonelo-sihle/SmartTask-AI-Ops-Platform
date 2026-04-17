from datetime import datetime

def predict_risk(task):
    if task['status'] != 'complete':
        days_left = (task['deadline'] - datetime.utcnow()).days

        if days_left < 2:
            return "high"
        elif days_left < 5:
            return "medium"

    return "low"


def suggest_action(risk):
    if risk == "high":
        return "Increase priority or extend deadline"
    elif risk == "medium":
        return "Monitor task closely"
    return "On track"