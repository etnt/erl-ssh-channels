#!/usr/bin/env python3

import unittest
import subprocess
import xml.etree.ElementTree as ET
import os
import glob
import tempfile
import time

class TestNetconfServer(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        print(f"Temporary directory: {self.temp_dir}")

    def tearDown(self):
        for file in glob.glob(os.path.join(self.temp_dir, "*.log")):
            os.remove(file)
        os.rmdir(self.temp_dir)

    def test_hello_message_exchange(self):
        # Start the netconf_server.py as a subprocess
        process = subprocess.Popen(
            ['python3', 'netconf_server.py', '--log-dir', self.temp_dir],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True
        )

        try:
            # Read the server's hello message
            server_hello = ""
            while "]]>]]>" not in server_hello:
                chunk = process.stdout.read(1)
                if not chunk:
                    break
                server_hello += chunk

            # Verify the server's hello message
            self.assertIn("<hello xmlns=\"urn:ietf:params:xml:ns:netconf:base:1.0\">", server_hello)
            self.assertIn("<capability>urn:ietf:params:netconf:base:1.0</capability>", server_hello)

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
            print("Sent client hello message")

            time.sleep(1)
            

        finally:
            # Clean up
            process.terminate()
            process.wait(timeout=5)
            process.stdin.close()
            process.stdout.close()
            process.stderr.close()

        # Give some time for log file to be written
        time.sleep(1)

        # Check for log file
        log_files = glob.glob(os.path.join(self.temp_dir, "netconf_server_*.log"))
        self.assertTrue(log_files, "No log file found")
        
        # Get the most recent log file
        latest_log_file = max(log_files, key=os.path.getmtime)
        
        # Check log file contents
        with open(latest_log_file, 'r') as log_file:
            log_content = log_file.read()
            print(f"Log file contents:\n{log_content}")
            self.assertIn("Netconf server started", log_content)
            self.assertIn("Sent hello message", log_content)
            self.assertIn("Received valid hello message", log_content)
            self.assertIn("Hello message exchange completed", log_content)

if __name__ == '__main__':
    unittest.main()
