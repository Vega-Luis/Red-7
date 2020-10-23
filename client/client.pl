:- use_module(library(socket)).
client(IpAddr) :-
	setup_call_cleanup(tcp_socket(S),  % no leaks on connect failure
			   (   true; fail),
			   Connected == true -> true; tcp_close_socket(S)),

	tcp_connect(S, IpAddr),
	tcp_open_socket(S, In, Out),

	Connected = true, !,

	call_cleanup((true; fail),  % no matter what happens, socket gets released
		     (writeln('closing...'),
		      close(In),
		      close(Out))),

	forall(between(1,20, N),
	       (   format(Out, 'eating chicken: ~p', [N]),
		   flush_output(Out),
		   \+at_end_of_stream(In),
		   read_pending_input(In, Codes, []),
		   format('chicken  received: ~s~n', [Codes]))
	      ), !.
