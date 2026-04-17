from datetime import datetime

def predict_risk(task):
    # Handle if deadline is missing or task is complete
    if task.get('status') == 'complete' or not task.get('deadline'):
        return "low"
    
    days_left = (task['deadline'] - datetime.utcnow()).days
    
    if days_left < 2:
        return "high"
    elif days_left < 5:
        return "medium"
    else:
        return "low"

def suggest_action(risk):
    if risk == "high":
        return "Increase priority or extend deadline"
    elif risk == "medium":
        return "Monitor task closely"
    return "On track"