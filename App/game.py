## To use classes ##
# ### LOOKING TO THE FUTURE: Gather Music from Spotify using API, then output to user. Possibly provide music sample?
# Add Lyric option if song name unknown
# Explore the possibilites of MusicQuizzing
# ###

# IMPORT LIB
import linecache, random, time, sys, os

# Initialise Var GLOBAL VALUES (outside of class on 'vanila' code)
userAttempts = 0
mGenreType = ''

## CLASS Game ##
class Game:

    def getLines(self, f_type):
        global fc_line
        fc_line = 0
        with open(f'App/Inc/{f_type}.txt', 'r') as f:
            for i in f:
                i
                fc_line += 1

    def displayData(self):
        global qInitiate

        Game().retrieveData(r_send_value = 'rc_user'), Game().retrieveData(r_send_value = 'av_option')

        qInitiate = input(f"Hello {firstName}.\nPlease select from the following options to begin playing: {A_availList}\n").title()

        if qInitiate == A_availList:
            MusicHandle().displayData()

    def retrieveData(self, r_send_value):
        global name, firstName, lastName, userName, f_song, mGenreType, f_artist, fs_releasey, f_song1, fs_hint1, A_availList

        if r_send_value == 'rc_user':
            f_type = 'currentUser'
            folder = 'Auth'
            fl_value = 1
        elif r_send_value == 'rm_info':
            f_type = qInitiate
            Game().getLines(f_type)
            folder = 'App'
            fl_value = random.randint(0, fc_line)
        elif r_send_value == 'av_option':
            f_type = '.avaliOption'
            folder = 'App'
            fl_value = 1


        contents = linecache.getline(f'{folder}/Inc/{f_type}.txt', fl_value)
        dataBlock = contents.split('|')

        if r_send_value == 'rc_user':
            name = dataBlock[0]
            userName = dataBlock[1]

            nameSplit = name.split(' ')
            firstName = nameSplit[0]
            lastName = nameSplit[1]
        elif r_send_value == 'rm_info':
            f_song = dataBlock[0]
            f_artist = dataBlock[1]
            fs_releasey = dataBlock[2]

            f_song1 = f_song[0]
            fs_hint1 = f_song[1]
        elif r_send_value == 'av_option':
            A_availList = dataBlock[0] # to be changed, allowing compile of array to string and saving to new array list n.
        
        linecache.clearcache()

    def userTryCount(self):
        global userAttempts

        userAttempts += 1

        if userAttempts == 3:
            print("Attempts exceeded. Try again later.")
            exit(time.sleep(3))


## CLASS MusicHandle ##
class MusicHandle:
    def displayData(self):
        global q_number
        q_number = 1
        while True:
            Game().retrieveData(r_send_value = 'rm_info')
            q_user = input(f'Question {q_number}\n{"-"*50}\nFirst Letter of Song: {f_song1} | Artist: {f_artist}\n{"-"*20}\nSong Name: ').title()

            if q_user == f_song:
                print(f'{firstName}, It is CORRECT!')# SCORING REDIR + 1 CORRECT
                Scoring().calcScore(s_status = 'user_y_song')
            else:
                print(f'{firstName}, It is wrong!')
                

            q_number += 1
    # DEF compileDupMusicQ (Duplicate music, create a sub-folder for user then destroy lines, allowing for the q to only appear once)

## CLASS Scoring ##
class Scoring:

    # DEF retireveHighscore

    def calcScore(self, s_status):
        if q_number == 1:
            active_score = 0
        if s_status == 'user_y_song':
            # song correct, award 1
            active_score += 1
        elif s_status == 'user_y_rYear':
            # Release year correct, award + 1
            active_score += 1

    # DEF passToFile (Pass current score to the file, update it everytime a q is answered)
## CLASS Error&Validation ##
class ErrorValidation:
    pass


## CLASS Console (writes user actions to console for better logging) ## LATE IMPLEMENTATION (low Priority)

### MAIN CODE:INIT ###

Game().displayData()