import os
import json
from flask import Flask, jsonify, request, abort

app = Flask(__name__)
app.secret_key = 'supersecretkey'
TASKS_FILE = 'tasks.json'

# Load tasks from JSON file
def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r') as file:
            return json.load(file)
    return []

# Save tasks to JSON file
def save_tasks():
    with open(TASKS_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)

# In-memory storage for tasks loaded from JSON
tasks = load_tasks()

# Helper function to find a task by ID
def find_task(task_id):
    return next((task for task in tasks if task["id"] == task_id), None)

# GET /tasks - Retrieve the list of tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({"tasks": tasks}), 200

# POST /tasks - Create a new task
@app.route('/tasks', methods=['POST'])
def create_task():
    if not request.json or 'title' not in request.json:
        abort(400, "Title is required to create a task")
    print("tasks", tasks)
    new_task = {
        "id": tasks[-1]["id"] + 1 if tasks else 1,  # Auto-increment id
        "title": request.json["title"],
        "description": request.json.get("description", "")
    }
    tasks.append(new_task)
    save_tasks()  # Save to JSON file after adding a new task
    return jsonify(new_task), 201

# DELETE /tasks/<int:task_id> - Delete a task by ID
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = find_task(task_id)
    if not task:
        abort(404, "Task not found")
    
    tasks.remove(task)
    save_tasks()  # Save to JSON file after deleting a task
    return jsonify({"message": "Task deleted"}), 200

# Error handling for invalid routes or methods
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Bad request"}), 400

if __name__ == '__main__':
    app.run(debug=True)
