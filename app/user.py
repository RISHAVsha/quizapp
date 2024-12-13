from models import User, db
from app import app

with app.app_context():
#creating user for just some testing
    if not User:
        user = User(username="rishav", email="rishavshah@gmail.com")
        user.set_password("rishav") 
        db.session.add(user)
        db.session.commit()
    

    