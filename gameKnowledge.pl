%To load a external file
%:- ensure_load(fileName).

color(red, X):-
	X is 6.
color(orange, X):-
        X is 5.
color(yellow, X):-
        X is 4.
color(green, X):-
        X is 3.
color(lBlue, X):-
        X is 2.
color(purple, X):-
        X is 1.
color(violet, X):-
        X is 0.

getColor(Card, Color):-
        Color is ceil(Card / 7).  

getCardNumber(Card, Number):- 
        Result is Card - (7 * floor(Card /  7)),
        (
        Result = 0 ->
        Number is 7
        ;
        Number is Result
        ).

%to make the deck we must create a vector and shuffle it and get the first 14 elements
createDeck(Deck).

%defining the rules

%number of pair cards rule
rule(pairRule, [], Score).

rule(pairRule, [Head|Tail], Score):- 
	isPair(Head, Result),
       	Sum is 1 - Result,
        Total  is Score + Sum,
        rule(pairRule, Tail, Total).	
        
isPair(Number, Result):- 
        Result is Number - (2 * floor(Number /  2)).

