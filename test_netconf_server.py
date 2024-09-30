#!/usr/bin/env python3

import unittest
import subprocess
import xml.etree.ElementTree as ET

class TestNetconfServer(unittest.TestCase):
    def test_hello_message_exchange(self):
        # Start the netconf_server.py as a subprocess
        process = subprocess.Popen(
            ['python3', 'netconf_server.py'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Read the server's hello message
        server_hello = ""
        while "]]>]]>" not in server_hello:
            chunk = process.stdout.read(1)
            if not chunk:
                break
            server_hello += chunk

        # Verify the server's hello message
        self.assertIn('<hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">', server_hello)
        self.assertIn('<capability>urn:ietf:params:netconf:base:1.0</capability>', server_hello)

        # Send a client hello message
        client_hello = """
        <hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
            <capabilities>
                <capability>urn:ietf:params:netconf:base:1.0</capability>
            </capabilities>
        </hello>]]>]]>
        """
        process.stdin.write(client_hello)
        process.stdin.flush()

        # Read the server's response
        server_response = ""
        while "]]>]]>" not in server_response:
            chunk = process.stdout.read(1)
            if not chunk:
                break
            server_response += chunk

        # Verify the server's response
        self.assertIn("Echoing received message:", server_response)
        self.assertIn('<hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">', server_response)

        # Clean up
        process.terminate()
        process.wait()

if __name__ == '__main__':
    unittest.main()
