#!/usr/bin/python3
# Import utility to ping
from pythonping import ping        
# pexepct for interaction                                               
import pexpect
# Import the config parser
import configparser
# Time
import time

# Get the config
config = configparser.ConfigParser()
config.read('config.ini')

def pingtest():
    # Get variables from config
    pingtestip = config.get('config', 'pingtestip')
    shutdowntime = config.get('config', 'shutdowntime')
    print(f'[*] Pinging {pingtestip}')
    # Start the ping
    p = ping(pingtestip, count=10)
    # If the ping is all good we notify the console and start again.
    if p.success():
        print(f'[*] No issue with {pingtestip} Online')
        pingtest()
    else:
        print(f'[!] {pingtestip} has gone offline shuttding down the firewalls in {shutdowntime}')
        time.sleep(shutdowntime)
        # Failsafe just incase it's come online again
        # The pinging should be put in a funciton so we're not repeating the code here but it works.
        print(f'[*] Doing final test for {pingtestip} to be back online')
        p = ping(pingtestip, count=10)
        if p.success():
            print(f'[*] {pingtestip} Back online')
            # Restart the function from the start
            pingtest()
        else:
            # Final test fails we test again
            print(f'[!] {pingtestip} is still down, shutting down the firewall')
            shutdown()


def shutdown():
    # Create variables out of the config file
    firewalluser = config.get('config', 'firewalluser')
    firewallpass = config.get('config', 'firewallpass')
    print('[!] Starting shutdown of firewall')
    # Create SSH connection
    child = pexpect.spawnu(f'/usr/bin/ssh -q -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no\
                            -o PubkeyAuthentication=no {firewalluser}@172.16.16.16', encoding='utf-8')

    child.delaybeforesend = 1
    # Enter Password to auth
    child.expect('password:', timeout=10)
    child.sendline(f'{firewallpass}')
    # Select Shutdown/Reboot Option
    child.expect('Select Menu Number', timeout=10)
    child.sendline('7')
    # Proper dirty error handling
    try:
        # Send S to shutdown the device
        child.expect('Shutdown(S/s)', timeout=10)
        child.sendline('S')
        print(f'[*] Appliance is shutdown')
    except:
        print(f'[!] Error shutting down appliance')
    # Close the connection
    child.close()

if __name__ == "__main__":
    # Start with a ping test
    pingtest()