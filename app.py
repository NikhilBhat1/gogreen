from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask, request, render_template
import psycopg2
import hashlib
import pandas as pd
import pickle
import numpy as np




df=pd.read_csv('search.csv')

salt="#j@nu$w&"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://stgculhhzfqsnp:7b2285e352bee51479a4bc6dd01073794c5cc3270b18cb7dbfcf80b2427683ed@ec2-3-220-207-90.compute-1.amazonaws.com:5432/d96v1v718pbl7i"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
DATABASE_URL="postgres://stgculhhzfqsnp:7b2285e352bee51479a4bc6dd01073794c5cc3270b18cb7dbfcf80b2427683ed@ec2-3-220-207-90.compute-1.amazonaws.com:5432/d96v1v718pbl7i"
db = SQLAlchemy(app)
migrate = Migrate(app, db)
conn=psycopg2.connect(DATABASE_URL, sslmode='receive')
conn.autocommit = True
cursor=conn.cursor()



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


class CartModel(db.Model):
    __tablename__ = 'carts'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String())
    item = db.Column(db.String())
    image = db.Column(db.String())
    price=db.Column(db.Integer)
    
    
    
    def __init__(self, email, item, image,price):
        self.email = email
        self.item=item
        self.image = image
        self.price=price
        


@app.route('/', methods=['GET'])
def index():
    return  render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return  render_template('login.html')
    elif request.method == 'POST':
        global uname
        if request.method== 'POST':
            cursor.execute('''SELECT * from users''')
            result=cursor.fetchall()
            uname=request.form.get("email")
            passw=request.form.get("phone")
            dbpass=passw+salt
            hashed=hashlib.md5(dbpass.encode())
            passw=hashed.hexdigest()
            te=0
            
          
            for i in result:
                
                if i[3]==uname and i[2]==passw:
                    te=1
                    print(te)
            cursor.execute('SELECT * from test')
            result=cursor.fetchall()
             
            if te==1:
                return render_template('home.html',length1=int(len(result)/2),length2=len(result),result = result)
            else:
                return render_template('login.html')
        else:
            print("error")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return  render_template('signup.html')
    elif request.method == 'POST':
        cursor.execute('''SELECT * from users''')
        result=cursor.fetchall()
        count=0
        uname=request.form.get("email")
        phno=request.form.get("people")
        print(uname,phno)
        for i in result:
            if i[3]==uname or i[6]==phno:
                count=1
        if count==1:
            return render_template("signup.html")
            
        else:
            if request.form:
                data = request.form
                dbpass=data["phone"]+salt
                hashed=hashlib.md5(dbpass.encode())
                new_user = UsersModel(name=data['name'], password=hashed.hexdigest(),email=data['email'],age=data['date'],gender=data['time'],mobile=data['people'],address=data['message'])
                db.session.add(new_user)
                db.session.commit()
                return render_template("login.html")
            else:
                return {"error": "No data passed in form."}
       
@app.route('/product', methods=['GET'])
def product():
    cursor.execute('SELECT * from test')
    result=cursor.fetchall()
    
    return render_template("product.html", length1=int(len(result)/2),length2=len(result),result = result)
    

@app.route('/cart',methods=['GET'])
def cart():
    cursor.execute('SELECT * from carts where email=%s',[uname])
    result=cursor.fetchall()
    tp=0
    for i in range(0,len(result)):
        tp=tp+result[i][4]
    return render_template('cart.html',result=result,length=len(result),tp=tp)



@app.route('/grow',methods=['GET'])
def grow():
    cursor.execute('SELECT * from carts where email=%s',[uname])
    result=cursor.fetchall()
    
    return render_template('grow.html',result=result,length=len(result))



@app.route('/health', methods=['GET', 'POST'])
def health():
    if request.method == 'GET':
        return render_template('health.html')
    elif request.method == 'POST':
        dataset = pd.read_csv('nutrition.csv')
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
        
        return render_template("health.html", content = cont)

       
@app.route('/popularity')
def popularity():
    popular_df = pickle.load(open('popular_.pkl','rb'))
    return render_template('popularity.html',
                           Item = list(popular_df['Title'].values),
                           des=list(popular_df['category'].values),
                           image=list(popular_df['image'].values),
                           ##votes=list(popular_df['num_ratings'].values),
                           rating=list(np.round(popular_df['avg_ratings'].values,2)))
        
    

@app.route('/recommend', methods=['GET', 'POST'])
def recommend_ui():
    if request.method == 'GET':
        return render_template('recommend.html')
    elif request.method == 'POST':
        pt = pickle.load(open('pt.pkl','rb'))
        items = pickle.load(open('item.pkl','rb'))
        similarity_scores = pickle.load(open('similarity_scores.pkl','rb'))
        user_input = request.form.get('user_input').strip()
        index = [ id for id, item in enumerate(list(pt.index)) if user_input.lower() in item.lower() ][0]
        similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]


        data = [] 
        for i in similar_items:
            item = []
            temp_df = items[items['Title'] == pt.index[i[0]]]
            item.extend(list(temp_df.drop_duplicates('Title')['Title'].values))
            item.extend(list(temp_df.drop_duplicates('Title')['category'].values))
            item.extend(list(temp_df.drop_duplicates('Title')['image'].values))
            data.append(item)

        return render_template('recommend.html',data=data)


@app.route('/search' ,methods=['POST','GET'])
def search():
    search=request.form.get("search")
    product=None
    price=None
    cursor.execute('SELECT * from test')
    result=cursor.fetchall()

    index = [ id for id, prod in enumerate(list(df['Product'])) if search.lower() in prod.lower()][0]

    product = df['Product'][index]
    price = df['price'][index]
    img = df['image'][index]
        
    return render_template('home.html', search=product,price=price,img=img,length1=int(len(result)/2),length2=len(result),result = result)

@app.route('/gohtml',methods=['GET'])
def grows():
    return render_template('gohtml.html')


@app.route('/checkout', methods=['GET'])
def carts():

    item = request.args.get('item')
    image = request.args.get('image')
    price=request.args.get('price')
    print(price)
   
    cursor.execute('SELECT item from carts WHERE email=%s',[uname])
    result=cursor.fetchall()
   
    
    
    
    if ( item != None ): 
        global count2
        count2=0
        print(len(result))
       
        for i in range(0,len(result)):
            print(result[i][0])
            
            if item==result[i][0]:
               
                count2=1
                break        
        if count2==1:
            print("exists")
        else:
        
            
            new_user = CartModel(email=uname, item=item, image=image,price=price)
            db.session.add(new_user)
            db.session.commit()
    global result2
    cursor.execute('SELECT * from carts WHERE email= %s', [uname])
    result2=cursor.fetchall()
    
    tp=0
    for i in range(0,len(result2)):
        tp=tp+result2[i][4]

    return render_template("cart.html", length=len(result2), result = result2,tp=tp)



@app.route('/dropitems', methods=['GET'])
def dropitems():
    item = request.args.get('item')
    
    
    
   
    cursor.execute('DELETE from carts * WHERE item=%s',[item])
    cursor.execute('SELECT * from carts WHERE email=%s',[uname])
    result=cursor.fetchall()
    tp=0
    for i in range(0,len(result)):
        tp=tp+result[i][4]

    
    return render_template("cart.html", length=len(result), result = result,tp=tp)
@app.route('/home',methods=['GET'])
def home():
    cursor.execute('SELECT * from test')
    result=cursor.fetchall()
    return render_template('home.html',length1=int(len(result)/2),length2=len(result),result = result)



if __name__ == "__main__":
    app.run(debug=True) 
