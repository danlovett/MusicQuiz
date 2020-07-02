import sys as s
import linecache as l
import time
import os
dynamicAttempt = 0
dynamicLine = 1
totalLine = 0
getCurrentLineToCheckPassword = 0
onCheckFirstAfterLoopCheck = True
checkUserBeforeLoop = True


class General:

    def formatUI(self, rangeOfClear):
        for x in range(rangeOfClear):
            s.stdout.write("\033[F"), s.stdout.write("\033[K"), x

    def getDisplayContent(self, action):
        global displayName, displayUser, displayPassword, dynamicLine

        if action == 'dynamicLine:+1':
            dynamicLine += 1
        elif action == 'dynamicLine:Current':
            dynamicLine = dynamicLine
        elif action == 'dynamicLine:CheckingPassword':
            dynamicLine = getCurrentLineToCheckPassword
        elif action == 'dynamicLine:Reset':
            dynamicLine = 1

        if os.path.isfile('auth/lib/userdb.txt') and os.access('auth/lib/userdb.txt', os.R_OK):
            databaseContent = l.getline('auth/lib/userdb.txt', dynamicLine)
            individualContent = databaseContent.split('|')
            displayName = individualContent[0]
            displayUser = individualContent[1]
            displayPassword = individualContent[2]
            l.clearcache()

    def getTotalLines(self):
        global totalLine
        totalLine = 0
        if os.path.isfile('auth/lib/userdb.txt') and os.access('auth/lib/userdb.txt', os.R_OK):
            with open('auth/lib/userdb.txt', 'r') as f:
                for x in f:
                    totalLine += 1
                    x

    def getUserAttemptDynamic(self, action, typeofAction):
        global dynamicAttempt
        dynamicAttempt += 1
        if dynamicAttempt == 3 and action == 'CreateAccount:Fail':
            if typeofAction == 'from:ConfirmPassword':
                General().formatUI(1)
            elif typeofAction == 'from:Registration':
                General().formatUI(6)
            exit('Account Setup ⨉\nRestart the program.')
        elif dynamicAttempt == 3 and action == 'Login:Fail':
            General().formatUI(2)
            exit('Account Login ⨉\nRestart the program.')
        elif dynamicAttempt == 3:
            exit('⨉\nRestart the program.')


class Register:
    def userContentName(self):
        global userInName
        userInName = input(
            'Your name must:\n - Be AT LEAST 3 letters long\n - Contain NO numbers\n - Contain a space (to Separate first name and last name)\nFull Name: ').title()
        Validation().validateRegisterInUser('valid:name')
        General().formatUI(5)
        print(f"Name ✓"), time.sleep(.1)

    def userContentUsername(self):
        global userInUsername
        userInUsername = input(
            'Your Username must:\n - Be AT LEAST 4 characters long\n - Contain NO spaces\n - Be in lower case (don\'t worry, your username is automatically converted into lower case when you hit enter!)\nUsername: ').lower()
        Validation().validateRegisterInUser('valid:userName')
        General().formatUI(6)
        print(f"Name ✓ Username ✓"), time.sleep(.1)

    def userContentPassword(self):
        global userInPassword
        userInPassword = input(
            'Your password must:\n - Be between 8 and 60 characters (to stop hackers)\n - Contain AT LEAST one upper case character\n - Contain AT LEAST one number\nPassword: ')
        Validation().validateRegisterInUser('valid:password')
        General().formatUI(6)
        print(f"Name ✓ Username ✓ Password ✓"), time.sleep(.1)

    def userContentConfirmPassword(self, userInPassword):
        userInConfirmPassword = input('Confirm Password: ')
        if userInPassword == userInConfirmPassword:
            General().formatUI(2)
            print(f"Name ✓ Username ✓ Password ✓ Password Confirmation ✓"), time.sleep(.1)
            Register().accountSucceedWriteToDB()
            exit(input("Account Setup Complete ✓\n\nRestart the program and sign in!\nPress ENTER to exit this program."))
        else:
            General().formatUI(2)
            print(f"Name ✓ Username ✓ Password ✓ Password Confirmation ⨉"), time.sleep(.1)
            General().getUserAttemptDynamic('CreateAccount:Fail', 'from:ConfirmPassword')

    def accountSucceedWriteToDB(self):
        General().getDisplayContent('dynamicLine:Reset')
        if displayName == 'undefined' or displayUser == 'undefined' or displayPassword == 'undefined':
            with open('auth/lib/userdb.txt', 'w') as f:
                f.write(
                    f'{userInName}|{userInUsername}|{userInPassword}|'), f.close()
        else:
            with open('auth/lib/userdb.txt', 'a') as f:
                f.write(
                    f'\n{userInName}|{userInUsername}|{userInPassword}|'), f.close()

    def userContentRegisterBase(self, action):
        global dynamicAttempt
        if action in 'register':
            print('REGISTER\n' + '-'*35)
            Register().userContentName()
            Register().userContentUsername()
            Register().userContentPassword()
            Register().userContentConfirmPassword(userInPassword)


