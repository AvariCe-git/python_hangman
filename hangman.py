import random, os, json

class hangman:

    def __init__(self, word):
        self.word = word
        self.masked_word = ''

    def mask(self):
        for i in range(len(self.word)):
            self.masked_word += '_'

    def game(self):
        
        inp             = ''
        counter         = 0
        failed_attempts = []
        found_char      = False

        self.mask()
        self.print_lines(failed_attempts,counter)

        while '_' in self.masked_word and counter <= 6:
            
            inp = input('Give a guess: ').lower()

            if inp == '':
                print(f'You missclick often and with great pleasure')
            elif ( len(inp) != 1) or (not inp.isalpha()):
                print (f'Give a single character')
                self.print_lines(failed_attempts,counter)
                continue
            elif inp in failed_attempts:
                print (f'Give a different guess')
                self.print_lines(failed_attempts,counter)
                continue
            elif inp in self.masked_word.lower():
                print (f'You\'ve already found this letter')
                self.print_lines(failed_attempts,counter)
                continue

            found_char = False

            for i in range(len(self.word)):
                if self.word[i].lower() == inp:
                    self.masked_word = f'{self.masked_word[:i]}{self.word[i]}{self.masked_word[i+1:]}'
                    found_char = True

            if not found_char:
                counter += 1 
                print(f"Wrong guess")
                failed_attempts.append(inp)
            self.print_lines(failed_attempts,counter)

    def check_win(self):      

        if '_' in self.masked_word:
            print (f'You suck. The word was {self.word}')
            return False

        else:
            print (f'You suck, but at least you won')
            return True

    def print_lines(self,attempts,counter):
        lines =    [f'       \n       \n        \n       \n        ',
                    f' +---+ \n |     \n |      \n |     \n===     ',
                    f' +---+ \n |   O \n |      \n |     \n===     ',
                    f' +---+ \n |   O \n |   |  \n |     \n===     ',
                    f' +---+ \n |   O \n |  /|  \n |     \n===     ',
                    f' +---+ \n |   O \n |  /|\\\n |     \n===     ',
                    f' +---+ \n |   O \n |  /|\\\n |    \\\n===    ',
                    f' +---+ \n |   O \n |  /|\\\n |  / \\\n===    ']

        print(lines[counter])
        
        print(self.masked_word)

        if len(attempts) > 0:
            print (f"Failed attempts:", end = ' ')
            for i in range(len(attempts)-1):
                print(attempts[i], end = ', ')
            print(attempts[-1])

def read_file():
    
    word_list = []
    stats     = {'wins':  0,
                'losses': 0,
                'total':  0}

    try:
        with open('wordlist.txt','r') as words_file:
            word_list = words_file.readlines()
    except IOError:
        print(f'wordlist.txt not found')
        exit()
    except:
        print(f'Something fucked up is going on with the wordlist, I\'m outta here')
        exit()

    try:
        if os.stat('stats.txt').st_size > 0:
            print(f'Welcome back!')
            
            with open ('stats.txt','r') as stats_file:
                try:
                    stats = json.loads(stats_file.read())
                    p_win  = stats['wins']   * 100 / stats['total'] 
                    p_loss = stats['losses'] * 100 / stats['total'] 

                    if (stats['wins'] > stats ['total']) or (stats['losses'] > stats['total']) or (p_win + p_loss < 99.9) or (p_win + p_loss > 100.1):
                        stats['wins']   = 0
                        stats['losses'] = 0
                        stats['total'] += 1

                    print(f'You\'ve played  {stats["total"]} games')
                    print(f'You\'ve won  {stats["wins"]} games, {str(round(p_win,2))} % of the total games')
                    print(f'You\'ve lost {stats["losses"]} games, {str(round(p_loss,2))} % of the total games')
                
                except:
                    print(f'Stats file is corrupted, deleting stats')
                    with open('stats.txt','w') as stats_file:
                        stats_file.write(json.dumps(stats))

    except IOError:
        print(f'This is your first time playing. Welcome to hell!')
    
    return word_list,stats

def play_game():

    play_game = True
    
    word_list, stats = read_file()

    while play_game:

        i =  random.randint(0, len(word_list)-1)
        wotd = hangman(word_list[i].replace('\n', ''))
        wotd.game()
        
        if wotd.check_win():
            stats['wins']   += 1
        else:
            stats['losses'] += 1
        stats['total']      += 1

        print(f'Total games: {stats["total"]}, Wins: {stats["wins"]}, Losses: {stats["losses"]}')
        print (f'Do you want to continue?')
        inp = input(f'Press y for yes, anything else to quit: ').lower()
        
        if inp != 'y':
            with open('stats.txt','w') as stats_file:
                stats_file.write(json.dumps(stats))
            play_game = False
        else:
            del wotd

play_game()