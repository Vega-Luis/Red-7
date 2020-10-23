:- use_module(library(socket)).
server(PortNumber) :-
	setup_call_cleanup(tcp_socket(S),  % no leaks, please
			   (true; fail),
			   tcp_close_socket(S)),

	tcp_bind(S, PortNumber),
	tcp_listen(S, 5),
	server_loop(S).

server_loop(S) :-
	tcp_accept(S, S1, From),
	format('receiving fried chicken from: ~q~n', [From]),
	setup_call_cleanup(tcp_open_socket(S1, In, Out),
			   server_operation(In, Out),
			   (  writeln('fnished meal :D'),
			      close(In),
			      close(Out))), !,
	server_loop(S).

server_operation(In, Out) :-
	\+at_end_of_stream(In),
	read_pending_input(In, Codes, []),   % loopback for testing.
	format(Out, '~s', [Codes]),
	flush_output(Out),
	server_operation(In, Out).

server_operation(_In, _Out).
