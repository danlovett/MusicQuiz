
import linecache, random, time, sys, os
from datetime import datetime

userAttempts = 0
mGenreType = ''
day = datetime.today().strftime('%Y-%m-%d')

class Game():

    def logout(self):
        os.remove('Auth/Inc/currentUser.txt')

    def getLines(self, f_type):
        global fc_line
        fc_line = 1
        with open(f'{f_type}.txt', 'r') as f:
            for i in f:
                i
                fc_line += 1
    
    def displayData(self):
        global qInitiate, qRange
        
        Game().retrieveData(r_send_value = 'av_option')

        qInitiate = input(f"Please select from the following options to begin playing: {a_availList}\n").title()

        if qInitiate == a_availList:
            Game().getLines(f_type = f'App/Inc/{qInitiate}')
            qRange = list(range(1, fc_line))
            input(f'Okay, running {a_availList} music now.\nPress ENTER to continue.'), time.sleep(0.5), os.system('cls' if os.name=='nt' else 'clear')
            MusicHandle().displayData()
        else:
            os.system('cls' if os.name=='nt' else 'clear')
            print(f'"{qInitiate}" is not a music genre avaliable for this quiz.\nRestart the program and try again.')
        
    def retrieveData(self, r_send_value):
        global name, firstName, lastName, userName, f_song, f_artist, fs_releasey, f_song1, fs_hint1, a_availList, fl_value, f_highScore, f_userName, f_fullName, fullName

        if r_send_value == 'rc_user':
            f_type = 'Auth/Inc/currentUser'
            fl_value = 1
        elif r_send_value == 'rm_info':
            f_type = f'App/Inc/{qInitiate}'
            fl_value = int(random.choice(qRange))
            qRange.remove(fl_value)
        elif r_send_value == 'av_option':
            f_type = 'App/Inc/.avaliOption'
            fl_value = 1

        elif r_send_value == 'ch_score':
            f_type = f'App/Score/{qInitiate}'
            fl_value = 1

        if os.path.isfile(f'{f_type}.txt') and os.access(f'{f_type}.txt', os.R_OK):
            contents = linecache.getline(f'{f_type}.txt', fl_value)
            dataBlock = contents.split('|')

            if r_send_value == 'rc_user':
                name = dataBlock[0]
                userName = dataBlock[1]
                nameSplit = name.split(' ')
                firstName = nameSplit[0]
                lastName = nameSplit[1]
                f_fullName = dataBlock[0]

            elif r_send_value == 'rm_info':
                f_song = dataBlock[0]
                f_artist = dataBlock[1]
                fs_releasey = dataBlock[2]
                f_song1 = f_song[0]
                fs_hint1 = f_song[1]

            elif r_send_value == 'av_option':
                a_availList = dataBlock[0] # to be changed, allowing compile of array to string and saving to new array list n.

            elif r_send_value == 'ch_score':
                f_highScore = dataBlock[1]
                f_userName = dataBlock[2]

                linecache.clearcache()
        else:
            print('User Authorisation Failed.\nLogin first')
            exit()
    
    def userTryCount(self):
        global userAttempts

        userAttempts += 1

        if userAttempts == 3:
            print("Attempts exceeded. Try again later.")
            exit()

