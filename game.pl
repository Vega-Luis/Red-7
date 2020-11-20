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

%start the game by generating the deck for the player and the IA and choosing their first card
game(begin, PlayerDeck, IADeck, PlayerCard, IACard):-
    generateDeck(Player, IA),
    getCard(Player, 0, 7, PlayerCard),
    getCard(IA, 0, 7, IACard),
    delete(Player, PlayerCard, PlayerDeck),
    delete(IA, IACard, IADeck).
/*
--Input
@Rule Current rule
@Deck Current player deck
@CardIndex Card choosed by the player
@DeckPlayed Current cards used by the player
--Output
@Score score after the move
@Status game status after the move *needs to be implemented
@NewDeck player deck after the move
*/
game(move, Rule, Deck, CardIndex, DeckPlayed, Score, Status, NewDeck):-
    getCard(Deck, 0, CardIndex, Card),
    delete(Deck, Card, NewDeck),
    append(DeckPlayed, [Card], NewDeckPlayed),
    %updateStatus(A,B,Status),
    rule(Rule, NewDeckPlayed, Score).
    

    
    
    


