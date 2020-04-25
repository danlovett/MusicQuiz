### START OF LOGIN/REGISTER ###

#Importing linecache from modules ('time' module later for code delays)
import linecache
import os

# Setting the variables
catchLineLogin = 1
welcomeRetry = 0
attemptsMade = 0
attemptsRemain = 3
userName = False
firstName = False
lastName = False
userNameCheck = False
password = False
passwordCheck = False
redirect = False

### FUNCTIONS ###

#REDIRECT (User Feedback)
def redirectReason(userName, redirect):
    if redirect == 'data_load_missing':
        print("Data missing from File.\n--> Registration")
        registration(userName, redirect)
    elif redirect == 'username_load_error':
        print("--> Registration")
        registration(userName, redirect)
    elif redirect == 'from_missing_reload':
        print("Data has been saved in the file, under the username '" + userName + "'. You must restart to continue")
        input("Press ENTER")
        os.system('cls' if os.name == 'nt' else 'clear')
        exit()

    elif redirectReason == 'user_redirect_admin':
        print("Exiting")
        exit()

    elif redirectReason == 'password_load_error':
        print("Attempt limit reached - Exiting")
        exit()
        
def attemptsRemainCheck(userName, count, catchLineLogin, redirect, presentUserNameIn, attemptsRemain, attemptsMade, eventLogger):

    attemptsRemain = 3 - attemptsMade

    if attemptsRemain == 1:
        attemptsWord = ' attempt '
    else:
        attemptsWord = ' attempts '

    if attemptsRemain > 0 and eventLogger == 'user_redirect_main':
        print("'" + userName + "' user not found. You have " + str(attemptsRemain) + attemptsWord + "remaining before being directed to the register page")
        presentUserNameIn = True  
    elif attemptsRemain == 0 and eventLogger == 'user_redirect_main':
        redirectReason(userName, redirect = 'username_load_error')

    elif attemptsRemain > 0 and eventLogger == 'user_redirect_admin':
        print("You cannot have 'admin' in your username, you have " + str(attemptsRemain) + attemptsWord + "remaining before you're forced to exit")
    elif attemptsRemain == 0 and eventLogger == 'user_redirect_admin':
        redirectReason(userName, redirect = 'user_redirect_admin')


    elif attemptsRemain > 0 and eventLogger == 'password_load_error':
        print("Worng Password. You have " + str(attemptsRemain) + attemptsWord + "remaining")
    elif attemptsRemain == 0 and eventLogger == 'password_load_error':
        redirectReason(userName, redirect = 'password_load_error')

#Registration
def registration(userName, redirect):

    count = 0

    with open('Auth/Inc/Login.txt', 'r') as f:
        for line in f:
            count += 1

    userAccept = False
    login = False

    firstName = input("What is your first name?\nFirst Name: ").capitalize()
    lastName = input("What is your last name?\nLast Name: ").capitalize()

    print("Your username must have:\n  - At least 4 characters\n  - No spaces")

    catchLineLogin = 1

    presentUserNameIn = True
    
    while userAccept == False:
        
        if presentUserNameIn == True:
            userName = input("Username: ").lower()

        if len(userName) < 4:
            print("'" + userName + "' was not long enough\nTry again")
            presentUserNameIn = True
        elif ' ' in userName:
            print("'" + userName + "' contains a space.\nTry again")
            presentUserNameIn = True
        elif ' ' in userName and len(userName) < 4:
            print("'" + userName + "' was not long enough and a space was present\nTry again")
            presentUserNameIn = True
        else:
            login = False

            fileInfo = linecache.getline('Auth/Inc/Login.txt', catchLineLogin)
            dataBlock = fileInfo.split(',')

            if (dataBlock[0] == userName and count == catchLineLogin) or (userName == dataBlock[0] and count != catchLineLogin):
                print("Username already taken, try a different one")
                userAccept = False
                presentUserNameIn = True

            elif (dataBlock [0] != userName and count == catchLineLogin) or (count == 0):
                print("Username Accepted")
                userAccept = True

            else:
                catchLineLogin = catchLineLogin + 1
                presentUserNameIn = False

    print("Your password must have:\n  - At least 8 (eight) characters\n  - Contain AT LEAST 1 upper character")

    while login == False:

        password = input("Password: ")

        if len(password) < 8:
            print("-->The Password was not long enough. (" + str(len(password)) + " characters)\nTry again")
            continue
        elif ' ' in password:
            print("-->The Password contains a space\nTry again")
            continue
        elif not any(x.isupper() for x in password):
            print("-->The password contains no upper cases\nTry again")
            continue
        elif not any(x.isdigit() for x in password):
            print("-->The password contains no numbers\nTry again")
            continue
        else:
            print("Success!")
            writingLogin = open('Auth/Inc/Login.txt', 'a')
            writingLogin.write(userName + "," + password + "," + firstName + "," + lastName + ",account\n")
            writingLogin.close()
            redirect = 'data_load_missing'
            break

    if redirect == 'username_load_error' or redirect == 'data_load_missing':
        redirectReason(userName, redirect = 'from_missing_reload')

