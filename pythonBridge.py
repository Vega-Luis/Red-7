"""
Created on Wed Oct 21 10:15:19 2020

@author: marcos
"""
import math

from pyswip import *
from tkinter import ttk
from tkinter import Tk
from tkinter import Button
from tkinter import Label
from tkinter import StringVar
from tkinter import PhotoImage
from tkinter import messagebox
from PIL import Image

class Player:
    def __init__(self):
        self.cardImages = []
        self.deck = []
        self.playedCards = []
        self.score = 0
        self.btns = []
        self.out = False

#Game constants
PATH = 'game.pl'
RULES = ['below4Rule','run','diferentColor','pairRule','sameColorRule','sameNumberRule','highestRule']

#Variables
prolog = Prolog()
prolog.consult(PATH)
players = []
currentRule = [RULES[6]]
currentRuleImg = []
playerTurn = []
checkBox = []
maxScore = []

#gets the current max score of the game
def getMaxScore(pPlayerIndex):
    maxScore = 0
    cont = 0
    for player in players:
        if(player.out == False and pPlayerIndex != cont):
            maxScore = max(maxScore, player.score)
        cont += 1
    return maxScore

def checkWin(pGameWindow):
    cont = 0
    for player in players:
        if(player.out == True):
            cont += 1
    if (cont == len(players ) - 1):
        messagebox.showinfo('Ganó c:')
        pGameWindow.destroy()

#choose the player on the left of the player with max score to begin the game
def chooseFirstPlayer(pGameWindow):
    index = 0
    tempIndex = 0
    score = 0
    for player in players:
        tempMax = max(score, player.score)
        if(tempMax != score):
            score = tempMax
            index = tempIndex
        tempIndex += 1
    scoreLbl = Label(pGameWindow, text = 'El jugador '+str(index)+'\n va ganando con \n un Score de: '+str(players[index].score))
    scoreLbl.lift
    scoreLbl.grid(row = 0, column = 0)
    maxScore.append(scoreLbl)
    return index + 1
        
def changePlayerRule(pCardIndex, pGameWindow):
    Rule = Variable()
    Color = Variable()
    color = Functor('getColor', 2)
    q = Query(color(players[0].deck[pCardIndex], Color))
    while q.nextSolution():
        Color = int(Color.value) 
    q.closeQuery()
    rule = Functor('colorRule', 2)
    q = Query(rule(Color, Rule))
    while q.nextSolution():
        Rule = str(Rule.value)
    q.closeQuery()
    updateRule(Rule, pGameWindow)
    if(players[0].score < getMaxScore(0) or not(checkDraws(0))):
        messagebox.showinfo('Perdió :c')
        pGameWindow.destroy()
    else:
        playGame(pGameWindow)

"""
executes a move
@pCurrentRule current rule
@pPlayerNumber index of the player that is going to do the move
@pCardIndex index of the card choosed by the player
"""
def executeMovement(pPlayerNumber, pCardIndex, pGameWindow, pIsPlayer):
    if(pIsPlayer):
        players[0].btns[pCardIndex].config(state="disabled")
        if(checkBox[0].instate(['selected'])):
            changePlayerRule(pCardIndex, pGameWindow)
            return
    game = Functor('game', 7)
    Score = Variable()
    NewDeck = Variable()
    NewDeckPlayed = Variable()
    q = Query(game(currentRule[0], players[pPlayerNumber].deck, pCardIndex, players[pPlayerNumber].playedCards, Score, NewDeck, NewDeckPlayed))
    while q.nextSolution():
        players[pPlayerNumber].score = Score.value
        players[pPlayerNumber].playedCards = list(NewDeckPlayed.value)
        if(pPlayerNumber != 0):
            players[pPlayerNumber].deck = list(NewDeck.value)     
    q.closeQuery()
    placePlayedCard(pPlayerNumber, pGameWindow)
    scoreLbl = Label(pGameWindow, text = 'El jugador '+str(pPlayerNumber % len(players))+'\n va ganando con \n un Score de: '+str(players[pPlayerNumber].score))
    scoreLbl.lift
    scoreLbl.grid(row = 0, column = 0)
    maxScore.append(scoreLbl)
    if(pPlayerNumber == 0):
        if(players[0].score < getMaxScore(0) or not(checkDraws(0))):
            messagebox.showinfo('Perdió :c')
            pGameWindow.destroy()
        else:
            playGame(pGameWindow)

def updateScores(pRule):
    for player in players:
        Score = Variable()
        rule = Functor('rule', 3)
        q = Query(rule(pRule, player.playedCards, Score))
        while q.nextSolution(): 
            player.score = int(Score.value)
        q.closeQuery()

def getPlayersCards(pIndex):
    cont = 0
    cards = []
    for player in players:
        if cont != pIndex:
            cards.append(player.playedCards)
        cont += 1
    return cards

def updateRule(pRule, pGameWindow):
    updateScores(pRule)
    currentRule[0] = pRule
    index = RULES.index(currentRule[0]) + 1
    color = Functor('color',2)
    Color = Variable()
    q = Query(color(Color, index))
    while q.nextSolution():
        Color = str(Color.value)
    q.closeQuery()
    updateRuleImage(Color)
    Label(pGameWindow, text = "", image = currentRuleImg[-1]).grid(row = 4, column = 4)

