from flask import Flask, render_template, redirect, request, flash
from mysqlconnection import connectToMySQL
import re

app = Flask('__name__')
app.secret_key = "development_key"

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register_email", methods=['POST'])
def validate_email():
    print(request.form['emailAddress'])
    if not EMAIL_REGEX.match(request.form['emailAddress']):
        flash("Email is not valid")
        return redirect("/")
    else:
        check_mysql = connectToMySQL('flask_pets')
        check_query = "SELECT * FROM email_address WHERE email like %(email)s"
        check_data = {
            "email": request.form['emailAddress']
        }
        ls = check_mysql.query_db(check_query, check_data)
        print(ls)
        if ls:
            flash("Email already exist")
            return redirect("/")
        else:
            mysql = connectToMySQL('flask_pets')
            query = "INSERT INTO email_address(email, created_at) VALUES(%(email)s, NOW())"
            data = {
                "email": request.form['emailAddress']
            }
            mysql.query_db(query, data)
            flash("The email address you entered " + request.form['emailAddress'] + " is a valid email address! Thank you!")
            return redirect("/success")
    
@app.route("/success")
def success():
    mysql = connectToMySQL('flask_pets')
    query = "SELECT * FROM email_address"
    emailList = mysql.query_db(query)
    return render_template("/success.html", emailList=emailList)

@app.route("/delete/<id>")
def delete(id):
    delete_mysql = connectToMySQL('flask_pets')
    delete_query = "DELETE FROM email_address WHERE id = %(id)s"
    delete_data = {
        "id": id
    }
    delete_mysql.query_db(delete_query, delete_data)

    mysql = connectToMySQL('flask_pets')
    query = "SELECT * FROM email_address"
    emailList = mysql.query_db(query)
    return render_template("/success.html", emailList=emailList)

if __name__ == '__main__':
    app.run(debug=True)