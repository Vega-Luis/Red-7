"""
Created on Wed Oct 21 10:15:19 2020

@author: marcos
"""
from pyswip import *
from tkinter import ttk
from tkinter import Tk
from tkinter import Button
from tkinter import Label
from tkinter import StringVar
from tkinter import PhotoImage
from PIL import Image

class Player:
    def __init__(self):
        self.cardImages = []
        self.deck = []
        self.playedCards = []
        self.score = 0

#Game constants
PATH = 'game.pl'
RULES = ['below4Rule','run','diferentColor','pairRule','sameColorRule','sameNumberRule','highestRule']

#Variables
prolog = Prolog()
prolog.consult(PATH)
players = []
currentRule = RULES[6]
#gets the current max score of the game
def getMaxScore():
    maxScore = 0
    for player in players:
        maxScore = max(maxScore, player.score)
    return maxScore

#choose the player on the left of the player with max score to begin the game
def chooseFirstPlayer():
    index = 0
    tempIndex = 0
    maxScore = 0
    for player in players:
        tempMax = max(maxScore, player.score)
        if(tempMax != maxScore):
            maxScore = tempMax
            index = tempIndex
        tempIndex += 1
    return index - 1 
        
def prologQuery():
    res = prolog.query('like_fried_chicken(basten)')
    if(bool(list(res))): 
        print('yes')
    else:
        print('no')

"""
executes a move
@pCurrentRule current rule
@pPlayerNumber index of the player that is going to do the move
@pCardIndex index of the card choosed by the player
"""
def executeMovement(pPlayerNumber, pCardIndex):
    #prolog.consult("iaBehavior.pl")
    game = Functor('game', 7)
    Score = Variable()
    NewDeck = Variable()
    NewDeckPlayed = Variable()
    q = Query(game(currentRule, players[pPlayerNumber].deck, pCardIndex, players[pPlayerNumber].playedCards, Score, NewDeck, NewDeckPlayed))
    while q.nextSolution():
        players[pPlayerNumber].score = Score.value
        players[pPlayerNumber].deck = list(NewDeck.value)
        players[pPlayerNumber].playedCards = list(NewDeckPlayed.value)
    q.closeQuery()
    print(players[pPlayerNumber].playedCards)
    print('Score:'+str(players[pPlayerNumber].score))

def IAMove(pPlayerNumber):
    nextMove = Functor('nextMove', 7)
    CardIndex = Variable()
    NewRule = Variable()
    maxScore = getMaxScore()
    q = Query(nextMove(currentRule, RULES, players[pPlayerNumber].deck, players[pPlayerNumber].playedCards, maxScore, CardIndex, NewRule))
    while q.nextSolution():
        CardIndex = int(CardIndex.value)
        print("Index " + str(CardIndex))
        NewRule = str(NewRule.value)
    q.closeQuery()
    return [CardIndex, NewRule]

def initGame(pPlayerQuantity):
    Decks = Variable()
    generateDeck = Functor('generateDeck', 2)
    q = Query(generateDeck(pPlayerQuantity, Decks))
    while q.nextSolution(): 
        Decks = (list(Decks.value))
    for item in Decks:
        player = Player()
        player.deck = item[:7]
        print(item[:7])
        print(item[-1])
        player.playedCards.append(item[-1])
        players.append(player)
    q.closeQuery()

def playGame():
    playerTurn = chooseFirstPlayer()
    CARD_INDEX = 0
    CURR_RULE = 1
    while(len(players) != 1):
        move = [0, currentRule]
        playerNumber = playerTurn % 3
        print(players[playerNumber].deck)
        if(playerNumber == 0):
            print("Elija su carta")
            move[CARD_INDEX] = int(input())
        else:
            move = IAMove(move[CURR_RULE], playerNumber)
        executeMovement(move[CURR_RULE], playerNumber, move[CARD_INDEX])
        playerTurn -= 1

