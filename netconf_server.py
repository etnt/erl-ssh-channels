#!/usr/bin/env python3

import sys
import xml.etree.ElementTree as ET
import logging
import os
from datetime import datetime

# Set up logging
log_file = f"/tmp/netconf_server_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logging.basicConfig(filename=log_file, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def create_hello_message():
    hello = ET.Element("hello", xmlns="urn:ietf:params:xml:ns:netconf:base:1.0")
    capabilities = ET.SubElement(hello, "capabilities")
    ET.SubElement(capabilities, "capability").text = "urn:ietf:params:netconf:base:1.0"
    return ET.tostring(hello, encoding="unicode") + "]]>]]>"

def parse_hello_message(message):
    try:
        root = ET.fromstring(message)
        if root.tag.endswith("hello"):
            logging.info("Received valid hello message")
            logging.info(ET.tostring(root, encoding="unicode"))
            return True
    except ET.ParseError:
        logging.error("Failed to parse hello message")
    return False

def main():
    logging.info("Netconf server started")
    
    # Send hello message
    hello_message = create_hello_message()
    sys.stdout.write(hello_message)
    sys.stdout.flush()
    logging.info("Sent hello message")

    # Receive and parse client's hello message
    buffer = ""
    while True:
        chunk = sys.stdin.read(1)
        if not chunk:
            logging.error("Nothing to read")
            break
        buffer += chunk
        if "]]>]]>" in buffer:
            message, _, buffer = buffer.partition("]]>]]>")
            if parse_hello_message(message):
                logging.info("Hello message exchange completed")
                break

    # Continue processing other messages
    while True:
        chunk = sys.stdin.read(1)
        if not chunk:
            logging.info("No more msgs to read")
            break
        buffer += chunk
        if "]]>]]>" in buffer:
            message, _, buffer = buffer.partition("]]>]]>")
            logging.info(f"Received message: {message}")
            # Here you would typically process the message and send a response
            # For this example, we'll just echo the message back
            sys.stdout.write(f"Echoing received message: {message}]]>]]>")
            sys.stdout.flush()
            logging.info("Echoed message back to client")

    logging.info("Netconf server shutting down")

if __name__ == "__main__":
    main()
