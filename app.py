from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from sklearn.ensemble import RandomForestRegressor
from datetime import datetime, timedelta

app = Flask(__name__)
@app.route('/')
def home():
    return 'Hello, this is the home page!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
api = Api(app)
db = SQLAlchemy(app)
jwt = JWTManager(app)


# Database Model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    deadline = db.Column(db.DateTime, nullable=False)
    importance = db.Column(db.Integer, nullable=False)
    workload = db.Column(db.Integer, nullable=False)


# Machine Learning Model
class PriorityModel:
    def __init__(self):
        # This is a placeholder. In a real-world scenario, train a model with a relevant dataset.
        self.model = RandomForestRegressor()

    def predict_priority(self, task):
        # This is a placeholder. In a real-world scenario, use the trained model to predict task priority.
        return 0.5


# Resource for Task Management
class TaskResource(Resource):
    @jwt_required()
    def get(self):
        tasks = Task.query.all()
        task_data = [{'name': task.name, 'deadline': task.deadline, 'importance': task.importance,
                      'workload': task.workload} for task in tasks]
        return jsonify({'tasks': task_data})

    @jwt_required()
    def post(self):
        data = request.get_json()
        new_task = Task(name=data['name'], deadline=datetime.strptime(data['deadline'], '%Y-%m-%d %H:%M:%S'),
                        importance=data['importance'], workload=data['workload'])
        db.session.add(new_task)
        db.session.commit()
        return jsonify({'message': 'Task added successfully'})


# Resource for AI Prioritization
class PriorityResource(Resource):
    @jwt_required()
    def get(self, task_id):
        task = Task.query.get_or_404(task_id)
        model = PriorityModel()
        priority = model.predict_priority(task)
        return jsonify({'priority': priority})


# Login Resource
class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        # In a real-world scenario, validate user credentials from a secure database.
        access_token = create_access_token(identity=data['username'], expires_delta=timedelta(hours=1))
        return jsonify(access_token=access_token)


# Initialize Resources
api.add_resource(TaskResource, '/tasks')
api.add_resource(PriorityResource, '/priority/<int:task_id>')
api.add_resource(LoginResource, '/login')


if __name__ == '__main__':
    
    with app.app_context():
        # Run your application or any code that requires the application context
        db.create_all()
        app.run(debug=True)