class Login:

    def userContentUsername(self):
        global userInUsername, checkUserBeforeLoop
        userInUsername = input('Username: ').lower()
        Validation().contentPassCheckLoginData('from:CheckUserContent')
        if checkUserBeforeLoop == True:
            General().formatUI(1)
            checkUserBeforeLoop = False
        else:
            General().formatUI(2)
        print("Username ✓"), time.sleep(.1)

    def userContentPassword(self):
        global userInPassword
        userInPassword = input('Password: ')
        Validation().contentPassCheckLoginData('check:CheckPasswordContent')
        General().formatUI(2)
        print("Username ✓ Password ✓"), time.sleep(.1)

    def userContentLoginBase(self, action):
        if action in 'login' or action == 'Login:ClearAllDataToGo':
            print('Login\n' + '-'*35)
            Login().userContentUsername()
            Login().userContentPassword()

        print("Account Authorised ✓")
        if action == 'Login:ClearAllDataToGo':
            Validation().clearUserDataActing()
        General().formatUI(1)
        print(f'Status: Logged in')
        with open('auth/lib/authoUserdb.txt', 'w') as f:
            f.write(f'{displayName}|{displayUser}|'), f.close()
        for x in range(3):
            print(
                f'Taking you to the game now{"."*x}'), time.sleep(.5), s.stdout.write("\033[F"), x
        from app import game