#Login
def login(userName, password, userNameCheck, passwordCheck, redirect, attemptsRemain, attemptsMade):

    catchLineLogin = 1
    count = 0

    try:
        with open('Auth/Inc/Login.txt', 'r') as f:
            for line in f:
                count += 1
        if count == 0:
            redirectReason(userName, redirect = 'data_load_missing')
    except IOError:
        file = open('Auth/Inc/Login.txt', 'w+')
        file.close()
        redirectReason(userName, redirect= 'from_missing_reload')

    infoFile = linecache.getline('Auth/Inc/Login.txt', catchLineLogin)
    dataBlock = infoFile.split(',')

    presentUserNameIn = True

    while userNameCheck == False:

        userContinue = True

        if presentUserNameIn == True:
            userName = input("Username: ").lower()

        if userName == 'admin' or userName == 'admin1':
            print("That is an administrative account. Cannot be used.\nTry again using a different username")
            userContinue = False
            attemptsMade = attemptsMade + 1
            attemptsRemainCheck(userName, count, catchLineLogin, redirect, presentUserNameIn, attemptsRemain, attemptsMade, eventLogger= 'user_redirect_admin')

        infoFile = linecache.getline('Auth/Inc/Login.txt', catchLineLogin)
        dataBlock = infoFile.split(',')
        if userContinue == True:
            if (dataBlock[0] == userName and count == catchLineLogin) or (userName == dataBlock[0]):
                userNameCheck = True
            elif dataBlock[0] != userName:
                if count == catchLineLogin:
                    attemptsMade = attemptsMade + 1
                    attemptsRemainCheck(userName, count, catchLineLogin, redirect, presentUserNameIn, attemptsRemain, attemptsMade, eventLogger= 'user_redirect_main')
                catchLineLogin = catchLineLogin + 1
                presentUserNameIn = False
            else:
                catchLineLogin = catchLineLogin + 1
                presentUserNameIn = False

    while passwordCheck == False:

        infoFile = linecache.getline('Auth/Inc/Login.txt', catchLineLogin)
        dataBlock = infoFile.split(',')

        firstName = dataBlock[2]
        lastName = dataBlock[3]

        password = input("Password: ")

        if dataBlock[1] == password:
            print("Hello " + firstName)

            file = open('Auth/Inc/UserActive.txt', 'w')
            file.write(userName + ',' + firstName + ',' + lastName)
            file.close()
            passwordCheck = True
        elif dataBlock[1] != password:
            passwordCheck = False
            attemptsMade = attemptsMade + 1
            attemptsRemainCheck(userName, count, catchLineLogin, redirect, presentUserNameIn, attemptsRemain, attemptsMade, eventLogger= 'password_load_error')
            if attemptsMade == 3:
                print("Attempt limit reached - Exiting")
                exit()

### END OF FUNCTIONS ###

### ACCESSING FUNCTIONS/PROGRAM ###
while True:
    welcome = input("Login/Register (Type Either 'Register' or 'Login'): ").capitalize()
    if welcome == "Login":
        login(userName, password, userNameCheck, passwordCheck, redirect, attemptsRemain, attemptsMade)
        break
    elif welcome == "Register":
        registration(userName, redirect)
        break
    elif welcome == 'Push_to_github':
        file1 = open("Auth/Inc/Login.txt", "r+")
        file2 = open("Auth/Inc/UserActive.txt", "r+")
        file1.truncate(0)
        file2.truncate(0)
        file1.close()
        file2.close()
        exit()
    elif welcomeRetry == 3:
        print("Exit and try again")
        exit()
    else:
        print("Error\nTry again")
        welcomeRetry = welcomeRetry + 1
        continue

### END OF ACCESSING FUNCTIONS ###

### END OF LOGIN/REGISTER ###