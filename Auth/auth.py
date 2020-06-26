import time, os, sys as s, linecache as l
s.path.insert(1, 'App/game')
u_attempt, c_line = 0, 1

class General:
    def clearLnR(self, rng):
        print()
        for i in range(rng):
            s.stdout.write("\033[F")
            s.stdout.write("\033[K")
            i

    def sys_data(self, r_action):
        global sys_name, sys_userName, sys_password, c_line
        if r_action == '+ln': c_line += 1
        else: c_line = 1

        if os.path.isfile('Auth/Inc/Login.txt') and os.access('Auth/Inc/Login.txt', os.R_OK):
            data = l.getline('Auth/Inc/Login.txt', c_line)
            dataBlock = data.split('|')
            sys_name = dataBlock[0]
            sys_userName = dataBlock[1]
            sys_password = dataBlock[2]
            l.clearcache()

    def c_user(self, name, userName):
        with open('Auth/Inc/currentUser.txt', 'w') as f: f.write(f'{name}|{userName}|'), f.close()  
        print('Enjoy the game!')

    def UIdata(self, a):
        global name, userName, password
        if a == 'l': 
            print('LOGIN\n' + '-'*35)
            userName = input('Username: ').lower()
            password = input('Password: ')
            Login().auth_data(userName, password, u_attempt, a = 'l')
        elif a == 'x-rmv-aldata':
            userName = input('Username: ').lower()
            password = input('Password: ')
            General().sys_data(r_action= '.'), Login().auth_data(userName, password, u_attempt, a = 'x-rmv-aldata')

    def totline(self):
        global line
        if os.path.isfile('Auth/Inc/login.txt') and os.access('Auth/Inc/login.txt', os.R_OK): 
            line = 0
            with open('Auth/Inc/login.txt', 'r') as f: 
                for i in f: 
                    line += 1
                    i       
    def attempts(self, pathDecision, goto):
        global u_attempt
        u_attempt += 1
        if u_attempt == 3 and pathDecision == False and goto == 'from:confirmP':
            for i in range(2):
                s.stdout.write("\033[F")
                s.stdout.write("\033[K")
                i
            print('Account Setup ⨉\nRestart the program.')
            exit(time.sleep(3))
        elif u_attempt == 3 and pathDecision == False and goto == 'from:nup':
            for i in range(7):
                s.stdout.write("\033[F")
                s.stdout.write("\033[K")
            print('Account Setup ⨉\nRestart the program.')
            exit(time.sleep(3))
        if u_attempt == 3 and pathDecision == False: 
            print('Error.\nRestart the program.')
            exit(time.sleep(3))
        elif u_attempt == 1 and pathDecision == True:
            cRegAsk = input('We noticed that some information was not quite correct (details are mentioned above), do you want to continue with login or registration (Type either "L" OR "R")\nL/R: ').capitalize()
            if cRegAsk == 'L': General().UIdata(a)
            elif cRegAsk == 'R': General().UIdata(a)
            else: General().attempts(pathDecision = True, goto='')


