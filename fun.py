
from pickle import FALSE
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask, request, render_template

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:hacker1@localhost:5432/users"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = FALSE
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class UsersModel(db.Model):
    __tablename__ = 'cart'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String())
    password = db.Column(db.String())

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __repr__(self):
        return f"<User {self.email}>"

@app.route('/', methods=['GET'])
def home():
    return render_template('logn.html')

@app.route('/users2', methods=['POST', 'GET'])
def handle_users():
    if request.method == 'POST':
        if request.form:
            data = request.form
            
            
            new_user = UsersModel(email=data['email'],item=data['phone'])
            
            db.session.add(new_user)
            db.session.commit()
            return {"message": f"user {new_user.email} has been created successfully."}
        else:
            return {"error": "No data passed in form."}

    elif request.method == 'GET':
        users = UsersModel.query.all()
        results = [
            {
                "name": user.name
            } for user in users]

        return {"count": len(results), "users": results}
if __name__ == "__main__":
    app.run()

