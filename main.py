#Import System and Time Modules
import sys
import time

#Finding path of required filed for the game to run
sys.path.insert(1, 'Auth/loginRegisterNEW')
sys.path.insert(1, 'App/game') #TO PUT SCORING SYS IN WITH GAME

welcomeAnswer = input("Hello!\nReady to get started? (Y/N)\nY/N: ").capitalize()

if welcomeAnswer == "Y":
    from Auth import loginRegisterNEW
elif welcomeAnswer == "N":
    exit("OK. See you in a bit.")
else:
    print("Error\nPlease run the file again.")
    time.sleep(1)
    exit()