def generateCardImage(pBackground, pNumber):
    numberSize = 32, 32
    number = Image.open('sources/' + pNumber + '.png', 'r')
    number.thumbnail(numberSize, Image.ANTIALIAS)
    numberWidth, numberHeight = number.size
    background = Image.open('sources/' + pBackground + '.png', 'r')
    backGroundsize = 128,128
    background.thumbnail(backGroundsize, Image.ANTIALIAS)
    bgWidth, bgHeight = background.size
    offset = ((bgWidth - numberWidth) // 2, (bgHeight - numberHeight) // 2)
    background.paste(number, offset, number)
    background.save('card.png')

def updateWidget(pWidget):
    text = StringVar()
    text.set("Text")
    pWidget.config(textvariable=text)  # añadimos una variable de texto

def menu():
    menuWindow = Tk()
    menuWindow.title("Menú")
    exitBtn = Button(menuWindow, text = "Salir", command = lambda: menuWindow.destroy())
    playBtn = Button(menuWindow, text = "Jugar", command = lambda: gameWindow(menuWindow, playersOptions.get()))
    playersOptions = ttk.Combobox(menuWindow, state="readonly")
    playersOptions["values"] = [2, 3, 4]
    playBtn.pack()
    exitBtn.pack()
    playersOptions.pack()
    menuWindow.mainloop()
    
def gameWindow(pMainWindow, pPlayerQuantity):
    pMainWindow.destroy()
    initGame(int(pPlayerQuantity))
    gameWindow = Tk()
    generatePlayerCards(gameWindow)
    gameWindow.mainloop()

def getCardColorName(pCard):
    getCardColorName = Functor('getCardColorName', 2)
    ColorName = Variable()
    q = Query(getCardColorName(pCard, ColorName))
    while q.nextSolution():
        ColorName = str(ColorName.value)
    q.closeQuery()
    return ColorName

def getCardNumber(pCard):
    getCardColorName = Functor('getCardNumber', 2)
    Number = Variable()
    q = Query(getCardColorName(pCard, Number))
    while q.nextSolution():
        Number = str(Number.value)
    q.closeQuery()
    return Number

def placePlayedCard(pPlayerIndex, pGameWindow):
    playerRow = 0
    playerColumn = 0
    generateCardImage(getCardColorName(players[pPlayerIndex].playedCards[-1]), getCardNumber(players[pPlayerIndex].playedCards[-1]))
    players[pPlayerIndex].cardImages.append(PhotoImage(file = r'card.png'))
    if(pPlayerIndex == 0):
        playerRow = 1
        playerColumn =  len(players[pPlayerIndex].playedCards)
    else:
        if(pPlayerIndex == 1):
            playerRow = len(players[pPlayerIndex].playedCards) + 1
            playerColumn = 8
        elif(pPlayerIndex == 2):
            playerRow = 8
            playerColumn = len(players[pPlayerIndex].playedCards)
        else:
            playerRow = len(players[pPlayerIndex].playedCards) + 1
            playerColumn = 0
    lbl = Label(pGameWindow, text = str(pPlayerIndex), image = players[pPlayerIndex].cardImages[-1])
    lbl2 = Label(pGameWindow, text = "Score")
    lbl2.grid(row = 0, column = 0)
    lbl.grid(row = playerRow, column = playerColumn, columnspan = 1)

def generatePlayerCards(pGameWindow):
    for i in range(len(players[0].deck)):
        generateCardImage(getCardColorName(players[0].deck[i]), getCardNumber(players[0].deck[i]))
        players[0].cardImages.append(PhotoImage(file = r'card.png'))
        btn = Button(pGameWindow, text = '', image = players[0].cardImages[i] , command = lambda: executeMovement(0, i))
        btn.grid(row = 0, column = i+1)
    for i in range(len(players)):
        placePlayedCard(i, pGameWindow)

if __name__ == "__main__":
    menu()
    #initGame(3)
    #playGame()
