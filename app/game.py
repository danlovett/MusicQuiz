# imports
import linecache as l
import sys as s
import random
import time
import os
from datetime import datetime

dynamicAttempt = 0
dynamicQuestionInt = 1
dynamicScore = 0
questionIterateContinue = True
currentDayValue = datetime.today().strftime('%Y-%m-%d')


class General:

    def UIdata(self):
        global userDecisionTypeMusic, questionRangeIndex
        General().getDisplayContentSystem('GetQuizOptions', 'standardQuiz')
        userDecisionTypeMusic = input(
            f"Please select from the following options to begin playing: {typeofData}\n").title()
        if userDecisionTypeMusic == typeofData:
            General().getTotalLines(
                f'{typeofData}.txt', 'app/lib/standard-quizes')
            questionRangeIndex = list(range(1, totalLine))
            input(f'Okay, running {typeofData} music now.\nPress ENTER to continue.'), Game(
            ).userContentStandardQuiz()
        else:
            print(
                f'"{userDecisionTypeMusic}" is not a music genre avaliable for this quiz.\nRestart the program and try again.')

    def formatUI(self, rangeOfClear):
        for x in range(rangeOfClear):
            s.stdout.write("\033[F"), s.stdout.write("\033[K"), x

    def getDisplayContentUser(self):
        global displayFirstName, displayUser, displayName
        folderDirectoryQuery = 'auth/lib'
        fileDirectoryQuery = 'authoUserdb.txt'
        if os.path.isfile(f'{folderDirectoryQuery}/{fileDirectoryQuery}') and os.access(f'{folderDirectoryQuery}/{fileDirectoryQuery}', os.R_OK):
            databaseContent = l.getline(
                f'{folderDirectoryQuery}/{fileDirectoryQuery}', 1)
            individualContent = databaseContent.split('|')
            displayName = individualContent[0]
            displayUser = individualContent[1]
            nameParts = displayName.split(' ')
            displayFirstName = nameParts[0]
            l.clearcache()
        elif os.path.isfile('auth/lib/authoUserdb.txt') == False:
            exit(f"Autho Failed.\nLogin First.\nError: noSuchFileExists.\nRestart from main.py and try again.")
        else:
            exit('Unknown Error. Restart the program (and IDE) and try again.\nIf the issue persits, send an email to "danlovett@hey.com" with a descriptive issue report to help you fix the issue\nMore details on GitHub.')

    def getDisplayContentSystem(self, action, typeofAction):
        global displaySong, displayArtist, displaySongReleaseYear, displayFirstStringItem, displayHintFromSong, typeofData
        if action == 'GetStandardQuizData':
            fileDirectoryQuery = f'{userDecisionTypeMusic}.txt'
            readLineFromFile = random.choice(questionRangeIndex)
            questionRangeIndex.remove(readLineFromFile)
        elif action == 'GetQuizOptions':
            fileDirectoryQuery = '.compile.txt'
            readLineFromFile = 1
        elif action == 'GetUserGeneratedQuiz':
            pass  # NOT YET IMP.

        if typeofAction == 'standardQuiz':
            folderDirectoryQuery = 'app/lib/standard-quizes'
        elif typeofAction == 'GetUserGeneratedQuiz':
            folderDirectoryQuery = 'app/lib/ugen-quizes'

        if os.path.isfile(f'{folderDirectoryQuery}/{fileDirectoryQuery}') and os.access(f'{folderDirectoryQuery}/{fileDirectoryQuery}', os.R_OK):
            databaseContent = l.getline(
                f'{folderDirectoryQuery}/{fileDirectoryQuery}', readLineFromFile)
            individualContent = databaseContent.split('|')

            if action == 'GetStandardQuizData':
                displaySong = individualContent[0]
                displayArtist = individualContent[1]
                displaySongReleaseYear = individualContent[2]
                displayFirstStringItem = displaySong[0]
                displayHintFromSong = displaySong[1]
            elif action == 'GetQuizOptions':
                # To change get back all avail options
                typeofData = individualContent[0]
        else:
            ProcessFeatures().newFileGenerate(fileDirectoryQuery, folderDirectoryQuery)

    def getDisplayContentScoring(self, action):
        global displayHighScore, displayHighScoreDateAchieved, displayUsername
        folderDirectoryQuery = 'app/lib/scores'
        fileDirectoryQuery = 'highScoredb.txt'
        readLineFromFile = 1

        if os.path.isfile(f'{folderDirectoryQuery}/{fileDirectoryQuery}') and os.access(f'{folderDirectoryQuery}/{fileDirectoryQuery}', os.R_OK):
            databaseContent = l.getline(
                f'{fileDirectoryQuery}', readLineFromFile)
            individualContent = databaseContent.split('|')

            if action == 'GetHighScoreDB':
                displayHighScoreDateAchieved = individualContent[0]
                displayHighScore = individualContent[1]
                displayUsername = individualContent[2]
        else:
            ProcessFeatures().newFileGenerate(fileDirectoryQuery, folderDirectoryQuery)

    def getTotalLines(self, fileDirectoryQuery, folderDirectoryQuery):
        global totalLine
        totalLine = 0
        if os.path.isfile(f'{folderDirectoryQuery}/{fileDirectoryQuery}') and os.access(f'{folderDirectoryQuery}/{fileDirectoryQuery}', os.R_OK):
            with open(f'{folderDirectoryQuery}/{fileDirectoryQuery}', 'r') as f:
                for x in f:
                    totalLine += 1
                    x

    def getUserAttemptDynamic(self, action):
        global dynamicAttempt
        if action == 'UserInputCorrect:ResetAttempts':
            dynamicAttempt = 0
        elif action == 'userInputNotValid:+1':
            dynamicAttempt += 1
        if questionWrong == 3 and action == 'CheckAttemptsMadeFail':
            exit('⨉\nRestart the program.')


