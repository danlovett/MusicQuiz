### FOR FUTURE: use userID for better auth ###

import linecache, time, os, sys
sys.path.insert(1, 'App/game')

userAttempts = 0
currentLine = 1

rFeedbackLoop = ''
rDetailed = ''

class User:
    # Handling Getting file contents | computing userAttempts made

    def fileDataRetrieve(self, redirectMsg):
        global file_name, file_userName, file_password, currentLine
        
        if redirectMsg == 'append_line':
            currentLine += 1
        elif redirectMsg == 'reset_line':
            currentLine = 1

        if os.path.isfile('Auth/Inc/login.txt') and os.access('Auth/Inc/login.txt', os.R_OK):
            contents = linecache.getline('Auth/Inc/login.txt', currentLine)
            dataBlock = contents.split('|')
            file_name = dataBlock[0]
            file_userName = dataBlock[1]
            file_password = dataBlock[2]

            linecache.clearcache()

    def stateCurrentUser(self, name, userName):
        with open('Auth/Inc/currentUser.txt', 'w') as f:
            f.write(f'{name}|{userName}|')
            f.close()
            print('Enjoy the game!')

    def displayData(self, userPath):
        global name, userName, password
        if userPath == 'user_register':
            print('Registration:\n' + '-'*35 )
            UserRegister().showRules(parsingInfo = 'file_getName')
            name = input('Full Name: ').title()
            UserRegister().showRules(parsingInfo = 'file_getUserName')
            userName = input('Username: ').lower()
            UserRegister().showRules(parsingInfo = 'file_getPassword')
            password = input('Password: ')
        else:
            userName = input('Username: ').lower()
            password = input('Password: ')

        if userPath == 'user_register':
            Validation().registerValidate(rFeedbackLoop, rDetailed)
            UserRegister().newUser(password)
        elif userPath == 'user_login':
            UserLogin().dataAuth(userName, password, userAttempts)

    def getLines(self):
        global line
        if os.path.isfile('Auth/Inc/login.txt') and os.access('Auth/Inc/login.txt', os.R_OK):
            line = 0
            with open('Auth/Inc/login.txt', 'r') as f:
                for i in f:
                    i
                    line += 1
        
            
    def userTryCount(self, pathDecision):

        global userAttempts

        userAttempts += 1

        if userAttempts == 3:
            print("Attempts exceeded. Try again later.")
            exit(time.sleep(3))
        elif userAttempts == 1 and pathDecision == True:
            cRegAsk = input('We noticed that some information was not quite correct (details are mentioned above), do you want to continue with login or registration (Type either "L" OR "R")\nL/R: ').capitalize()
        
            if cRegAsk == 'L':
                User().displayData(userPath = 'user_login')
            elif cRegAsk == 'R':
                User().displayData(userPath = 'user_register')
            else:
                User().userTryCount(pathDecision = True)


class UserRegister(User):
    # Handling gather & write user credentials to a LOCKED file | Collecting and checking if username used | validation userName, name and password
    def newUser(self, password):
        authorised = False
        while authorised == False:
            passwordConfirm = input('Confirm Password: ')

            if password == passwordConfirm:
                UserRegister().parseToFile(name, userName, password)
                authorised = True
                os.system('cls' if os.name == 'nt' else "printf '\033c'")
                exit(input("Success!\nYou must restart the program to continue to sign in.\nPress ENTER to EXIT."))
                
            else:
                print("Passwords do not match. Try Again.")
                User().userTryCount(pathDecision = False)

    def parseToFile(self, name, userName, password):
        Validation().newUserUnRemove()
        with open('Auth/Inc/login.txt', 'a') as contents:
            contents.write(f'{name}|{userName}|{password}|\n')
            contents.close()

    def showRules(self, parsingInfo):

        destLocation = 'Auth/Inc/paramRequirements.txt'
        
        if parsingInfo != 'register_INITINFO':
            if parsingInfo == 'file_getName':
                print(linecache.getline(destLocation, 1))
            elif parsingInfo == 'file_getUserName':
                print(linecache.getline(destLocation, 2))
            elif parsingInfo == 'file_getPassword':
                print(linecache.getline(destLocation, 3))
            
            print("-"*50)

class UserLogin:
    # Handling show UI to user (UserName, Password) | looking for contents in locked file.

    def dataAuth(self, userName, password, userAttempts):
        global registerLoginMsg

        cycleComplete = False
        while cycleComplete == False:
            if line != currentLine:
                if userName == file_userName and password == file_password:
                    UserLogin().completeContinue()
                else:
                    User().fileDataRetrieve(redirectMsg = 'append_line')
            else:
                if userName == file_userName and password == file_password:
                    UserLogin().completeContinue()
                elif userName == file_userName and password != file_password:
                    User().fileDataRetrieve(redirectMsg = 'reset_line')
                    Validation().loginHandling(rFeedbackLoop = 'authError_passwordIncorrect', regLogin = 'user_login')
                elif userName != file_userName and password == file_password:
                    registerLoginMsg = 'password_present_RegLogin'
                    User().fileDataRetrieve(redirectMsg = 'reset_line')
                    Validation().loginHandling(rFeedbackLoop = 'authError_usernameIncorrect', regLogin = 'user_login')
                else:
                    User().fileDataRetrieve(redirectMsg = 'reset_line')
                    Validation().loginHandling(rFeedbackLoop = 'auth_userNamePassword_notFound', regLogin = 'user_login')

    def completeContinue(self):
        global cycleComplete

        cycleComplete = True
        os.system('cls' if os.name == 'nt' else "printf '\033c'")
        print('Logged In!')
        User().stateCurrentUser(file_name, userName)
        time.sleep(.1)
        from App import game

