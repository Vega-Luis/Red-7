# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 10:15:19 2020

@author: marcos
"""
from pyswip import Prolog

#Game constants
PATH = 'game.pl'
RULES = ['below4Rule','run','diferentColor','pairRule','yellow','sameNumberRule','highestRule']

#Variables
prolog = Prolog()
prolog.consult(PATH)
playerDeck = []
IADeck = []
playerPlayedCards = []
IAPlayedCards = []
playerScore = 0
IAScore = 0

def prologQuery():
    res = prolog.query('like_fried_chicken(basten)')
    if(bool(list(res))): 
        print('yes')
    else:
        print('no')

def initGame():
    for item in prolog.query('game(begin, PlayerDeck, IADeck, PlayerCard, IACard)'): 
        playerDeck = list((item['PlayerDeck']))
        IADeck = list((item['IADeck']))

def playGame():
    gameStatus = 'playing'
    currentRule = RULES[0]
    for item in prolog.query('rule(Rule, NewDeckPlayed, Score)'):

    for item in prolog.query('game(playing, 0, Status)'): 
        if((item['Status']) == 'player'):
            print('yes')
        else:
            print('no')

    
    
if __name__ == "__main__":
    initGame()
    playGame()