class Game:
    def userContentStandardQuiz(self):
        global questionWrong
        dynamicQuestionInt = 1
        General().getDisplayContentUser()
        questionIterateContinue = True
        questionWrong = 0
        while questionIterateContinue == True:
            General().getUserAttemptDynamic('CheckAttemptsMadeFail')
            General().getDisplayContentSystem('GetStandardQuizData', 'standardQuiz')
            General().getTotalLines(
                f'{userDecisionTypeMusic}.txt', 'app/lib/standard-quizes')
            if displaySong == None:
                input(
                    f'{displayFirstName}, you have completed this set of questions.\nCurrent Score is {dynamicScore}.\nPress ENTER to exit.')
                questionIterateContinue = True

            questionNotCorrect = True
            while questionNotCorrect == True:
                questionPresentUser = input(
                    f'Question {dynamicQuestionInt}\n{"-"*50}\nFirst Letter of Song: {displayFirstStringItem} | Artist: {displayArtist}\n{"-"*20}\nSong Name: ').title()
                if questionPresentUser == displaySong:
                    matchXBool = 'questionMatch:True'
                    ScoreCheck().userDynamicScoreUpdate('questionMatch:True'), ScoreCheck(
                    ).userHighScoreValidate('Check:HighScoreData')
                elif questionPresentUser == 'Exit':
                    exit(f'Thanks for playing {displayUser}!')
                else:
                    matchXBool = 'questionMatch:False'

                if matchXBool != 'questionMatch:True':
                    General().getUserAttemptDynamic('userInputNotValid:+1')
                    if dynamicAttempt == 3:
                        print('You have tried 3 times!\nMoving on...')
                        questionWrong += 1
                        General().getUserAttemptDynamic('UserInputCorrect:ResetAttempts')
                        questionNotCorrect = False
                        break
                    userInputIncorrectMoveOn = input(
                        f'You didn\'t get the answer correct. Do you want to try one more time? (Yes/No)\nYou have {3-dynamicAttempt} tr{"ies" if 3-dynamicAttempt>=2 else "y"} left before moving on.\n').title()
                    if userInputIncorrectMoveOn == 'Yes':
                        pass
                    elif userInputIncorrectMoveOn == 'No':
                        questionNotCorrect = False
                        questionWrong += 1
                        General().getUserAttemptDynamic('UserInputCorrect:ResetAttempts')
                    else:
                        print(
                            'Nothing was entered. We presume you want to try again...')

                if matchXBool == 'questionMatch:True':
                    questionPresentUserReleaseYear = input(
                        f'Do you know what year "{displaySong}" by "{displayArtist}" was released?\n{"-"*20}\nRelease Year: ')
                    if questionPresentUserReleaseYear == str(displaySongReleaseYear):
                        ScoreCheck().userDynamicScoreUpdate('releaseYearMatch:True'), ScoreCheck(
                        ).userHighScoreValidate('Check:HighScoreData')

            if questionRangeIndex == []:
                os.system('cls' if os.name == 'nt' else 'clear')
                while True:
                    endOfSetDecision = input(
                        f'{displayFirstName}, that is the end of the set! Want to play again? (yes/no)\n').lower()
                    if endOfSetDecision == 'yes':
                        Game().userContentStandardQuiz()
                    elif endOfSetDecision == 'no':
                        print(
                            f'Thanks for playing!\nRemember your username "{displayUser}" for next time!')
                        questionIterateContinue = False
                        break
                    else:
                        General().getUserAttemptDynamic('userInputNotValid:+1')

                    if endOfSetDecision != 'no':
                        questionEndDecision = input(
                            '\nPress ENTER to continue. Type "exit" to leave the program\n').lower()
                        if questionEndDecision == 'exit':
                            ScoreCheck().userHighScoreValidate('Check:HighScoreData')
                            questionIterateContinue = False
                            break
                    else:
                        General().getUserAttemptDynamic('userInputNotValid:+1')
                        questionIterateContinue = False
            dynamicQuestionInt += 1


