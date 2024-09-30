all:
	erlc ssh_channel_test.erl

run:
	erl -noshell -s ssh_channel_test test -s init stop

test:
	python3 -m unittest test_netconf_server.py