class Register:

    def name(self, re):
        global name
        name = input('Your name must:\n - Be AT LEAST 3 letters long\n - Contain NO numbers\n - Contain a space (to Separate first name and last name)\n\nFull Name: ').title()
        Validation().valid_reg(goto='valid:name')
        General().clearLnR(rng=7)
        print(f"name ✓"), time.sleep(.1)
    def userName(self, re):
        global userName
        userName = input('Your Username must:\n - Be AT LEAST 4 characters long\n - Contain NO spaces\n - Be in lower case (don\'t worry, your username is automatically converted into lower case when you hit enter!)\n\nUsername: ').lower()
        Validation().valid_reg(goto='valid:userName')
        General().clearLnR(rng=7)
        s.stdout.write("\033[F")
        print(f"name ✓ username ✓"), time.sleep(.1)
    def password(self, re):
        global password
        password = input('Your password must:\n - Be between 8 and 60 characters (to stop hackers)\n - Contain AT LEAST one upper case character\n - Contain AT LEAST one number\n\nPassword: ')
        Validation().valid_reg(goto='valid:password')
        General().clearLnR(rng=7)
        s.stdout.write("\033[F")
        print(f"name ✓ username ✓ Password ✓"), time.sleep(.1)
    def register(self, a):
        if a in 'register':
            print('REGISTER\n' + '-'*35)
            Register().name(re='')
            Register().userName(re='')
            Register().password(re='')
            Register().confirm_user(password)

    def confirm_user(self, password):
        auth = False
        while auth == False:
            c_password = input('Confirm Password: ')
            time.sleep(.1)
            if password == c_password:
                for i in range(2):
                    s.stdout.write("\033[F")
                    s.stdout.write("\033[K")
                    i
                print(f"name ✓ username ✓ Password ✓ Password Confirmation ✓"), time.sleep(.1)
                Register().wFile_newUser(name, userName, password)
                auth = True
                exit(input("Account Setup Complete ✓\n\nRestart the program and sign in!\nPress ENTER to exit this program."))
            else: 
                for i in range(2):
                    s.stdout.write("\033[F")
                    s.stdout.write("\033[K")
                    i
                print(f"name ✓ username ✓ Password ✓ Password Confirmation ⨉"), time.sleep(.1)
                General().attempts(pathDecision = False, goto='from:confirmP')

    def wFile_newUser(self, name, userName, password):
        Validation().uRemove_def()
        with open('Auth/Inc/login.txt', 'a') as contents: 
            if l.getline('Auth/Inc/Login.txt', 1) == '': contents.write(f'{name}|{userName}|{password}|'), contents.close()
            else: contents.write(f'\n{name}|{userName}|{password}|'), contents.close()

    def reg_req(self, redir):
        loc = 'Auth/Inc/paramRequirements.txt'
        if redir == 'f-getN': print(l.getline(loc, 1))
        elif redir == 'f-getUN': print(l.getline(loc, 2))
        elif redir == 'f-getP': print(l.getline(loc, 3))
        print(f"{'-'*50}")


class Login:

    def auth_data(self, userName, password, u_attempt, a):
        General().totline()
        cc = False
        while cc == False:
            if line != c_line:
                if a == 'x-rmv-aldata': cc = True, Validation().rmvDataVal(userName)
                elif userName == sys_userName and password == sys_password: Login().auth_con()
                else: General().sys_data(r_action = '+ln')
            else:
                if a == 'x-rmv-aldata': cc = True, Validation().rmvDataVal(userName)
                elif userName == sys_userName and password == sys_password: Login().auth_con()
                elif userName == sys_userName and password != sys_password: General().sys_data(r_action = '.x'), Validation().log_handle(rfdbk = 'xerr_pin')
                elif userName != sys_userName and password == sys_password: General().sys_data(r_action = '.x'), Validation().log_handle(rfdbk = 'xerr_uin')
                else: General().sys_data(r_action = '.x') , Validation().log_handle(rfdbk = 'xerr_pui_nfd')

    def auth_con(self):
        global cc
        cc = True
        os.system('cls' if os.name == 'nt' else "printf '\033c'")
        print('Logged In!')
        General().c_user(sys_name, userName)
        time.sleep(.1)
        from App import game

