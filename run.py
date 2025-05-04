# filepath: run.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app, db

app = create_app()

if __name__ == '__main__':
    # Ensure the database tables are created before starting the app
    with app.app_context():
        print("App context is active")
        try:
            db.create_all()  # Create the database tables if they don't exist
            print("Database tables created successfully")
        except Exception as e:
            print(f"Error creating database tables: {e}")
    app.run(debug=True)