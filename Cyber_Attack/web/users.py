
def user_register( username , password ) :

   
    with open("users.txt", "r") as file:
        users = file.readlines()
    
    # Check if the username is already exists
    for user in users:
        stored_username, stored_password = user.strip().split(",")
        if stored_username == username :
            print("\nUser Name Already Exists")
            return False
    
    with open("users.txt", "a") as file:
        file.write(f"{username},{password}\n")
    print("Registration successful!")
    
    return True


def user_login( username , password ) :
    
    # Read users from the users.txt file
    with open("users.txt", "r") as file:
        users = file.readlines()
    
    # Check if the username and password match
    for user in users:
        stored_username, stored_password = user.strip().split(",")
        if stored_username == username and stored_password == password:
            print("Login successful!")
            return True
    print("Invalid username or password!")
    return False
    
def put_currentuser( username ) :
    with open("currentuser.txt", "w") as file:
        file.write(username)
        
def get_currentuser( ) :
    with open("currentuser.txt", "r") as file:
        currentuser = file.read()
    return currentuser
    


