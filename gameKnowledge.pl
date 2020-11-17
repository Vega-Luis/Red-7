%prevent warning
:-discontiguous rule/3.

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
createDeck(_).

%defining the rules

%rule to check if number is pair
isPair(Number, Result):- 
        Result is Number - (2 * floor(Number /  2)).

countPairs([], Total, Total).

countPairs([Head|Tail], Total, Score):-
        isPair(Head, Result),
        Total2 is Total + (1 - Result),
        countPairs(Tail, Total2, Score).

%rules to check the number of times that a element appears in a list
ocurrence(List, Element, Count) :-
        aggregate(count, member(Element,List), Count).

lowerThanFour([], Total, Total).

lowerThanFour([Head|Tail], Total, Score):-
        ( 
        Head < 4 ->
        Total2 is Total + 1,
        lowerThanFour(Tail, Total2, Score)
        ;
        lowerThanFour(Tail, Total, Score)
        ).

%number of pair cards rule
rule(pairRule, List, Score):-
        countPairs(List, 0, Score).

rule(highestRule, List, Score):-
        max_list(List, Score).

rule(sameNumberRule, List, Element, Score):-
        aggregate(max(Score1 ,Element1), ocurrence(List, Element1, Score1), max(Score,Element)).

%Cards lower than 4 rule
rule(below4Rule, List, Score):-
        lowerThanFour(List, 0, Score).


%transform a list of cards to a color list cards
cardsToColors([], ColorList, ColorList).

cardsToColors([Head|Tail], AuxList, ColorList):- 
        getColor(Head,Color),
        append(AuxList, [Color], Result),
        cardsToColors(Tail, Result, ColorList).

%Cards of the same color
%Once the we have the card color numbers, we can reuse the sameNumberRule :D 

%get the non repeated numbers in the list, 
getSingles([], Result, Result).

getSingles([Head|Tail], Aux, Result):- 
        (
        member(Head, Aux) ->
        getSingles(Tail, Aux, Result)
        ;
        append(Aux, [Head], NewList),
        getSingles(Tail, NewList, Result)
        ).

%Cards of diferent color
rule(diferentColor, ColorList, Score):-
        getSingles(ColorList, [], Singles),
        length(Singles, Score).

%cards that form a RUN(4 5 6 ... 12 3)
%el numero de la carta, no la carta

rule(run, Cards, Score):-
        getSingles(Cards, [], Singles),
        sort(Singles, Sorted),
        countTheRun(Sorted, 1, [], Score).

countTheRun([], Counter, ScoreList, Score):-
        max_list(ScoreList, Score).

countTheRun([Head|Tail], Counter, ScoreList, Score):-
        countRun(Tail, Head, Counter, TempScore),
        append(ScoreList, [TempScore], NewList),
        countTheRun(Tail, Counter, NewList, Score).

%    this works    
countRun([], _Temp, Counter, Counter).

countRun([Head|Tail], Temp, Counter, Output):-
       N is Head-Temp,
       (
               N = 1 ->
               Counter2 is Counter + 1,
               countRun(Tail, Head, Counter2, Output)
        ;
               countRun(Tail, Temp, Counter, Output)
       ).