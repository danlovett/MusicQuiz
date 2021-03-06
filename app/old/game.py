import linecache
import random
import time as t
import os
from datetime import datetime
u_attempt, mGenreType, day = 0, '', datetime.today().strftime('%Y-%m-%d')


class Game():

    def logout(self):
        os.remove('Auth/Inc/currentUser.txt')
        exit(f'Goodbye, {firstName}')

    def totline(self, f_type):
        global line
        line = 1
        with open(f'{f_type}.txt', 'r') as f:
            for i in f:
                line += 1
            i

    def UIdata(self):
        global q, qrg
        Game().sys_data(r_redir='options')
        q = input(
            f"Please select from the following options to begin playing: {sys_genre}\n").title()
        if q == sys_genre:
            Game().totline(f_type=f'App/Inc/{q}')
            qrg = list(range(1, line))
            input(f'Okay, running {sys_genre} music now.\nPress ENTER to continue.'), t.sleep(
                0.5), os.system('cls' if os.name == 'nt' else 'clear'), Music().UIdata()
        else:
            os.system('cls' if os.name == 'nt' else 'clear'), print(
                f'"{q}" is not a music genre avaliable for this quiz.\nRestart the program and try again.')

    def sys_data(self, r_redir):
        global name, firstName, lastName, userName, sys_song, sys_artist, sys_releaseY, sys_fStrSong, sys_hint, sys_genre, rd_line, sys_highScore, sys_userName, sys_fullName

        if r_redir == 'rc_u':
            f_type = 'auth/lib/authoUserdb'
            rd_line = 1
        elif r_redir == 'r_music':
            f_type = f'App/Inc/{q}'
            rd_line = int(random.choice(qrg))
            qrg.remove(rd_line)
        elif r_redir == 'options':
            f_type = 'App/Inc/.avaliOption'
            rd_line = 1
        elif r_redir == 'rh_scr':
            f_type = f'App/Score/{q}'
            rd_line = 1

        if os.path.isfile(f'{f_type}.txt') and os.access(f'{f_type}.txt', os.R_OK):
            contents = linecache.getline(f'{f_type}.txt', rd_line)
            dataBlock = contents.split('|')

            if r_redir == 'rc_u':
                name, userName = dataBlock[0], dataBlock[1]
                nameSplit = name.split(' ')
                firstName, lastName, sys_fullName = nameSplit[0], nameSplit[1], dataBlock[0]
            elif r_redir == 'r_music':
                sys_song = dataBlock[0]
                sys_artist = dataBlock[1]
                sys_releaseY = dataBlock[2]
                sys_fStrSong = sys_song[0]
                sys_hint = sys_song[1]
            elif r_redir == 'options':
                # to be changed, allowing compile of array to string and saving to new array list n.
                sys_genre = dataBlock[0]
            elif r_redir == 'rh_scr':
                sys_highScore = dataBlock[1]
                sys_userName = dataBlock[2]
                linecache.clearcache()
        else:
            print(
                'User Authentification Failed.\nLogin First.\n\nError Code: AUTH_ERROR'), exit()

    def attempt(self):
        global u_attempt
        u_attempt += 1
        if u_attempt == 3:
            print("Attempts exceeded. Try again later."), exit()


