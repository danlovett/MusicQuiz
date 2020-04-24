#Importing time and linecache from modules
import time
import linecache

# Setting the variables
catchLineLogin = 1

userName = False
password = False
redirect = False
welcomeRetry = 0

def directRegister(userName, redirect):
    print("The Account with the username '" + userName + "' was not found\n--> Registration")
    registration(userName, redirect)

def redirectReason(redirect):
    if redirect == 'data_load_missing':
        print("You was redirected as the data from the login file was missing/corrupt.\nYou must register to continue")
    elif redirect == 'username_load_error':
        print("--> Registration")
    elif redirect == 'from_missing_reload':
        print("You was redirected as the data from the login file was missing/corrupt.\nYou must restart to continue")
        exit()
    else:
        pass

def login(userName, password, userNameCheck, passwordCheck, passwordFailCounter = 0, userFailCounter = 0, firstTime = True):

    catchLineLogin = 1
    count = 0

    with open('Auth/Inc/Login.txt', 'r') as f:
        for line in f:
            count += 1

    infoFile = linecache.getline('Auth/Inc/Login.txt', catchLineLogin)
    dataBlock = infoFile.split(',')

    while userNameCheck == False:
        userName = input("Username: ")

        infoFile = linecache.getline('Auth/Inc/Login.txt', catchLineLogin)
        dataBlock = infoFile.split(',')
        
        if (dataBlock[0] == userName and count == catchLineLogin) or (userName == dataBlock[0]):
            userNameCheck = True
        elif (dataBlock[0] != userName and count == catchLineLogin) or (dataBlock[0] != userName):
            userFailCounter = userFailCounter + 1 
            userAttempsRemains = 3 - userFailCounter
            if catchLineLogin == count:
                if userFailCounter < 3:
                    print(userName + " user not found. You have " + str(userAttempsRemains) + " attempts remaining before being directed to the register page")
                
                elif userFailCounter == 3:
                    directRegister(userName, redirect = "username_load_error")
                    userNameCheck = True
        
        else:
            catchLineLogin = catchLineLogin + 1
            continue

    while passwordCheck == False:

        infoFile = linecache.getline('Auth/Inc/Login.txt', catchLineLogin)
        dataBlock = infoFile.split(',')

        password = input("Password: ")

        if dataBlock[1] == password:
            print("Hello " + dataBlock[2])
            break
        elif dataBlock[1] != password:
            passwordFailCounter = passwordFailCounter + 1
            passwordAttempsRemain = 3 - passwordFailCounter
            passwordCheck = False

            print("Worng Password. You have " + str(passwordAttempsRemain) + " attemps remaining")

            if passwordFailCounter == 3:
                print("You have failed to log in.\nRestart the program and try again")
                exit()
    
#REGISTRATION
def registration(userName, redirect):

    count = 0

    with open('Auth/Inc/Login.txt', 'r') as f:
        for line in f:
            count += 1

    userAccept = False
    login = False

    firstName = input("What is your first name?\nFirst Name: ").capitalize()
    lastName = input("What is your last name?\nLast Name: ").capitalize()
    
    while userAccept == False:
        userName = input("Your username must have:\n  - At least 4 characters\n  - No spaces\nUsername: ").lower()
        if len(userName) < 4:
            print("Error\nThe username was not long enough\nTry again")
            continue
        elif ' ' in userName:
            print("Error\nThe username contains a space.\nTry again")
            continue
        elif ' ' in userName and len(userName) < 4:
            print("Error\nThe username was not long enough and a space was present\nTry again")
            continue
        else:
            catchLineLogin = 1
            login = False

            fileInfo = linecache.getline('Auth/Inc/Login.txt', catchLineLogin)
            dataBlock = fileInfo.split(',')

            if (dataBlock[0] == userName and count == catchLineLogin) or (userName == dataBlock[0]):
                print("Username already taken, try a different one")
                userAccept = False

            elif (dataBlock [0] != userName and count == catchLineLogin) or (count == 0):
                print("Username Accepted")

                userAccept = True

            else:
                catchLineLogin = catchLineLogin + 1
                continue

    while login == False:
        password = input("Your password must have:\n  - At least 8 (eight) characters\n  - Contain AT LEAST 1 upper character\nPassword: ")

        if len(password) < 8:
            print("Error\nThe username was not long enough\nTry again")
            continue
        elif ' ' in password:
            print("Error\nThe username contains (a) space[s]\nTry again")
            continue
        elif not any(x.isupper() for x in password):
            print("Error\nThe password contains no upper cases\nTry again")
            continue
        elif not any(x.isdigit() for x in password):
            print("Error\nThe password contains no numbers\nTry again")
            continue
        else:
            print("Success!")
            break

    writingLogin = open('Auth/Inc/Login.txt', 'a')
    writingLogin.write(userName + "," + password + "," + firstName + "," + lastName + ",account\n")
    writingLogin.close()

    if redirect == 'username_load_error' or redirect == 'data_load_missing':
        redirectReason(redirect = 'from_missing_reload')

### END OF FUNCTIONS ###

### ACCESSING FUNCTIONS ###
while True:
    welcome = input("Login/Register (Type Either 'Register' or 'Login'): ").capitalize()
    if welcome == "Login":
        login(userName, password, userNameCheck = False, passwordCheck = False)
        break
    elif welcome == "Register":
        registration(userName, redirect)
        break
    elif welcomeRetry == 3:
        print("Exit and try again")
        exit()
    else:
        print("Error\nTry again")
        welcomeRetry = welcomeRetry + 1
        continue