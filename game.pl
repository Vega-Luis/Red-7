:- ensure_loaded("gameKnowledge.pl").

%generate the deck for the game, there is a total of 49 cards
generateDeck(Deck):-
    numlist(1,49,List),
    random_permutation(List, Deck). %shuffle list

getSublist([Head|Tail], Result):-
    length(Tail, X),
    (
        X = 7 ->
        append(Tail,[], Result)
        ;
        getSublist(Tail, Result)
    ).

%generate the deck for the players, each deck size is of 7 cards
generateDeck(Player, IA):-
    generateDeck(Cards),
    reverse(Cards, ReversedCards),
    writeln(Cards),writeln(ReversedCards),
    getSublist(Cards, Player),
    getSublist(ReversedCards, IA).
    
    