class Validation:

    def chk_data(self):
        General().totline()
        General().sys_data(r_action = '.ln')
        if sys_name == 'undefined' or sys_userName == 'undefined' or sys_password == 'undefined':
            print('Looks like you\'re not in the system.\nRedirecting you to registration now.')
            time.sleep(3), os.system('cls' if os.name == 'nt' else "printf '\033c'")
            General().UIdata(a = 'r')
        
    def rmvDataVal(self, userName):
        General().totline()
        with open('Auth/Inc/Login.txt', 'r') as f:
            content = f.readline()
            dataBlock = content.split('|')
        
        if dataBlock[1] != userName and line < 5: conRmvData = False, print("Sorry, you are not eligible to do this.\n\nERROR CODE(S): XERR-NOT-FIRST-USER, XERR-UREQ-FAIL")
        else: 
            conRmvData = True
            print('Continue...')

        if conRmvData == True:
            while True:
                cfrmDelData = input('Are you sure you want to remove all user data? (Yes/No)\n').title()
                if cfrmDelData == 'Yes':
                    with open('Auth/Inc/Login.txt', 'w') as f: f.write(f'{name}|{userName}|{password}'), f.close()
                    print('Successfully Removed.')
                    while True:
                        toReg = input('Do you want to register a new account? (Yes/No)').title()
                        if toReg == 'Yes': General().UIdata(a = 'r')
                        elif toReg == 'No': break
                        else: 
                            General().attempts(pathDecision = False,goto='')
                            print(f'Error.\nYou have {u_attempt} attempt{"" if u_attempt == 1 else "s"} remaining.\n{"-"*50}')
                    break
                elif cfrmDelData == 'No':
                    print('Okay, Program will now exit.')
                    break
                else:
                    General().attempts(pathDecision = False, goto='')
                    print(f'Error.\nYou have {u_attempt} attempt{"" if u_attempt == 1 else "s"} remaining.\n{"-"*50}')

        else: print('Exit.')

    def uRemove_def(self):
        General().sys_data(r_action = '.x')
        General().totline()
        if (os.path.isfile('Auth/Inc/login.txt') and os.access('Auth/Inc/login.txt', os.R_OK)) and sys_name == 'undefined': open('Auth/Inc/login.txt', 'w').close()

    def log_handle(self, rfdbk):
        if rfdbk == 'xerr_pin':
            print("That password isn't linked to that account.")
            General().attempts(pathDecision = False, goto='')
        elif rfdbk == 'xerr_uin': print("That username was not found.")
        elif rfdbk == 'xerr_pui_nfd':
            print("The username OR the password was not found.")
            General().attempts(pathDecision = True, goto='')
        
        if (3 - u_attempt) >= 1: print("Try Again.")
        print("\nYou have " + str(3 - u_attempt) + " attempt(s) remaining.")
        print('-'*50)
        General().UIdata(a = 'L')
        os.system('cls' if os.name == 'nt' else "printf '\033c'")

    def chk_exist_user(self,):
        if os.path.isfile('Auth/Inc/login.txt') and os.access('Auth/Inc/login.txt', os.R_OK):
            dcc, fc = False, 'ic'
            while dcc == False:
                General().totline()
                if fc == 'ic':General().sys_data(r_action = '.x')
                elif fc == 'c': General().sys_data(r_action = '+ln')
                if line != c_line and sys_userName == userName:
                    dcc = True
                    xerr = True
                    General().clearLnR(rng=8)
                elif line != c_line and sys_userName != userName: xerr = False
                elif line == c_line and sys_userName == userName: 
                    dcc = True
                    xerr = True
                    General().clearLnR(rng=8)
                elif sys_userName != userName and line == c_line:
                    xerr = False
                    dcc = True
                fc = 'c'
            
            if xerr == True:
                General().attempts(pathDecision = False, goto='')
                print(f'name ✓ username ⨉ {3-u_attempt} {"try" if 3 - u_attempt == 1 else "tries"} remain')
                Register().userName(re='')

    def valid_reg(self, goto):
        if goto == 'valid:name':
            if len(name) <= 3 or name is any(x.isdigit() for x in name) or ' ' not in name:
                re='error:name'
                General().attempts(pathDecision = False, goto='from:nup')
                General().clearLnR(rng=8)
                print("name ⨉")
                Register().name(re)
            else: re = ''
        elif goto == 'valid:userName':
            if len(userName) < 4 or ' ' in userName: 
                re='error:userName'
                General().attempts(pathDecision = False, goto='from:nup')
                General().clearLnR(rng=8)
                print("name ✓ username ⨉")
                Register().userName(re)
            else: 
                re = ''
                Validation().chk_exist_user()
        elif goto == 'valid:password':
            if (len(password) < 8 and len(password) > 60) or not any(x.isupper() for x in password) or not any(x.isdigit() for x in password): 
                re='error:password'
                General().attempts(pathDecision = False, goto='from:nup')
                General().clearLnR(rng=8)
                print("name ✓ username ⨉ password ⨉")
                Register().password(re)
            else: re = ''

try:
    a = input("How's it gonna be? Login or Register?\nI'm going to ").lower()
    if a in 'register': os.system('cls' if os.name == 'nt' else "printf '\033c'"), Register().register(a)
    elif a == 'x-rmv-aldata': os.system('cls' if os.name == 'nt' else "printf '\033c'"), General().UIdata(a)
    else: os.system('cls' if os.name == 'nt' else "printf '\033c'"), Validation().chk_data(), General().UIdata(a = 'l')
except KeyboardInterrupt:
    exit('\nForce Exit.\nAll data has been LOST.\nSorry for the inconvenience.')
