#!/usr/bin/env python3

import sys
import xml.etree.ElementTree as ET
import select

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
    timeout = 5  # 5 seconds timeout
    while True:
        ready, _, _ = select.select([sys.stdin], [], [], timeout)
        if not ready:
            sys.stderr.write("Timeout waiting for client hello\n")
            return
        chunk = sys.stdin.read(1)
        if not chunk:
            break
        buffer += chunk
        if "]]>]]>" in buffer:
            message, _, buffer = buffer.partition("]]>]]>")
            if parse_hello_message(message):
                sys.stderr.write("Hello message exchange completed\n")
                break


if __name__ == "__main__":
    main()
