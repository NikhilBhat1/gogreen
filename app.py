
from ssl import ALERT_DESCRIPTION_ACCESS_DENIED
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask, request, render_template
import psycopg2
import hashlib
import pandas as pd
import pickle
import numpy as np
dataset = pd.read_csv('nutrition.csv')
df=pd.read_csv('search.csv')
app = Flask(__name__)
salt="#j@nu$w&"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:hacker1@localhost:5432/users"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
migrate = Migrate(app, db)
conn=psycopg2.connect(database="users",user='postgres',password='hacker1',host='localhost',port='5432')
conn.autocommit = True
cursor=conn.cursor()
cursor.execute('''SELECT * from users''')
result=cursor.fetchall()




class UsersModel(db.Model):
    __tablename__ = 'users'



    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    password = db.Column(db.String())
    email=db.Column(db.String())
    age=db.Column(db.String())
    gender=db.Column(db.String())
    mobile=db.Column(db.String())
    address=db.Column(db.String())


    def __init__(self, name, password,email,age,gender,mobile,address):
        self.name = name
        self.password = password
        self.email=email
        self.age=age
        self.gender=gender
        self.mobile=mobile
        self.address=address
    
    def __repr__(self):
        return f"<User {self.name}>"
    @app.route('/', methods=['GET'])
    def users1():
        return  render_template('index.html')
    @app.route('/logn', methods=['GET'])
    def users2():
        return  render_template('logn.html')
    @app.route('/sgnup', methods=['GET'])
    def users3():
        return  render_template('sgnup.html')
   
                    

    
   
    @app.route('/product', methods=['GET'])
    def users5():
        return  render_template('product.html')
    @app.route('/cart',methods=['GET'])
    def users6():
        return render_template('cart.html')
    @app.route('/health', methods=['GET'])
    def users7():
        return  render_template('health.html')
    @app.route("/result" ,methods=['POST','GET'])
    def result():
        content=request.form.get("content")
        
        cont=None
        
        if content == 'Low fat products':
            dataset['fat_100g'].isin(range(0))
            low_fat=dataset.loc[dataset['fat_100g']==True]
            cont=low_fat.product_name.values.tolist()
        

            
        elif content == "Low sugar products":
            dataset['sugars_100g'].isin(range(0))
            low_sugar=dataset.loc[dataset['sugars_100g']==True]
            cont=low_sugar.product_name.values.tolist()
            
        elif content == "Low cabohydrates products":
            dataset['carbohydrates_100g'].isin(range(2000))
            low_carb=dataset.loc[dataset['carbohydrates_100g']==True]
            cont=low_carb.product_name.values.tolist()
            
        
        elif content == "Protein rich products":
            dataset['proteins_100g'].isin(range(90,100))
            protein_rich=dataset.loc[dataset['proteins_100g']==True]
            cont=protein_rich.product_name.values.tolist()
           
            
        elif content == "Low salt products":
            dataset['salt_100g'].isin(range(0,1))
            low_salt=dataset.loc[dataset['salt_100g']==True]
            
            cont=low_salt.product_name.values.tolist()
            
         
        elif content == "Energy rich products":
            dataset['energy_100g'].isin(range(1000))
            energy_boos=dataset.loc[dataset['energy_100g']==True]
            cont=energy_boos.product_name.values.tolist()
        
        return render_template("health.html",content = cont)
    @app.route('/users', methods=['POST', 'GET'])
    def handle_users():
        if request.method == 'POST':
                count=0
                uname=request.form.get("email")
                phno=request.form.get("people")
                print(uname,phno)
                for i in result:
                    if i[3]==uname or i[6]==phno:
                        count=1
                if count==1:
                    return render_template("sgnup.html")
                    
                else:
                    if request.form:
                        data = request.form
                        dbpass=data["phone"]+salt
                        hashed=hashlib.md5(dbpass.encode())
                        new_user = UsersModel(name=data['name'], password=hashed.hexdigest(),email=data['email'],age=data['date'],gender=data['time'],mobile=data['people'],address=data['message'])
                        db.session.add(new_user)
                        db.session.commit()
                        return render_template("logn.html")
                        
                    else:
                        return {"error": "No data passed in form."}

        elif request.method == 'GET':
            users = UsersModel.query.all()
            results = [
                {
                    "name": user.name
                } for user in users]

            return {"count": len(results), "users": results}
popular_df = pickle.load(open('popular_.pkl','rb'))
rating=popular_df['avg_ratings'].values

@app.route('/popularity')
def popularity():
    return render_template('popularity.html',
                           Item = list(popular_df['Title'].values),
                           des=list(popular_df['category'].values),
                           image=list(popular_df['image'].values),
                           ##votes=list(popular_df['num_ratings'].values),
                           rating=list(np.round(popular_df['avg_ratings'].values,2))
                           
                           
                           
                           
                           )
popular_df = pickle.load(open('popular_.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
items = pickle.load(open('item.pkl','rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl','rb'))
@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/user4',methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        item = []
        temp_df = items[items['Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Title')['Title'].values))
        item.extend(list(temp_df.drop_duplicates('Title')['category'].values))
        item.extend(list(temp_df.drop_duplicates('Title')['image'].values))
        data.append(item)

    print(data)

    return render_template('recommend.html',data=data)
@app.route('/search' ,methods=['POST','GET'])
def search():
    search=request.form.get("search")
    product=None
    price=None
    
    if search=="rice":
        product=df['Product'][0]
        price=df['price'][0]
        img=df['image'][0]

    elif search=="nutella":
        product=df['Product'][1]
        price=df['price'][1]
        img=df['image'][1]


        
    return render_template('home.html',search=product,price=price,img=img)

uname=None
class UsersModel2(db.Model):
    __tablename__ = 'cart'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    
    def __init__(self, name, item):
       
        self.name = name
        self.item=item
    def __repr__(self):
        return f"<User {self.name}>"
    @app.route('/users2', methods=['GET','POST'])
    def users4():
        if request.method== 'POST':
            cursor.execute('''SELECT * from users''')
            result=cursor.fetchall()
            uname=request.form.get("email")
            passw=request.form.get("phone")
            dbpass=passw+salt
            hashed=hashlib.md5(dbpass.encode())
            passw=hashed.hexdigest()
            
            
            print(uname,passw)
            for i in result:
                if i[3]==uname and i[2]==passw:
                    
                    return render_template('home.html')
    @app.route('/gohtml',methods=['GET'])
    def grows():
        return render_template('gohtml.html')
    @app.route('/cartst', methods=['GET'])
    def carts():
        return render_template('cart.html')
    
    
       
 
    
if __name__ == "__main__":
    app.run()
