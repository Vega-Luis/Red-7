:- ensure_loaded("gameKnowledge.pl").

%generate the deck for the game, there is a total of 49 cards
generateDeck(Deck):-
    numlist(1,49,List),
    random_permutation(List, Deck). %shuffle list

getSublist([_|Tail], Result):-
    length(Tail, X),
    (
        X = 8 ->
        append(Tail,[], Result)
        ;
        getSublist(Tail, Result)
    ).

getCard([Head|Tail], Current, Index, Result):-
    (
    Current = Index ->
    Result is Head
    ;
    Current2 is Current + 1,
    getCard(Tail, Current2, Index, Result)    
    ).

%generate the deck for the players, each deck size is of 7 cards
generateDeck(Player, IA):-
    generateDeck(Cards),
    reverse(Cards, ReversedCards),
    writeln(Cards),writeln(ReversedCards),
    getSublist(Cards, Player),
    getSublist(ReversedCards, IA).

game(playerTurn):-
    writeln("player").

game(iaTurn):-
    writeln("ia").

game():-
    generateDeck(Deck),
    generateDeck(Player, IA).

    
    


