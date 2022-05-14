import random
import time


class Color:
    # color for text
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    YELLOW = "\033[1;33m"
    END = "\033[0m"


class War:
    def distribute_cards(self):
        # makes and distributes deck
        """
        Card Identifiers (will be printed later)
        0.1 = ♠️ spades
        0.2 = ♣️ clubs
        0.3 = ♦️ diamonds
        0.4 = ♥️ hearts
        Suits don't matter in War. However, it's useful to have this if I choose to make other games.

        11 = Jack
        12 = Queen
        13 = King
        14 = Ace
        """
        spades_deck = [i + 0.1 for i in range(2, 15)]
        clubs_deck = [i + 0.2 for i in range(2, 15)]
        diamonds_deck = [i + 0.3 for i in range(2, 15)]
        hearts_deck = [i + 0.4 for i in range(2, 15)]

        # combines all decks into one deck
        deck = spades_deck + clubs_deck + diamonds_deck + hearts_deck

        # shuffles deck
        random.shuffle(deck)

        # distributes deck. usr gets first half, cpu gets second half.
        self.usr_deck = deck[:26]
        self.cpu_deck = deck[26:]

        # returns as tuple
        return self.usr_deck, self.cpu_deck

    @staticmethod
    def format_card(num):
        # replaces decimal point with appropriate suit
        num_str = str(num)
        num_formatted = num_str.replace('.1', '♠').replace('.2', '♣').replace('.3', '♦').replace('.4', '♥')
        """
        0.1 = ♠️ spades
        0.2 = ♣️ clubs
        0.3 = ♦️ diamonds
        0.4 = ♥️ hearts
        """

        # replaces numbers greater than 10 with appropriate face card
        num_formatted = num_formatted.replace('11', 'J').replace('12', 'Q').replace('13', 'K').replace('14', 'A')
        """
        11 = Jack
        12 = Queen
        13 = King
        14 = Ace
        """

        return num_formatted

    def check_len(self):
        # checks if length is 0 and returns the winner (person who's length isn't 0)
        if self.usr_deck_len == 0:
            return "cpu"
        elif self.cpu_deck_len == 0:
            return "usr"
        else:
            return

    def draw_card(self, draw=0):
        # draw tells where in deck to draw from.

        # draws card. if not possible, it will search through stake
        try:
            self.usr_draw = self.usr_deck[draw]
        except IndexError:
            self.usr_draw = self.usr_stake[draw]
        try:
            self.cpu_draw = self.cpu_deck[draw]
        except IndexError:
            self.cpu_draw = self.cpu_stake[draw]
        # formatting cards
        self.usr_draw_formatted = self.format_card(self.usr_draw)
        self.cpu_draw_formatted = self.format_card(self.cpu_draw)

        # prints card in format
        print('usr:', self.usr_draw_formatted)
        print('cpu:', self.cpu_draw_formatted)

    def compare_card(self, is_tie_round=False):
        # compares card values and appends winnings to winner's list. also removes card from usr and cpu
        if int(self.usr_draw) > int(self.cpu_draw):
            print(Color.GREEN + 'You beat CPU!' + Color.END)

            # appends winnings to usr_deck
            self.usr_deck.append(self.usr_draw)
            self.usr_deck.append(self.cpu_draw)
            # removes cards from usr and cpu. if IndexError, skip because game will end
            try:
                self.usr_deck.pop(0)
            except IndexError:
                pass
            try:
                self.cpu_deck.pop(0)
            except IndexError:
                pass
            # updates length of usr's and cpu's deck
            self.usr_deck_len = len(self.usr_deck)
            self.cpu_deck_len = len(self.cpu_deck)

            # if is_tie_round is true, this will output who won
            if is_tie_round:
                return "usr"

        elif int(self.cpu_draw) > int(self.usr_draw):
            print(Color.RED + 'CPU beats user!' + Color.END)

            # appends winnings to cpu_deck
            self.cpu_deck.append(self.cpu_draw)
            self.cpu_deck.append(self.usr_draw)
            # removes cards from usr and cpu. if IndexError, skip because game will end
            try:
                self.usr_deck.pop(0)
            except IndexError:
                pass
            try:
                self.cpu_deck.pop(0)
            except IndexError:
                pass
            # updates length of usr's and cpu's deck
            self.usr_deck_len = len(self.usr_deck)
            self.cpu_deck_len = len(self.cpu_deck)

            # if is_tie_round is true, this will output who won
            if is_tie_round:
                return "cpu"

        elif int(self.usr_draw) == int(self.cpu_draw):
            print(Color.YELLOW + 'TIE!' + Color.END)
            if is_tie_round and (self.usr_deck_len <= 3 or self.cpu_deck_len <= 3):
                self.draw_card(1)

            time.sleep(1)  # delay put in so user can track game easier

            # usr and cpu must sacrifice 3 more cards + card that was drawn when there is a tie
            self.usr_stake += self.usr_deck[:4]
            self.cpu_stake += self.cpu_deck[:4]

            # deletes first 4 cards. If not possible, it will delete all cards
            try:
                del self.usr_deck[:4]
            except IndexError:
                del self.usr_deck[:]
            try:
                del self.cpu_deck[:4]
            except IndexError:
                del self.cpu_deck[:]

            # usr and cpu draw 1 more card to determine winner
            self.draw_card()
            winner = self.compare_card(True)

            # distributes cards to appropriate winner
            if winner == "usr":
                self.usr_deck += self.usr_stake + self.cpu_stake
                self.usr_stake = []
                self.cpu_stake = []
            elif winner == "cpu":
                self.cpu_deck += self.cpu_stake + self.usr_stake
                self.usr_stake = []
                self.cpu_stake = []

            # updates length of usr's and cpu's deck
            self.usr_deck_len = len(self.usr_deck)
            self.cpu_deck_len = len(self.cpu_deck)

        # prints how many cards usr has left.
        # is_tie_round must be false to prevent more than one print statement from printing if there is tie
        if not is_tie_round:
            print(f"You have {self.usr_deck_len} cards remaining.")
            print(f"CPU has {self.cpu_deck_len} cards remaining.")

    def __init__(self):
        # usr's and cpu's card deck
        self.usr_deck = []
        self.cpu_deck = []
        # lengths of usr and cpu's card deck. initially 26 because both start at 26 at the beginning of the game
        self.usr_deck_len = 26
        self.cpu_deck_len = 26
        # what usr and cpu will put down if there is a tie
        self.cpu_stake = []
        self.usr_stake = []

        # card that usr and cpu draw
        self.usr_draw = 0
        self.cpu_draw = 0
        self.usr_draw_formatted = ''
        self.cpu_draw_formatted = ''

    @staticmethod
    def start():
        print("Welcome to auto War!")
        game = War()
        round_counter = 1

        # assigns deck to usr and cpu after distributing cards
        game.distribute_cards()

        # loops until either user or cpu wins
        while True:
            print('\nRound', round_counter)
            # draws card
            game.draw_card()
            # compares cards
            game.compare_card()
            # checks that neither side has no cards left
            winner = game.check_len()
            if winner == "usr":
                print("\nUser wins!")
                break
            elif winner == "cpu":
                print("\nCPU wins!")
                break

            time.sleep(1)  # delays between turns so user can keep track of game easier
            round_counter += 1

        play_again = input("Play again [Y/n]?: ")
        if play_again == "Y" or play_again == "y" or play_again == "":
            game.start()
        elif play_again == "n" or play_again == "N":
            print("Program terminated.")

        print('Game over!')


War.start()
