from app import app, db

# Set up the Flask application context
with app.app_context():
    # This will create the tables based on the defined models
    db.create_all()

    # You can add initial data or perform additional setup here if needed
