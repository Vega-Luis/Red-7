:- ensure_loaded("gameKnowledge.pl").
%se incluye en game.pl
%necesito saber la regla actual
%ver si hay un movimiento que sea mayor al score maximo
%Necesito retornarle un indice
%sucks
nextMove(ActualRule, _, PlayerCards, GameCards, MaxScore, CardIndex, NewRule):-
    cardsToColors(PlayerCards, [], ColorsList),
    maplist(getCardNumber, PlayerCards, MappedList),
    cardsToRules(ColorsList, [], RulesList),
    getScores(ActualRule, PlayerCards, GameCards, [], ScoreList),
    max_list(ScoreList, NewMax),
    getRuleScores(RulesList, GameCards, [], RuleScoreList),
    max_list(RuleScoreList, MaxRuleScore),
    (
        (NewMax >= MaxRuleScore, NewMax >= MaxScore) ->
        nth0(CardIndex, ScoreList, NewMax),
        NewRule = ActualRule
    ; 
        (
        MaxRuleScore > MaxScore ->
        nth0(CardIndex, RuleScoreList, MaxRuleScore),
        nth0(MaxRuleScore, RuleScoreList, NewRuleIndex), 
        nth0(NewRuleIndex, RulesList, NewRule)
        ;
        CardIndex is -1,
        NewRule = ActualRule
        )
    ).
    

getRuleScores([], _GameCards, RuleScoreList, RuleScoreList).

getRuleScores([Head|Tail], GameCards, AuxList, RuleScoreList):-
    getMoveScore(Head, GameCards, Score),
    append(AuxList, [Score], NewList),
    getRuleScores(Tail, GameCards, NewList, RuleScoreList).

getScores(_ActualRule, [], _Move, ScoreList, ScoreList).

getScores(ActualRule, [PHead|PTail], Move, AuxScoreList, ScoreList):-
    append([PHead], Move, NewMove),
    getMoveScore(ActualRule, NewMove, Score),
    append(AuxScoreList, [Score], NewScoreList),
    getScores(ActualRule, PTail, Move, NewScoreList, ScoreList).

%Obtains the movement score
getMoveScore(ActualRule, Move, Score):-
    rule(ActualRule, Move, Score).

