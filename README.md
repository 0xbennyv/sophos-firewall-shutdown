This script is designed to run on an intermediary device, not the sophos firewall. This script continually tests for an ip address being online, on failure will initialize a shutdown of the sophos firewall via ssh. 

This is provided as a proof of concept and should be thoroughly tested prior to running in production.

### Usage:
- python3 -m venv venv
- pip install -r requirements.txt
- python shutdown.py

Any issues that need attention please create an issue.