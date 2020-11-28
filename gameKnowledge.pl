%prevent warning
:-discontiguous rule/3.
:- discontiguous rule/4.

color(red, X):-
	X is 7.
color(orange, X):-
        X is 6.
color(yellow, X):-
        X is 5.
color(green, X):-
        X is 4.
color(blue, X):-
        X is 3.
color(indigo, X):-
        X is 2.
color(violet, X):-
        X is 1.

colorRule(7, 'highestRule').
colorRule(6, 'sameNumberRule').
colorRule(5, 'sameColorRule').
colorRule(4, 'pairRule').
colorRule(3, 'diferentColor').
colorRule(2, 'run').
colorRule(1, 'below4Rule').

cardsToRules([], RulesList, RulesList).

cardsToRules([Head|Tail], AuxList, RulesList):-
        colorRule(Head, Rule),
        append(AuxList, [Rule], Result),
        cardsToRules(Tail, Result, RulesList).


mod(Number, Mod, Result):-
        Result is Number - (Mod * floor(Number / Mod)).   

getColor(Card, Color):-
        Color is ceil(Card / 7).  

getCardColorName(Card, ColorName):-
        getColor(Card, Color),
        color(ColorName, Color),
        !.

getCardNumber(Card, Number):- 
        mod(Card, 7, Result),
        (
        Result = 0 ->
        Number is 7
        ;
        Number is Result
        ).

%defining the rules

%rule to check if number is pair
isPair(Number, Result):- 
        mod(Number, 2, Result).

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

%red
rule(highestRule, List, Score):-
        maplist(getCardNumber, List, MappedList),
        max_list(MappedList, Score).

%Orange
rule(sameNumberRule, List, Score):-
        maplist(getCardNumber, List, MappedList),
        rule(sameNumberRule, MappedList, _, Score). 

rule(sameNumberRule, List, _, Score):-
        aggregate(max(Score1 ,Element1), ocurrence(List, Element1, Score1), max(Score,Element)).

%yellow
rule(sameColorRule, List, Score):-
        maplist(getColor, List, MappedList),
        rule(sameColorRule, MappedList, _, Score). 

rule(sameColorRule, List, _, Score):-
        aggregate(max(Score1 ,Element1), ocurrence(List, Element1, Score1), max(Score,Element)).

%green
rule(pairRule, List, Score):-
        maplist(getCardNumber, List, MappedList),
        countPairs(MappedList, 0, Score).

%Blue
rule(diferentColor, ColorList, Score):-
        getSingles(ColorList, [], Singles),
        length(Singles, Score).

%Indigo
rule(run, Cards, Score):-
        getSingles(Cards, [], Singles),
        sort(Singles, Sorted),
        maplist(getCardNumber, Sorted, MappedList),
        countTheRun(MappedList, 1, [], Score).

countTheRun([], _, ScoreList, Score):-
        max_list(ScoreList, Score).

countTheRun([Head|Tail], Counter, ScoreList, Score):-
        countRun(Tail, Head, Counter, TempScore),
        append(ScoreList, [TempScore], NewList),
        countTheRun(Tail, Counter, NewList, Score).

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

%Violet
rule(below4Rule, List, Score):-
        maplist(getCardNumber, List, MappedList),
        lowerThanFour(MappedList, 0, Score).