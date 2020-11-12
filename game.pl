:- ensure_loaded("gameKnowledge.pl").

generateDeck(Deck):-
    numlist(1,49,List),
    random_permutation(List, Deck).

