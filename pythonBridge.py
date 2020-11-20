# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 10:15:19 2020

@author: marcos
"""
from pyswip import *

class Player:
    def __init__(self):
        self.deck = []
        self.playedCards = []
        self.score = 0

#Game constants
PATH = 'game.pl'
RULES = ['below4Rule','run','diferentColor','pairRule','yellow','sameNumberRule','highestRule']

#Variables
prolog = Prolog()
prolog.consult(PATH)
players = []

def prologQuery():
    res = prolog.query('like_fried_chicken(basten)')
    if(bool(list(res))): 
        print('yes')
    else:
        print('no')

def initGame(playerQuantity):
    Decks = Variable()
    generateDeck = Functor('generateDeck', 2)
    q = Query(generateDeck(playerQuantity, Decks))
    while q.nextSolution(): 
        Decks = (list(Decks.value))
    for item in Decks:
        player = Player()
        player.deck = item
        players.append(player)
    q.closeQuery()

def playGame():
    currentRule = RULES[6]
    """
    Score = Variable()
    rule = Functor("rule", 3)
    q = Query(rule(RULES[0], playerPlayedCards, Score))
    while q.nextSolution():
        print(Score.value)
    q.closeQuery()
    """
    playerTurn = 0
    game = Functor('game', 7)
    while(len(players) != 1):
        playerNumber = playerTurn % 3
        if(playerNumber == 0):
            print(players[playerNumber].deck)
            print("Elija su carta")
            cardIndex = int(input())
            Score = Variable()
            NewDeck = Variable()
            NewDeckPlayed = Variable()
            q = Query(game('below4Rule', players[playerNumber].deck, cardIndex, players[playerNumber].playedCards, Score, NewDeck, NewDeckPlayed))
            while q.nextSolution():
                players[playerNumber].score = Score.value
                players[playerNumber].deck = list(NewDeck.value)
                players[playerNumber].playedCards = list(NewDeckPlayed.value)
                print('Score:'+str(Score.value))
            q.closeQuery()
        


    
    
if __name__ == "__main__":
    initGame(3)
    playGame()