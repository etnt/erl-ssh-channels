# Test the behaviour of the Erlang SSH app with the Netconf subsystem

## Setup

1. Compile the Erlang client: `make`
2. Copy the `netconf_server.py` script to (e.g) `/usr/local/bin`
3. Add the following lines to `/etc/ssh/sshd_config`:
```
Subsystem	netconf	/usr/local/bin/netconf_server.py
```
4. Restart the SSH server: `sudo systemctl restart sshd` or `sudo service sshd restart`

## Usage

Run the Erlang client: `make run`

The client will connect to the SSH server and create two SSH channels. The first channel will send and
receive a Netconf Hello message and then close the channel.  The second channel will also send and
receive a Netconf Hello message and then close the channel.

This will verify that the Channels can be closed independently without affecting the other channel.