class Music:

    def UIdata(self):
        global q_num
        bt, r_redir, song_c, q_num, pa_y = False, False, False, 1, 'yes'
        Game().sys_data(r_redir='rc_u')
        while bt == False:
            Game().sys_data(r_redir='r_music')
            Game().totline(f_type=f'App/Inc/{q}')
            if sys_song == None:
                input(
                    f'{firstName}, you have completed this set of questions.\nCurrent Score is {score}.\nPress ENTER to exit.')
                bt = True

            q_u = input(
                f'Question {q_num}\n{"-"*50}\nFirst Letter of Song: {sys_fStrSong} | Artist: {sys_artist}\n{"-"*20}\nSong Name: ').title()
            if q_u == sys_song:
                Scoring().score(r_redir='song_c'), Scoring().highscore(r_redir, xvl=False)
                r_redir, song_c = True, True
            elif q_u == 'Exit':
                bt = True, print(f'Thanks for playing {userName}!')

            if song_c == True:
                qu = input(
                    f'Do you know what year "{sys_song}" by "{sys_artist}" was released?\n{"-"*20}\nRelease Year: ')
                if qu == str(sys_releaseY):
                    Scoring().score(r_redir='ry_c'), Scoring().highscore(hscore=True, xvl=False)

            if qrg == []:
                t.sleep(.5)
                os.system('cls' if os.name == 'nt' else 'clear')
                btNest = False
                while btNest == False:
                    pa_y = input(
                        f'{firstName}, that is the end of the set! Want to play again? (yes/no)\n').lower()
                    if pa_y == 'yes':
                        btNest = True, Game().UIdata()
                    elif pa_y == 'no':
                        bt = True
                        btNest = True
                        print(
                            f'Thanks for playing!\nRemember your username "{userName}" for next time!')
                    else:
                        Game().attempt(), print('error'), t.sleep(.2), os.system(
                            'cls' if os.name == 'nt' else 'clear')

                    if pa_y != 'no':
                        b = input(
                            '\nPress ENTER to continue. Type "exit" to leave the program\n').lower()
                        if b == 'exit':
                            os.system('cls' if os.name == 'nt' else 'clear')
                            print(f'High Score update:')
                            Scoring().highscore(hscore=False, xvl=True), Scoring().score(r_redir='x_wrdsk')
                            bt = True
                    else:
                        btNest = True
            os.system('cls' if os.name == 'nt' else 'clear')
            q_num += 1


class Scoring:

    def score(self, r_redir):
        Game().sys_data(r_redir='rc_u')
        global score
        try:
            score = 0
        except NameError:
            score = 0
        if r_redir == 'song_c':
            score += 1
            print('Song Correct')  # change this wording
        elif r_redir == 'ry_c':
            score += 2
            print('R Year Correct')  # change this wording
        elif r_redir == 'g_scr':
            return score
        elif r_redir == 'x_wrdsk':
            with open(f'App/Score/{q}-{userName}.txt', 'a') as f:
                f.write(f'{day}|{score}|{userName}|{sys_fullName}\n')
                f.close()

    def highscore(self, hscore, xvl):
        Game().sys_data(r_redir='rh_scr')
        if hscore == False:
            Game().sys_data(r_redir='rh_scr'), Game().sys_data(
                r_redir='rc_u'), Scoring().score(r_redir='s_scr')
            if sys_userName == 'undefined' and sys_highScore == 'undefined':
                print(
                    'Well done! You have just set the first high score for this genre!')
                with open(f'App/Score/{q}.txt', 'w') as f:
                    f.write(f'{day}|{score}|{userName}|{sys_fullName}\n')
                    f.close()
                t.sleep(4)
            elif score > int(sys_highScore) and sys_userName == userName:
                print("You just beat your own score! Well done!")
                with open(f'App/Score/{q}.txt', 'w') as f:
                    f.write(f'{day}|{score}|{userName}|{sys_fullName}')
                    f.close()
                t.sleep(2)
            elif xvl == True:
                print('No highscore\'s beaten. Try again another day.')
        elif score > int(sys_highScore) and sys_userName != userName:
            print(
                f'Well done! you just over took {sys_userName} (AKA "{sys_fullName}") with your highscore: {score} (their\'s was {sys_highScore}).')
            with open(f'App/Score/{q}.txt', 'w') as f:
                f.write(f'{day}|{score}|{userName}|{sys_fullName}')
                f.close()
            t.sleep(4)


try:
    Game().sys_data(r_redir='rc_u')
    if userName == 'danlovett':
        r = input('Reset data? (reset)\n').lower()
        if r == 'reset':
            with open('App/Score/Pop.txt', 'w') as f:
                f.write('undefined|'*4), f.close()
            exit('Complete.')
    Game().UIdata(), Game().logout()

except KeyboardInterrupt:
    print()
    Game().logout()
