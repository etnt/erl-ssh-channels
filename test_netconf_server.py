#!/usr/bin/env python3

import unittest
import subprocess
import xml.etree.ElementTree as ET
import time

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

        try:
            # Read the server's hello message with a timeout
            server_hello = self.read_with_timeout(process.stdout, "]]>]]>", 10)

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

            # Read the server's response with a timeout
            server_response = self.read_with_timeout(process.stdout, "]]>]]>", 10)

            # Verify the server's response
            self.assertIn("Echoing received message:", server_response)
            self.assertIn('<hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">', server_response)

        finally:
            # Clean up
            process.terminate()
            process.wait(timeout=5)

    def read_with_timeout(self, stream, delimiter, timeout):
        start_time = time.time()
        result = ""
        while True:
            if time.time() - start_time > timeout:
                raise TimeoutError("Timeout while reading from process")
            chunk = stream.read(1)
            if not chunk:
                break
            result += chunk
            if delimiter in result:
                break
        return result

if __name__ == '__main__':
    unittest.main()
