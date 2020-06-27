import linecache, random, time as t, os
from datetime import datetime

class CreateGame():
    def totline(self):
        global lines
        lines = 1
        with open('App/createQuiz/quizTypes.txt', 'r') as f:
            line = 0  
            for i in f: line += 1
    
    def uIData(self):
        user = linecache.getline('Auth/Inc/currentUser.txt', 1)
        data = user.split('|')
        name = data[0]
        sp = name.split(' ')
        firstName = sp[0]
        user = data[1]
        print(f'{firstName}, you\'ve selected to create a quiz!\nWhat type of quiz do you want to make? You can choose from the options below.')
        with open('App/createQuiz/quizTypes.txt', 'r') as f:
            CreateGame().totline()
            line = 1
            while line != lines:
                print(f.readline())
                line += 1
        takeType = input('Your option: ')
        print(takeType)
        
        QuizTypes()


class QuizTypes():
    pass
class Setup():
    pass
class Finish():
    pass

CreateGame().uIData()