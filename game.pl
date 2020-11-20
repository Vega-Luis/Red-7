:- ensure_loaded("gameKnowledge.pl").

getSublist([_|Tail], NewLength, NewList):-
    length(Tail, X),
    (
        X = NewLength ->
        append(Tail,[], NewList)
        ;
        getSublist(Tail, NewLength, NewList)
    ).

getCard([Head|Tail], Current, Index, Result):-
    (
    Current = Index ->
    Result is Head
    ;
    Current2 is Current + 1,
    getCard(Tail, Current2, Index, Result)    
    ).

generateDeck(done, TempDeck, TempDeck).

generateDeck([Head|Tail], Count, TempDeck, Deck):-
    (
    Count > 0 ->
    append([Head], TempDeck, NewDeck),
    Count2 is Count - 1,
    generateDeck(Tail, Count2, NewDeck, Deck)
    ;
    generateDeck(done, TempDeck, Deck)
    ).

%generate the deck for the game, there is a total of 49 cards
generateDeck(Deck):-
    numlist(1,49,List),
    random_permutation(List, Deck). %shuffle list

%generate the deck for a player, each deck size is of 7 cards
generateDeck(Player, NewDeck):-
    generateDeck(Cards),
    generateDeck(Cards, 7, [], Player),
    length(Cards, X),
    NewLength is X - 7,
    getSublist(Cards, NewLength, NewDeck).

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
    

    
    
    