class Validation:

    def contentPassCheckLoginData(self, action):
        global getCurrentLineToCheckPassword, onCheckFirstAfterLoopCheck
        if action == 'from:CheckUserContent':
            General().getTotalLines()
            General().getDisplayContent('dynamicLine:Reset')
            userNameLoginExistBool = False
            onCheckFirst = True
            while userNameLoginExistBool == False:
                if dynamicLine != totalLine:
                    if displayUser == userInUsername:
                        userNameLoginExistBool = True
                    elif onCheckFirst == True:
                        General().getDisplayContent('dynamicLine:Reset')
                        onCheckFirst = False
                    else:
                        General().getDisplayContent('dynamicLine:+1')
                else:
                    General().getDisplayContent('dynamicLine:Current')
                    if displayUser == userInUsername:
                        userNameLoginExistBool = True
                    else:
                        break
            getCurrentLineToCheckPassword = dynamicLine

        elif action == 'check:CheckPasswordContent':
            General().getTotalLines()
            General().getDisplayContent('dynamicLine:CheckingPassword')
            passwordMatchUserBool = False
            while passwordMatchUserBool == False:
                if displayPassword == userInPassword:
                    passwordMatchUserBool = True
                else:
                    break

        if action == 'from:CheckUserContent':
            if userNameLoginExistBool == False:
                General().getUserAttemptDynamic('Login:Fail', '')
                if onCheckFirstAfterLoopCheck == True:
                    General().formatUI(1)
                    onCheckFirstAfterLoopCheck = False
                else:
                    General().formatUI(2)
                print(
                    f'Username ⨉ {3-dynamicAttempt} {"try" if 3-dynamicAttempt==1 else "tries"} remain{"s" if dynamicAttempt == 2 else ""}.')
                Login().userContentUsername()
        elif action == 'check:CheckPasswordContent':
            if passwordMatchUserBool == False:
                General().getUserAttemptDynamic('Login:Fail', '')
                General().formatUI(2)
                print(
                    f'Username ✓ Password ⨉ {3-dynamicAttempt} {"try" if 3-dynamicAttempt==1 else "tries"} remain{"s" if dynamicAttempt == 2 else ""}.')
                Login().userContentPassword()

    def checkNewUserQuery(self):
        General().getTotalLines()
        General().getDisplayContent('dynamicLine:Reset')
        if displayName == 'undefined' or displayUser == 'undefined' or displayPassword == 'undefined':
            print(
                'Looks like you\'re not in the system.\nRedirecting you to registration now.')
            time.sleep(3)
            os.system('cls' if os.name == 'nt' else "printf '\033c'")
            Register().userContentRegisterBase('r')

    def validateRegisterInUser(self, action):
        if action == 'valid:name':
            if len(userInName) <= 3 or userInName is any(x.isdigit() for x in userInName) or ' ' not in userInName:
                General().getUserAttemptDynamic('CreateAccount:Fail', 'from:Registration')
                General().formatUI(5)
                print(
                    f'Name ⨉ {3-dynamicAttempt} {"try" if 3-dynamicAttempt==1 else "tries"} remain{"s" if dynamicAttempt == 2 else ""}.')
                Register().userContentName()
        elif action == 'valid:userName':
            if len(userInUsername) < 4 or ' ' in userInUsername:
                General().getUserAttemptDynamic('CreateAccount:Fail', 'from:Registration')
                General().formatUI(6)
                print(
                    f'Name ✓ Username ⨉ {3-dynamicAttempt} {"try" if 3-dynamicAttempt==1 else "tries"} remain{"s" if dynamicAttempt == 2 else ""}.')
                Register().userContentUsername()
            else:
                Validation().checkRegisterUserInData('from:CheckUserContent')
        elif action == 'valid:password':
            if (len(userInPassword) < 8 and len(userInPassword) > 60) or not any(x.isupper() for x in userInPassword) or not any(x.isdigit() for x in userInPassword):
                General().getUserAttemptDynamic('CreateAccount:Fail', 'from:Registration')
                General().formatUI(6)
                print(
                    f'Name ✓ Username ✓ Password ⨉ {3-dynamicAttempt} {"try" if 3-dynamicAttempt==1 else "tries"} remain{"s" if dynamicAttempt == 2 else ""}.')
                Register().userContentPassword()

    def checkRegisterUserInData(self, action):
        if action == 'from:CheckUserContent':
            General().getTotalLines()
            General().getDisplayContent('dynamicLine:Reset')
            duplicateUsernameBool = False
            while duplicateUsernameBool == False:
                if dynamicLine != totalLine:
                    if displayUser == userInUsername:
                        duplicateUsernameBool = True
                    else:
                        General().getDisplayContent('dynamicLine:+1')
                else:
                    General().getDisplayContent('dynamicLine:Current')
                    if displayUser == userInUsername:
                        duplicateUsernameBool = True
                    else:
                        break

        if action == 'from:CheckUserContent' and duplicateUsernameBool == True:
            General().getUserAttemptDynamic('CreateAccount:Fail', 'From:Registration')
            input('Username already Exists!\nPress ENTER to retry.')
            General().formatUI(8)
            print('Name ✓ Username ⨉ {}')
            Register().userContentUsername()

    def clearUserDataActing(self):
        General().getTotalLines()
        General().getDisplayContent('dynamicLine:Reset')
        General().formatUI(2)

        print(
            f'Database check ✓ User Input ✓ 5 Accounts {"✓" if totalLine >= 5 else "⨉"}')

        if (displayUser != userInUsername and totalLine < 5) or totalLine < 5:
            decisionContinue = False
            if (displayUser == userInUsername and totalLine < 5):
                errorReason = 'Not enough users'
            elif (displayUser != userInUsername and totalLine >= 5):
                errorReason = 'Not First User'
            else:
                errorReason = 'You did not meet any of the requirements.'
            print(
                f"\nSorry, you are not eligible to do this.\n\nReason: {errorReason}")
        else:
            decisionContinue = True
            print('Continue...')

        if decisionContinue == True:
            userInContinueRemoveData = input(
                'Are you sure you want to remove everyone, apart from yourself, from the database? (Yes/No)\n').title()
            if userInContinueRemoveData == 'Yes':
                with open('auth/lib/userdb.txt', 'w') as f:
                    f.write(f'{displayName}|{displayUser}|{displayPassword}')
                    f.close()
                print('Successfully Removed.')
                askUserRegister = input(
                    'Do you want to register a new account? (Yes/No)').title()
                if askUserRegister == 'Yes':
                    Register().userContentRegisterBase('r')
                elif askUserRegister == 'No':
                    exit('Exit.')
            elif userInContinueRemoveData == 'No':
                print('Okay, Program will now exit.')

        else:
            exit('Exit.')


class ProcessFeatures:
    def userExitLogoutForce(self):
        if os.path.isfile('auth/lib/authoUserdb.txt') and os.access('auth/lib/authoUserdb.txt', os.R_OK):
            os.remove('auth/lib/authoUserdb.txt')

    def clearUserDataProcess(self, action):
        if action == 'x-rmv-aldata':
            General().getDisplayContent('dynamicLine:Reset')
            if displayName == 'undefined':
                print('No Data found.\nError code: XERR-NDF-TREG\n\nTaking you to registration now. press "Ctrl + C" to stop this operation.')
                time.sleep(4)
                General().formatUI(5)
                Register().userContentRegisterBase('r')
            else:
                Login().userContentLoginBase('Login:ClearAllDataToGo')


try:
    action = input(
        "How's it gonna be? Login or Register?\nI'm going to ").lower()
    if action in 'register':
        os.system('cls' if os.name == 'nt' else "printf '\033c'")
        Register().userContentRegisterBase('r')
    elif action == 'x-rmv-aldata':
        os.system('cls' if os.name == 'nt' else "printf '\033c'")
        ProcessFeatures().clearUserDataProcess(action)
    else:
        os.system('cls' if os.name == 'nt' else "printf '\033c'")
        Validation().checkNewUserQuery()
        Login().userContentLoginBase('l')

except KeyboardInterrupt:
    ProcessFeatures().userExitLogoutForce()
    exit('\nYou requested to force exit the program.\n{exit}')
