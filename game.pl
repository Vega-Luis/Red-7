:- ensure_loaded("gameKnowledge.pl").

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

%generate the deck for the game, there is a total of 49 cards
generateDeck(Deck):-
    numlist(1,49,List),
    random_permutation(List, Deck). %shuffle list

%generate the deck for the players, each deck size is of 7 cards
generateDeck(Player, IA):-
    generateDeck(Cards),
    reverse(Cards, ReversedCards),
    getSublist(Cards, Player),
    getSublist(ReversedCards, IA).

game(playerTurn):-
    writeln("player").

game(iaTurn):-
    writeln("ia").

game(begin):-
    generateDeck(Deck),
    generateDeck(Player, IA),
    getCard(Player, 0, 7, PlayerCard),
    getCard(IA, 0, 7, IACard),
    delete(Player, PlayerCard, PlayerDeck),
    delete(IA, IACard, IADeck),
    writeln(PlayerCard), writeln(IACard).

game(playing, Count):-
    Count \= 15,
    mod(Count, 2, X),
    (
    X = 0 ->
    game(playerTurn)
    ;
    game(iaTurn)    
    ),
    Count2 is Count + 1,
    game(playing, Count2).
    
    
    