class Validation():

    def checkData(self):
        User().getLines()
        User().fileDataRetrieve(redirectMsg = 'reset_line')

        if file_name == 'undefined' or file_userName == 'undefined' or file_password == 'undefined':
            print('Looks like you\'re not in the system.\nRedirecting you to registration now.')
            time.sleep(3), os.system('cls' if os.name == 'nt' else "printf '\033c'")
            User().displayData(userPath = 'user_register')

    def newUserUnRemove(self):
        User().fileDataRetrieve(redirectMsg = 'reset_line')
        User().getLines()
        if os.path.isfile('Auth/Inc/login.txt') and os.access('Auth/Inc/login.txt', os.R_OK):
            if file_name == 'undefined':
                open('Auth/Inc/login.txt', 'w').close()


    def loginHandling(self, rFeedbackLoop, regLogin):
        if rFeedbackLoop == 'authError_passwordIncorrect':
            print("That password isn't linked to that account.")
            User().userTryCount(pathDecision = False)
        elif rFeedbackLoop == 'authError_usernameIncorrect':
            print("That username was not found.")
        elif rFeedbackLoop == 'auth_userNamePassword_notFound':
            print("The username OR the password was not found.")
            User().userTryCount(pathDecision = True)
    
        if (3 - userAttempts) >= 1:
            print("Try Again.")

        print("\nYou have " + str(3 - userAttempts) + " attempt(s) remaining.")
        print('-'*50)
        User().displayData(userPath = 'user_login')

    def dataUserScan(self, rFeedbackLoop, rDetailed):
        if os.path.isfile('Auth/Inc/login.txt') and os.access('Auth/Inc/login.txt', os.R_OK):
            dataCheckComplete = False
            rFeedbackLoop = 'authError_stringExistence'
            firstCheck = 'incomplete'

            while dataCheckComplete == False:

                User().getLines()
                if firstCheck == 'incomplete':
                    User().fileDataRetrieve(redirectMsg = 'reset_line')
                elif firstCheck == 'complete':
                    User().fileDataRetrieve(redirectMsg = 'append_line')

                if line != currentLine:
                    if file_userName == userName:
                        rDetailed = 'user_OCCUPIED'
                        dataCheckComplete = True
                    elif file_userName != userName:
                        rFeedbackLoop = 'name_user_ACCEPT'
                        dataCheckComplete = False
                    firstCheck = 'complete'

                else: # currentline == line (end line of file)
                    if file_userName != userName:
                        rFeedbackLoop = 'name_user_ACCEPT'
                    elif file_userName == userName:
                        rDetailed = 'user_OCCUPIED'

                    dataCheckComplete = True
            
            Validation().registerHandling(rFeedbackLoop, rDetailed)

    def registerValidate(self, rFeedbackLoop, rDetailed):
        validate = False

        while validate == False:
            if len(name) <= 3 or name is any(x.isdigit() for x in name) or ' ' not in name:
                Validation().registerHandling(rFeedbackLoop = 'init_validate_error', rDetailed = 'name')
            elif len(userName) < 4 or ' ' in userName:
                Validation().registerHandling(rFeedbackLoop = 'init_validate_error', rDetailed = 'userName')
            elif (len(password) < 8 and len(password) > 60) or not any(x.isupper() for x in password) or not any(x.isdigit() for x in password):
                Validation().registerHandling(rFeedbackLoop = 'init_validate_error', rDetailed = 'password')
            else:
                Validation().dataUserScan(rFeedbackLoop, rDetailed)
                print('Formatting Validation Complete!\n')
                validate = True

    def registerHandling(self, rFeedbackLoop, rDetailed):
        if rFeedbackLoop == 'init_validate_error':
            if rDetailed == 'name':
                UserRegister().showRules(parsingInfo = 'file_getName')
            elif rDetailed == 'userName':
                UserRegister().showRules(parsingInfo = 'file_getUserName')
            elif rDetailed == 'password':
                UserRegister().showRules(parsingInfo = 'file_getPassword')
            
            User().userTryCount(pathDecision = False)
            if (4 - userAttempts) >= 1:
                print("Try Again.")

            print("\nYou have " + str(3 - userAttempts) + " attempt(s) remaining.")
            print('-'*50)
            User().displayData(userPath = 'user_register')

        elif rFeedbackLoop == 'authError_stringExistence':
            if rDetailed == 'user_OCCUPIED':
                print('That userName already exists!')
            
            User().userTryCount(pathDecision = False)
            if (3 - userAttempts) >= 1:
                print("Try Again.")

            print("\nYou have " + str(3 - userAttempts) + " attempt(s) remaining.")
            print('-'*50)
            User().displayData(userPath = 'user_register')
            
            
            
        elif rFeedbackLoop == 'name_user_ACCEPT':
            os.system('cls' if os.name == 'nt' else "printf '\033c'")
            
            
    # Handles validation for bothing Login and Registration (name, userName, password, age)

a = input("Hello User! This program requires auth to access. Register (R) or Login (L)?\nR/L: ").capitalize()

if a == 'R':
    User().displayData(userPath = 'user_register')
else:
    Validation().checkData()
    User().displayData(userPath = 'user_login')