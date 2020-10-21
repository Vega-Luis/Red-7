# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 10:15:19 2020

@author: marcos
"""
from pyswip import Prolog

def prologQuery(path):
    prolog = Prolog()
    prolog.consult(path)
    for item in prolog.query('like_fried_chicken(X)'): print(item['X']) #check who LIKES friend chicken
    res = prolog.query('like_fried_chicken(basten)')
    if(bool(list(res))): 
        print('yes')
    else:
        print('no')
    
    
if __name__ == "__main__":
    prologQuery('testdb.pl')