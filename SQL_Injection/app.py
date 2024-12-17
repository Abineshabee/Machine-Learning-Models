import streamlit as st
import time
from MODEL import *

st.markdown(
    """
    <style>
    .big-button {
        width: 100%; /* Set the button to take full width */
        padding: 10px 20px; /* Adjust padding for a larger button */
        font-size: 18px; /* Increase the font size */
        background-color: #4CAF50; /* Optional: Change background color */
        color: white; /* Optional: Change text color */
        border: none; /* Optional: Remove border */
        border-radius: 8px; /* Optional: Add rounded corners */
        cursor: pointer;
    }

    .big-button:hover {
        background-color: #45a049; /* Optional: Change color on hover */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

USER_DATA_FILE = "users.txt"  # File to store user data

# Function to read users from a text file
def read_users_from_file():
    users = {}
    try:
        with open(USER_DATA_FILE, 'r') as file:
            for line in file:
                username, password = line.strip().split(',')
                users[username] = password
    except FileNotFoundError:
        # Create the file if it doesn't exist
        open(USER_DATA_FILE, 'w').close()
    return users

# Function to write a new user to the text file
def write_user_to_file(username, password):
    with open(USER_DATA_FILE, 'a') as file:
        file.write(f"{username},{password}\n")

# Function to display the login page
def login_page():
    st.title("Login Page")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    
    col1, col2 = st.columns([4,1])
    
    with col1:
        login_button = st.button(" &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Login &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;")
    
    with col2:
        register_button = st.button(" &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Register &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;")
    
    # Handle Login
    if login_button:
        users = read_users_from_file()
        if username in users and users[username] == password:
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.success(" Logged in successfully ")
            time.sleep(1)
            st.rerun()
        else:
            st.error("Invalid username or password.")
    
    # Handle Registration Redirect
    if register_button:
        st.session_state['page'] = 'register'
        st.rerun()

# Function to display the registration page
def register_page():
    st.title("Registration Page")
    
    username = st.text_input("Choose a Username")
    password = st.text_input("Choose a Password", type='password')
    confirm_password = st.text_input("Confirm Password", type='password')
    
    col1, col2 = st.columns([3,1])
    
    with col1:
        register_button = st.button(" &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Register &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;")
    
    with col2:
        login_redirect_button = st.button("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Back to Login &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;")
    
    # Handle Registration
    if register_button:
        # Add some basic validation
        if not username or not password:
            st.error("Username and password cannot be empty.")
        elif password != confirm_password:
            st.error("Passwords do not match.")
        else:
            users = read_users_from_file()
            if username in users:
                st.error("Username already exists. Please choose a different one.")
            else:
                write_user_to_file(username, password)
                st.success("Registration successful! Please log in.")
                st.session_state['page'] = 'login'
                st.rerun()
    
    # Handle Login Redirect
    if login_redirect_button:
        st.session_state['page'] = 'login'
        st.rerun()

# Function to display the dashboard
def load_dashboard():
    st.title(f"Welcome! {st.session_state.get('username', 'User')}")
    st.title("Robust SQL Injection Detection Model ✧")
    st.write("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  This application detects potential SQL injection attacks in SQL queries by analyzing patterns and behaviors associated with malicious inputs. It helps prevent unauthorized access and protects databases from data breaches.")
    
    sql_query = st.text_area("Enter the SQL query below &nbsp;&nbsp; : ")
    
    if st.button("Detect"):
    
        if sql_query.strip():
            st.subheader("Prediction Result  ")
            model_instance = Model()
            sample_input = [ sql_query ]
            prediction = model_instance.predict(sample_input)
            prediction_proba = model_instance.predict_proba(sample_input)

            st.info(f"Model  ✧ Prediction for the Query    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  : &nbsp;&nbsp; {prediction[0]}")
            st.info(f"Prediction Probability of Class [ 0 ]  &nbsp;&nbsp;&nbsp;  : &nbsp;&nbsp;  { round( prediction_proba[0][0] * 100 , 2 ) } % ")
            st.info(f"Prediction Probability of Class [ 1 ]  &nbsp;&nbsp;&nbsp;  : &nbsp;&nbsp;  { round( prediction_proba[0][1] * 100 , 2 ) } % ")
    
            st.subheader("SQL Injection Result ")
       
            if prediction[0] == 1:
                st.warning(f"The presence of SQL injection has been evaluated and determined to be &nbsp;&nbsp;&nbsp;  ** True **")
            else:
                st.success(f"The presence of SQL injection has been evaluated and determined to be &nbsp;&nbsp;&nbsp;  ** False **")
    
        else:
             st.error("Please enter a valid SQL query!")
    
    if st.button("Log Out"):
        # Clear the session state
        st.session_state['logged_in'] = False
        st.session_state['username'] = None
        st.session_state['page'] = 'login'
        st.rerun()

# Main app logic
def main():
    # Initialize session state if not already set
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    
    if 'page' not in st.session_state:
        st.session_state['page'] = 'login'
    
    # Routing logic
    if st.session_state['logged_in']:
        load_dashboard()
    elif st.session_state['page'] == 'register':
        register_page()
    else:
        login_page()

# Run the main application
if __name__ == "__main__":
    main()

