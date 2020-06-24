import time, os, sys as s, linecache as l
s.path.insert(1, 'App/game')
u_attempt, c_line = 0, 1
rfdbk, u_rfdbk = '', ''

class General:
    def sys_data(self, r_action):
        global sys_name, sys_userName, sys_password, c_line
        
        if r_action == '+ln': c_line += 1
        else: c_line = 1

        if os.path.isfile('Auth/Inc/login.txt') and os.access('Auth/Inc/login.txt', os.R_OK):
            data = l.getline('Auth/Inc/login.txt', c_line)
            dataBlock = data.split('|')
            sys_name = dataBlock[0]
            sys_userName = dataBlock[1]
            sys_password = dataBlock[2]
            l.clearcache()

    def c_user(self, name, userName):
        with open('Auth/Inc/currentUser.txt', 'w') as f: f.write(f'{name}|{userName}|'), f.close()  
        print('Enjoy the game!')

    def UIdata(self, redir):
        global name, userName, password
        if redir == 'u_reg':
            print('Registration:\n' + '-'*35 )
            Register().reg_req(redir = 'f-getN')
            name = input('Full Name: ').title()
            Register().reg_req(redir = 'f-getUN')
            userName = input('Username: ').lower()
            Register().reg_req(redir = 'f-getP')
            password = input('Password: ')
        else: 
            userName = input('Username: ').lower()
            password = input('Password: ')

        if redir == 'u_reg': Validation().valid_reg(rfdbk, u_rfdbk), Register().confirm_user(password)
        else: Login().auth_data(userName, password, u_attempt)

    def totline(self):
        global line
        if os.path.isfile('Auth/Inc/login.txt') and os.access('Auth/Inc/login.txt', os.R_OK): 
            line = 0
            with open('Auth/Inc/login.txt', 'r') as f: 
                for i in f: line += 1
                i       
    def attempts(self, pathDecision):
        global u_attempt
        u_attempt += 1
        if u_attempt == 3: print("Attempts exceeded. Try again later."), exit(time.sleep(3))
        elif u_attempt == 1 and pathDecision == True:
            cRegAsk = input('We noticed that some information was not quite correct (details are mentioned above), do you want to continue with login or registration (Type either "L" OR "R")\nL/R: ').capitalize()
            if cRegAsk == 'L': General().UIdata(redir = 'lgn')
            elif cRegAsk == 'R': General().UIdata(redir = 'u_reg')
            else: General().attempts(pathDecision = True)


class Register:

    def confirm_user(self, password):
        auth = False
        while auth == False:
            c_password = input('Confirm Password: ')
            if password == c_password: 
                Register().wFile_newUser(name, userName, password)
                auth = True, os.system('cls' if os.name == 'nt' else "printf '\033c'"), exit(input("Success!\nYou must restart the program to continue to sign in.\nPress ENTER to EXIT."))
            else: print("Passwords do not match. Try Again."), General().attempts(pathDecision = False)

    def wFile_newUser(self, name, userName, password):
        Validation().uRemove_def()
        with open('Auth/Inc/login.txt', 'a') as contents: contents.write(f'{name}|{userName}|{password}|\n'), contents.close()

    def reg_req(self, redir):
        loc = 'Auth/Inc/paramRequirements.txt'
        if redir == 'f-getN': print(l.getline(loc, 1))
        elif redir == 'f-getUN': print(l.getline(loc, 2))
        elif redir == 'f-getP': print(l.getline(loc, 3))
        print(f"{'-'*50}")


