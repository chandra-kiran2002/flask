from flask import Flask,redirect,render_template,request,url_for,flash,jsonify
import json
import ssl
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.inspection import inspect
from flask_mail import Mail, Message






local_server= True
app = Flask(__name__)
app.secret_key="^%$^$^^*&&FGGY9178"
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'dummy.python10@gmail.com'
app.config['MAIL_PASSWORD'] = 'tbkqmfolwjmjwnfk'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

# database configuration
# app.config['SQLALCHEMY_DATABASE_URI']='mysql://username:password@localhost/databasename'
app.config['SQLALCHEMY_DATABASE_URI']='mysql://uxqj2d1bk0mzw7e2:uQJMGfBd7eKprmCBQKHB@boohiq8z5datxmfqy0zy-mysql.services.clever-cloud.com:3306/boohiq8z5datxmfqy0zy'
db=SQLAlchemy(app)

# configuration of database tables
class Test(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(15))


# serialization
class Serializer(object):

    def serialize(self):
        return {c:getattr(self,c) for c in inspect(self).attrs.keys()}

    
    @staticmethod
    def serialize_list(obj):
        return [i.serialize() for i in obj]




class Products(db.Model,Serializer):
    pid=db.Column(db.Integer,primary_key=True)
    productName=db.Column(db.String(50))
    productDescription=db.Column(db.String(100))
    rating=db.Column(db.Integer)
    stocks=db.Column(db.Integer)
    price=db.Column(db.Integer)



@app.route("/test/")
def test():
    try:
        # query=Test.query.all()
        # print(query)
        sql_query="Select * from test"
        with db.engine.begin() as conn:
            response=conn.exec_driver_sql(sql_query).all()
            print(response)
        return f"Database is connected"

    except Exception as e:
        return f"Database is not connected {e} "


@app.route("/")
def home():
    try:
        products=Products.query.all()
        return render_template("index.html",products=products)
    except Exception as e:
        return f"Database is not connected {e} "
    

# create operation
@app.route("/create",methods=['GET','POST'])
def create():
    if request.method=="POST":
        pName=request.form.get('productname')
        pDesc=request.form.get('productDesc')
        pRating=request.form.get('rating')
        pStocks=request.form.get('stocks')
        pPrice=request.form.get('price')
        # query=Products(productName=pName,productDescription=pDesc,rating=pRating,stocks=pStocks,price=pPrice)
        # db.session.add(query)
        # db.session.commit()
        sql_query=f"INSERT INTO `products` (`productName`, `productDescription`, `rating`, `stocks`, `price`) VALUES ('{pName}', '{pDesc}', '{pRating}', '{pStocks}', '{pPrice}')"
        with db.engine.begin() as conn:
            conn.exec_driver_sql(sql_query)
            flash("Product is Added Successfully","success")
            return redirect(url_for('home'))
        


    return render_template("index.html")

# update operation
@app.route("/update/<int:id>",methods=['GET','POST'])
def update(id):
    product=Products.query.filter_by(pid=id).first()
    if request.method=="POST":
        pName=request.form.get('productname')
        pDesc=request.form.get('productDesc')
        pRating=request.form.get('rating')
        pStocks=request.form.get('stocks')
        pPrice=request.form.get('price')
        # query=Products(productName=pName,productDescription=pDesc,rating=pRating,stocks=pStocks,price=pPrice)
        # db.session.add(query)
        # db.session.commit()
        sql_query=f"UPDATE `products` SET `productName`='{pName}',`productDescription`='{pDesc}',`rating`='{pRating}',`stocks`='{pStocks}',`price`='{pPrice}' WHERE `pid`='{id}'"
       
        with db.engine.begin() as conn:
            conn.exec_driver_sql(sql_query)
            flash("Product is Updated Successfully","primary")
            return redirect(url_for('home'))


    return render_template("edit.html",product=product)



# delete operation
@app.route("/delete/<int:id>",methods=['GET'])
def delete(id):
    # print(id)
    query=f"DELETE FROM `products` WHERE `pid`={id}"
    with db.engine.begin() as conn:
        conn.exec_driver_sql(query)
        flash("Product Deleted Successfully","danger")
        return redirect(url_for('home'))


#flask apis
@app.route("/api/users",methods=['GET'])
def users():
    usersdata={
        "username":"anees",
        "salary":26000,
        "role":"Developer",
        "isActive":True
    }

    # return json.dumps(usersdata)
    return jsonify(usersdata)


@app.route("/api/products",methods=['GET'])
def apiproducts():
    data=Products.query.all()
    print(type(data))
    print(type(data[0]))
    return jsonify(Products.serialize_list(data))


@app.route("/api/product/<int:id>",methods=['GET'])
def apiproduct(id):
    data=Products.query.get(id)
    return jsonify(Products.serialize(data))

@app.route('/search', methods = ['POST',"GET"])
def search():
    if request.method == 'POST':
        text = request.form.get('searchtext')
        print(text)
        if text.isdigit():
            sql_query=f'SELECT * FROM `products` WHERE `pid`= {int(text)}'
            with db.engine.begin() as conn:
                response=conn.exec_driver_sql(sql_query).all()
                print(response)
                if len(response) == 0:
                    flash('No product found','info')
                    return redirect(url_for('home'))
                else:
                    return render_template('index.html', products = response)
        else:
            sql_query = 'SELECT * FROM products WHERE productName LIKE "'+text+'"'
            with db.engine.begin() as conn:
                print(sql_query)
                response = conn.exec_driver_sql(sql_query).all()
                print(response)
                if len(response) == 0:
                    flash('No product found','info')
                    return redirect(url_for('home'))
                else:
                    return render_template('index.html', products = response)


    return redirect(url_for('home'))

@app.route('/contact', methods = ['GET','POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        number = request.form.get('number')
        query = request.form.get('query')
        message = Message('Hello from Flask!',
                     sender= 'dummy.python10@gmail.com',recipients=[email])
        message.body = 'This is a test email sent from Flask!'
        try:
            mail.send(message)
            flash("Mail sent successfully",'success')
            return redirect(url_for('home'))
        except Exception as e:
            print(e)


    return render_template('contact.html')
@app.route('/mail')
def send_mail():
    msg = Message('Hello', sender = 'dummy.python0@gmail.com', recipients = ['dummy.python0@gmail.com'])
    msg.body = "This is the email body"
    mail.send(msg)
    return "Sent"


if __name__=="__main__":
    app.run(debug=True)
