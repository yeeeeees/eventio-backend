from app import create_app, db


# creating app to access databse without starting the server
app = create_app()

with app.app_context():
    """db_manipulation goes here"""
    db.drop_all()
    db.create_all()

# closing the app
print("Database added. Exiting the program...")