def updateRuleImage(pColorName):
    background = Image.open('sources/' + pColorName + '.png', 'r')
    backGroundsize = 64,64
    background.thumbnail(backGroundsize, Image.ANTIALIAS)
    background.save('currentRule.png')
    currentRuleImg.append(PhotoImage(file = r'currentRule.png'))

def deletePlayer(pIndex):
    players[pIndex].out = True
    players[pIndex].cardImages = 0

def IAMove(pPlayerNumber, pGameWindow):
    nextMove = Functor('nextMove', 7)
    CardIndex = Variable()
    NewRule = Variable()
    maxScore = getMaxScore(pPlayerNumber)
    playersCards = getPlayersCards(pPlayerNumber)
    q = Query(nextMove(currentRule[0], playersCards, players[pPlayerNumber].deck, players[pPlayerNumber].playedCards, maxScore, CardIndex, NewRule))
    while q.nextSolution():
        if(isinstance(CardIndex, int) == False):
            CardIndex = int(CardIndex.value)
            print('CardIndex:'+str(CardIndex))
        if(isinstance(NewRule, str) == False):
            NewRule = str(NewRule.value)
    q.closeQuery()
    print(NewRule)
    if(CardIndex == -1 or not(checkDraws(pPlayerNumber))):
        messagebox.showinfo('El jugador'+str(pPlayerNumber % len(players))+' ha perdido :(')
        deletePlayer(pPlayerNumber % len(players))
        checkWin(pGameWindow)
    else:
        if(currentRule[0] != NewRule):
            messagebox.showinfo('El jugador'+str(pPlayerNumber % len(players))+' ha cambiado la regla actual')
            updateRule(NewRule, pGameWindow)
        else:
            executeMovement(pPlayerNumber, CardIndex, pGameWindow, False)

"""
Checks if theres a tie, return False if the current player wins
"""
def checkDraws(pPlayerNumber):
    score = getMaxScore(5)
    maxIndex = 0
    newPlayerIndex = 0
    tied = []
    cont = 0
    for player in players:
        if(player.score == score):
            tied.append(player.playedCards)
            if(cont == pPlayerNumber):
                newPlayerIndex = len(tied) - 1
        cont += 1
    if(len(tied) > 1):
        tieBreaker = Functor('tieBreaker', 2)
        Winner = Variable()
        q = Query(tieBreaker(tied, Winner))
        while q.nextSolution():
            maxIndex = int(Winner.value)
        q.closeQuery()
        return maxIndex == newPlayerIndex
    return True

def initGame(pPlayerQuantity):
    Decks = Variable()
    generateDeck = Functor('generateDeck', 2)
    rule = Functor('rule', 3)
    q = Query(generateDeck(pPlayerQuantity, Decks))
    while q.nextSolution(): 
        Decks = (list(Decks.value))
    q.closeQuery()
    for item in Decks:
        player = Player()
        player.deck = item[:7]
        player.playedCards.append(item[-1])
        Score = Variable()
        q = Query(rule(currentRule[0], player.playedCards, Score))
        while q.nextSolution(): 
            player.score = int(Score.value)
        q.closeQuery()
        players.append(player)

def playGame(pGameWindow):
    for i in range(len(players)):
        playerTurn[0] %= (len(players))
        if(playerTurn[0] == 0):
            playerTurn[0] += 1
            break
        if(players[playerTurn[0]].out == False):
            IAMove(playerTurn[0], pGameWindow)
        playerTurn[0] += 1

def generateCardImage(pBackground, pNumber):
    numberSize = 16, 16
    number = Image.open('sources/' + pNumber + '.png', 'r')
    number.thumbnail(numberSize, Image.ANTIALIAS)
    numberWidth, numberHeight = number.size
    background = Image.open('sources/' + pBackground + '.png', 'r')
    backGroundsize = 64,64
    background.thumbnail(backGroundsize, Image.ANTIALIAS)
    bgWidth, bgHeight = background.size
    offset = ((bgWidth - numberWidth) // 2, (bgHeight - numberHeight) // 2)
    background.paste(number, offset, number)
    background.save('card.png')

def updateWidget(pWidget):
    text = StringVar()
    text.set("Text")
    pWidget.config(textvariable=text)  # anadimos una variable de texto

def menu():
    menuWindow = Tk()
    menuWindow.title("Menu")
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
    playerTurn.append(chooseFirstPlayer(gameWindow))
    checkBox.append(ttk.Checkbutton(gameWindow, text="CambiarRegla"))
    checkBox[0].grid(row = 0, column = 10)
    generatePlayerCards(gameWindow)
    updateRuleImage('red')
    Label(gameWindow, image = currentRuleImg[-1]).grid(row = 4, column = 4)
    playGame(gameWindow)
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
    lbl.grid(row = playerRow, column = playerColumn, columnspan = 1)

def generatePlayerCards(pGameWindow):
    for i in range(len(players[0].deck)):
        generateCardImage(getCardColorName(players[0].deck[i]), getCardNumber(players[0].deck[i]))
        players[0].cardImages.append(PhotoImage(file = r'card.png'))
        btn = Button(pGameWindow, text = '', image = players[0].cardImages[i] , command = lambda tmpRow = 0, tmpColumn = i: executeMovement(tmpRow, tmpColumn, pGameWindow, True))
        btn.grid(row = 0, column = i+1)
        players[0].btns.append(btn)
    for i in range(len(players)):
        placePlayedCard(i, pGameWindow)

if __name__ == "__main__":
    menu()