class ScoreCheck:

    def userDynamicScoreUpdate(self, action):
        global dynamicScore
        General().getDisplayContentUser()
        if action == 'questionMatch:True':
            dynamicScore += 1
        elif action == 'releaseYearMatch:True':
            dynamicScore += 2
        elif action == 'getCurrentScore:True':
            return dynamicScore

    def userHighScoreValidate(self, action):
        General().getDisplayContentScoring('getHighScoreDB')
        General().getDisplayContentUser()
        if action == 'Check:HighScoreData':
            if displayUser == 'undefined' and displayHighScore == 'undefined':
                print(
                    'Well done! You have just set the first high score for this genre!')
                with open(f'app/lib/', 'w') as f:
                    f.write(
                        f'{currentDayValue}|{dynamicScore}|{displayUser}|{displayName}\n'), f.close()
            elif dynamicScore > displayHighScore and displayUsername == displayUser:
                print("You just beat your own score! Well done!")
                with open(f'App/Score/{userDecisionTypeMusic}.txt', 'w') as f:
                    f.write(
                        f'{currentDayValue}|{dynamicScore}|{displayUser}|{displayName}'), f.close()


class ProcessFeatures:
    def userExitLogoutForce(self):
        if os.path.isfile('auth/lib/authoUserdb.txt') and os.access('auth/lib/authoUserdb.txt', os.R_OK):
            os.remove('auth/lib/authoUserdb.txt')

    def newFileGenerate(self, fileDirectoryQuery, folderDirectoryQuery):
        with open(f'{folderDirectoryQuery}/{fileDirectoryQuery}.txt', 'w') as f:
            f.write(f'{"undefined|"*4}'), f.close()


try:
    General().UIdata()
except KeyboardInterrupt:
    # ProcessFeatures().userExitLogoutForce()
    exit('\nYou requested to force exit the program.\n{exit}')
