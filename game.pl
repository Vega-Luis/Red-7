:- ensure_loaded("gameKnowledge.pl").
:- ensure_loaded("iaBehavior.pl").

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

%generate the deck for the game, there is a total of 49 cards
generateDeck(Deck):-
    numlist(1,49,List),
    random_permutation(List, Deck). %shuffle list

generateDeck(done, TempDeck, TempDeck).

%generate 1 deck
generateDeck(single, [Head|Tail], Count, TempDeck, Deck):-
    (
    Count > 0 ->
    append([Head], TempDeck, NewDeck),
    Count2 is Count - 1,
    generateDeck(single, Tail, Count2, NewDeck, Deck)
    ;
    generateDeck(done, TempDeck, Deck)
    ).

%generate the deck for all players, each deck size is of 7 cards, but 1 more is added to be used as first card
generateDeck(multiple, GameDeck, PlayerQuantity, TempDecks, Decks):-
    (
        PlayerQuantity > 0 ->
        generateDeck(single, GameDeck, 8, [], NewDeck),
        append(TempDecks, [NewDeck], TotalDecks),
        length(GameDeck, X),
        NewLength is X - 8,
        getSublist(GameDeck, NewLength, NewGameDeck),
        PlayerQuantity2 is PlayerQuantity - 1,
        generateDeck(multiple, NewGameDeck, PlayerQuantity2, TotalDecks, Decks)
        ;
        generateDeck(done, TempDecks, Decks)
    ).

generateDeck(PlayerQuantity, Decks):-
    generateDeck(GameDeck),
    generateDeck(multiple, GameDeck, PlayerQuantity, [], Decks).

/*
--Input
@Rule Current rule
@Deck Current player deck
@CardIndex Card choosed by the player
@DeckPlayed Current cards used by the player
--Output
@Score score after the move
@NewDeck player deck after the move
@NewDeckPlayed player playedDeck after the move
*/
game(Rule, Deck, CardIndex, DeckPlayed, Score, NewDeck, NewDeckPlayed):-
    getCard(Deck, 0, CardIndex, Card),
    delete(Deck, Card, NewDeck),
    append(DeckPlayed, [Card], NewDeckPlayed),
    rule(Rule, NewDeckPlayed, Score).
    

    
    
    


