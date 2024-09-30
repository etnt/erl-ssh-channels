all:
	erlc ssh_channel_test.erl

test:
	python3 -m unittest test_netconf_server.py



