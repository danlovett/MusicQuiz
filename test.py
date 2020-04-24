attemptsRemain = attemptsRemain - 1

if count == catchLineLogin:
    if attemptsRemain < 3 and eventLogger == 'user_redirect_main':
        print(userName + " user not found. You have " + str(userAttempsRemains) + " attempts remaining before being directed to the register page")
        presentUserNameIn = True
    elif attemptsRemain == 3 and eventLogger == 'user_redirect_main':
        redirectReason(userName, redirect = 'username_load_error')
    elif attemptsRemain < 3 and eventLogger == 'user_redirect_admin':
        print("You cannot have 'admin' in your username, you have " + str((attemptsRemain)) + " attempts remaining before you're forced to exit")
    elif attemptsRemain == 3 and eventLogger == 'user_redirect_admin':
        redirectReason(userName, redirect = 'user_redirect_admin')

if attemptsRemain < 3 and eventLogger == 'password_load_error':
    print(print("Worng Password. You have " + str(attemptsRemain) + " attempts remaining"))
elif attemptsRemain == 3 and eventLogger == 'password_load_error':
    redirectReason(userName, redirect = 'password_load_error')
    