class Login:

    def auth_data(self, userName, password, u_attempt):
        cc = False
        while cc == False:
            if line != c_line:
                if userName == sys_userName and password == sys_password: Login().auth_con()
                else: General().sys_data(r_action = '+ln')
            else:
                if userName == sys_userName and password == sys_password: Login().auth_con()
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
        General().sys_data(r_action = 'reset_line')
        if sys_name == 'undefined' or sys_userName == 'undefined' or sys_password == 'undefined':
            print('Looks like you\'re not in the system.\nRedirecting you to registration now.')
            time.sleep(3), os.system('cls' if os.name == 'nt' else "printf '\033c'")
            General().UIdata(redir = 'u_reg')

    def uRemove_def(self):
        General().sys_data(r_action = '.x')
        General().totline()
        if (os.path.isfile('Auth/Inc/login.txt') and os.access('Auth/Inc/login.txt', os.R_OK)) and sys_name == 'undefined': open('Auth/Inc/login.txt', 'w').close()

    def log_handle(self, rfdbk):
        if rfdbk == 'xerr_pin':
            print("That password isn't linked to that account.")
            General().attempts(pathDecision = False)
        elif rfdbk == 'xerr_uin': print("That username was not found.")
        elif rfdbk == 'xerr_pui_nfd':
            print("The username OR the password was not found.")
            General().attempts(pathDecision = True)
        
        if (3 - u_attempt) >= 1: print("Try Again.")
        print("\nYou have " + str(3 - u_attempt) + " attempt(s) remaining.")
        print('-'*50)
        General().UIdata(redir = 'lgn')
        os.system('cls' if os.name == 'nt' else "printf '\033c'")

    def chk_exist_user(self, rfdbk, u_rfdbk):
        if os.path.isfile('Auth/Inc/login.txt') and os.access('Auth/Inc/login.txt', os.R_OK):
            dcc, rfdbk, fc = False, 'un_exst', 'ic'
            while dcc == False:
                General().totline()
                if fc == 'ic':General().sys_data(r_action = '.x')
                else: General().sys_data(r_action = '+ln')
                if line != c_line and sys_userName == userName: u_rfdbk, dcc = 'u_occ', True
                elif sys_userName != userName and line == c_line: rfdbk, dcc = 'u_acc', True
                else: u_rfdbk, dcc = 'u_occ', True
                fc = 'c'
            
            Validation().reg_handle(rfdbk, u_rfdbk)

    def valid_reg(self, rfdbk, u_rfdbk):
        xdt = False
        while xdt == False:
            if len(name) <= 3 or name is any(x.isdigit() for x in name) or ' ' not in name: Validation().reg_handle(rfdbk = 'fmt-x', u_rfdbk = 'name')
            elif len(userName) < 4 or ' ' in userName: Validation().reg_handle(rfdbk = 'fmt-x', u_rfdbk = 'userName')
            elif (len(password) < 8 and len(password) > 60) or not any(x.isupper() for x in password) or not any(x.isdigit() for x in password): Validation().reg_handle(rfdbk = 'fmt-x', u_rfdbk = 'password')
            else: 
                Validation().chk_exist_user(rfdbk, u_rfdbk)
                print('Formatting Validation Complete!\n')
                xdt = True

    def reg_handle(self, rfdbk, u_rfdbk):
        if rfdbk == 'fmt-x':
            if u_rfdbk == 'name': Register().reg_req(redir = 'f-getN')
            elif u_rfdbk == 'userName': Register().reg_req(redir = 'f-getUN')
            elif u_rfdbk == 'password': Register().reg_req(redir = 'f-getP')
            General().attempts(pathDecision = False)
            print(f"\n{'Try Again.' if 4 - u_attempt >= 1 else ''}\nYou have {3 - u_attempt} attempt{'' if 3 - u_attempt == 1 else 's'} remaining.\n{'-'*50}\n")
            General().UIdata(redir = 'user_register')

        elif rfdbk == 'un_exst' and u_rfdbk == 'u_occ': 
            print('That userName already exists!')
            General().attempts(pathDecision = False)
            print(f"\n{'Try Again.' if 4 - u_attempt >= 1 else ''}You have {3 - u_attempt} attempt{'' if 3 - u_attempt == 1 else 's'} remaining.\n{'-'*50}\n")
            General().UIdata(redir = 'u_reg')
            os.system('cls' if os.name == 'nt' else "printf '\033c'")
             
        elif rfdbk == 'u_acc':
            os.system('cls' if os.name == 'nt' else "printf '\033c'")

a = input("Hello User! This program requires authorisation to access. Register (R) or Login (L)?\nR/L: ").capitalize()
if a == 'Reset':
    r = input('Reset data? (reset)\n').lower()
    if r == 'reset':
        with open('Auth/Inc/Login.txt', 'w') as f: f.write(f"{'undefined|'*3}"), f.close()
        exit('Complete.')
elif a == 'R': General().UIdata(redir = 'u_reg')
else: Validation().chk_data(), General().UIdata(redir = 'u_lgn')