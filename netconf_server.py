#!/usr/bin/env python3

import sys
import xml.etree.ElementTree as ET

def create_hello_message():
    hello = ET.Element("hello", xmlns="urn:ietf:params:xml:ns:netconf:base:1.0")
    capabilities = ET.SubElement(hello, "capabilities")
    ET.SubElement(capabilities, "capability").text = "urn:ietf:params:netconf:base:1.0"
    return ET.tostring(hello, encoding="unicode") + "]]>]]>"

def parse_hello_message(message):
    try:
        root = ET.fromstring(message)
        if root.tag.endswith("hello"):
            sys.stderr.write("Received valid hello message:\n")
            sys.stderr.write(ET.tostring(root, encoding="unicode") + "\n")
            return True
    except ET.ParseError:
        pass
    return False

def main():
    # Send hello message
    hello_message = create_hello_message()
    sys.stdout.write(hello_message)
    sys.stdout.flush()

    # Receive and parse client's hello message
    buffer = ""
    while True:
        chunk = sys.stdin.read(1)
        if not chunk:
            break
        buffer += chunk
        if "]]>]]>" in buffer:
            message, _, buffer = buffer.partition("]]>]]>")
            if parse_hello_message(message):
                sys.stderr.write("Hello message exchange completed\n")
                break

    # Continue processing other messages
    while True:
        chunk = sys.stdin.read(1)
        if not chunk:
            break
        buffer += chunk
        if "]]>]]>" in buffer:
            message, _, buffer = buffer.partition("]]>]]>")
            sys.stderr.write(f"Received message: {message}\n")
            # Here you would typically process the message and send a response
            # For this example, we'll just echo the message back
            sys.stdout.write(f"Echoing received message: {message}]]>]]>")
            sys.stdout.flush()

if __name__ == "__main__":
    main()