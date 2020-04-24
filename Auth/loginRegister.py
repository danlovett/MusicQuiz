### START OF LOGIN/REGISTER ###

#Importing linecache from modules ('time' module later for code delays)
import linecache

# Setting the variables
catchLineLogin = 1
welcomeRetry = 0
userName = False
password = False
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
        exit()
    else:
        pass

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
            redirect = 'from_missing_reload'
            break

    if redirect == 'username_load_error' or redirect == 'data_load_missing':
        redirectReason(userName, redirect = 'from_missing_reload')

#Login
def login(userName, password, userNameCheck, passwordCheck, passwordFailCounter = 0, userFailCounter = 0, firstTime = True):

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
                    redirectReason(userName, redirect = "username_load_error")
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

### END OF FUNCTIONS ###

### ACCESSING FUNCTIONS/PROGRAM ###
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

### END OF ACCESSING FUNCTIONS ###

### END OF LOGIN/REGISTER ###