class MusicHandle:

    def displayData(self):
        global q_number
        hscore_send_value = False
        user_y_song = False
        q_number = 1
        pAgain = 'yes'

        Game().retrieveData(r_send_value = 'rc_user')
        
        while True:
            Game().retrieveData(r_send_value = 'rm_info')
            Game().getLines(f_type = f'App/Inc/{qInitiate}')

            if f_song == None:
                input(f'{firstName}, you have completed this set of questions.\nCurrent Score is {active_score}.\nPress ENTER to exit.')
                break

            q_user = input(f'Question {q_number}\n{"-"*50}\nFirst Letter of Song: {f_song1} | Artist: {f_artist}\n{"-"*20}\nSong Name: ').title()

            if q_user == f_song:
                Scoring().score(s_status = 'user_y_song'), Scoring().highScore(hscore_send_value, exitValue = False)
                hscore_send_value = True
                user_y_song = True

            if user_y_song == True:
                q_user = input(f'Do you know what year "{f_song}" by "{f_artist}" was released?\n{"-"*20}\nRelease Year: ')

                if q_user == str(fs_releasey):
                    Scoring().score(s_status = 'user_y_releasey'), Scoring().highScore(hscore_send_value, exitValue = False)

            if qRange == []:
                time.sleep(.5)
                os.system('cls' if os.name=='nt' else 'clear')
                while True:
                    pAgain = input(f'{firstName}, that is the end of the set! Want to play again? (yes/no)\n').lower()

                    if pAgain == 'yes':
                        Game().displayData()
                        break
                    elif pAgain == 'no':
                        print(f'Thanks for playing!\nRemember your username "{userName}" for next time!')
                        break
                    else:
                        Game().userTryCount()
                        print('error')
                        time.sleep(.2), os.system('cls' if os.name=='nt' else 'clear')
            if pAgain != 'no':
                b = input('\nPress ENTER to continue. Type "exit" to leave the program\n').lower()
                if b == 'exit':
                    os.system('cls' if os.name=='nt' else 'clear')
                    print(f'High Score update: {Scoring().highScore(hscore_send_value = False, exitValue = True)}')
                    Scoring().score(s_status = 'exit_writeDisk')
                    break
            else:
                break

            os.system('cls' if os.name=='nt' else 'clear')
            q_number += 1
        
class Scoring:

    def score(self, s_status):
        Game().retrieveData(r_send_value = 'rc_user')
        global active_score
        try:
            active_score = 0
        except NameError:
            active_score = 0
        if s_status == 'user_y_song':
            print('Song Correct') # change this wording
            active_score += 1
        elif s_status == 'user_y_releasey':
            print('R Year Correct') # change this wording
            active_score += 2
        elif s_status == 'get_score':
            return active_score

        elif s_status == 'exit_writeDisk':
            with open(f'App/Score/{qInitiate}-{userName}.txt', 'a') as f:
                f.write(f'{day}|{active_score}|{userName}|{fullName}\n')
                f.close()
        
    def highScore(self, hscore_send_value, exitValue):
        if hscore_send_value == False:
            Game().retrieveData(r_send_value = 'ch_score'), Game().retrieveData(r_send_value = 'rc_user'), Scoring().score(s_status = 'get_score')
            if f_userName == 'undefined' and f_highScore == 'undefined':
                print(f'Well done! You, {firstName}, have just set the first high score for this genre!')
                with open(f'App/Score/{qInitiate}.txt', 'w') as f:
                    f.write(f'{day}|{active_score}|{userName}|{f_fullName}\n')
                    f.close()
                time.sleep(4)
            
            elif active_score > int(f_highScore) and f_userName == userName:
                print("You just beat your own score! Well done!")
                with open(f'App/Score/{qInitiate}.txt', 'w') as f:
                    f.write(f'{day}|{active_score}|{userName}|{fullName}')
                    f.close()
                time.sleep(2)
            elif exitValue == True:
                print('No highscore\'s beaten. Try again another day.')
                
        elif active_score > int(f_highScore) and f_userName != userName:
                print(f'Well done! you just over took {f_userName} (AKA "{f_fullName}") with your highscore: {active_score} (their\'s was {f_highScore}).')
                with open(f'App/Score/{qInitiate}.txt', 'w') as f:
                    f.write(f'{day}|{active_score}|{userName}|{fullName}')
                    f.close()
                time.sleep(4)


Game().retrieveData(r_send_value = 'rc_user')
if userName == 'danlovett':
    resetInfo = input('Reset data? (reset)\n')
    if resetInfo == 'reset':
        with open('App/Score/Pop.txt', 'w') as f:
            f.write('undefined|'*4)
            f.close()
        exit('Complete.')
    else:
        pass

Game().displayData()
Game().logout()

exit(f'Goodbye, {firstName}')