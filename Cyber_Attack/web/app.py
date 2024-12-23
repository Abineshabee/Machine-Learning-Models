from flask import Flask, render_template, request, redirect, url_for, flash
from MODEL import *
import users

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flash messages


@app.route('/')
@app.route('/login')
def home():
    return render_template('login.html')
    

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    print("\nUser Name : " , username )
    print("\nPassword  : " , password )
    
    user_login = users.user_login( username , password )
    
    if (  user_login == True ) :
        users.put_currentuser( username )
        return render_template('index.html', username=username)
    else:
        error_message = 'Invalid username or password. Please try again.'
        return render_template('login.html', error=error_message)




@app.route('/register')
def return_register() :
    print("\n RETURN REGISTER \n")
    return render_template('register.html')
    
    
    
@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    
    print("\nUser Name : " , username )
    print("\nPassword  : " , password )
    
    user_register = users.user_register( username , password )
    
    if (  user_register == True ) :
        users.put_currentuser( username )
        return render_template('index.html', username=username)
        
    else:
        error_message = 'Username Already Exists , Please try again.'
        return render_template('register.html' , error=error_message)
        
        
     
@app.route( '/index' , methods=['POST'])
def index() :
    sql_query = request.form['query']
    
    print("\nUSER      : " , users.get_currentuser(  ) )
    print("\nSQL Query : " , sql_query )
    
    print("\nPrediction Result  ")
    model_instance = Model()
    sample_input = [ sql_query ]
    prediction = model_instance.predict(sample_input)
    prediction_proba = model_instance.predict_proba(sample_input)
    print(f"Model Prediction for the Query           :   { prediction[0] }")
    print(f"Prediction Probability of Class [ 0 ]    :  { round( prediction_proba[0][0] * 100 , 2 ) } % ")
    print(f"Prediction Probability of Class [ 1 ]    :  { round( prediction_proba[0][1] * 100 , 2 ) } % ")
    
    print("\n SQL Injection Result\n")
       
    if prediction[0] == 1:
         print(f"\nThe presence of SQL injection has been evaluated and determined to be  ** True **\n")
         mr = "The presence of SQL injection has been evaluated and determined to be  ** True **"
         sqli = "True"
    else:
         print(f"\nThe presence of SQL injection has been evaluated and determined to be  ** False **\n")
         mr = "The presence of SQL injection has been evaluated and determined to be  ** False **"
         sqli = "False"
         
    username  =  users.get_currentuser(  )
    pred    =  prediction[0]
    ppc0      =  str ( round( prediction_proba[0][0] * 100 , 2 ) ) + " % "
    ppc1      =  str ( round( prediction_proba[0][1] * 100 , 2 ) ) + " % "
        
    

    return render_template('index.html' , username = username ,  result = True , pred = pred , ppc0 = ppc0 , ppc1 = ppc1 , mr = mr , sqli = sqli )

if __name__ == '__main__':
    app.run(debug=True)

