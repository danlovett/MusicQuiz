#Import System and Time Modules
import sys
import time

#Finding path of required filed for the game to run
sys.path.insert(1, 'Auth/loginRegister')
sys.path.insert(1, 'App/game') #TO PUT SCORING SYS IN WITH GAME

welcomeAnswer = input("Welcome to the game\nThis is a Music Quiz\nAre you ready to get started?\nY/N: ").capitalize()

if welcomeAnswer == "Y":
    pass
elif welcomeAnswer == "N":
    exit()
else:
    print("Error\nPlease run the file again.")
    time.sleep(1)
    exit()

from Auth import loginRegister # TO ADD IN FILE DIR

from App import game # TO ADD IN FILE DIR