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

    print(f'[!] Pinging {pingtestip}')

    p = ping(pingtestip, count=10)
    
    if p.success():
        print(f'[*] No issue with {pingtestip} Online')
        pingtest()
    else:
        print(f'[!] {pingtestip} has gone offline shuttding down the firewalls in {shutdowntime}')
        time.sleep(shutdowntime)
        # Failsafe just incase it's come online again
        print(f'[*] Doing final test for {pingtestip} to be back online')
        p = ping(pingtestip, count=10)
        if p.success():
            print(f'[*] {pingtestip} Back online')
            # Restart the ping test
            pingtest()
        else:
            print(f'[!] {pingtestip} is still down, shutting down the firewall')
            shutdown()


def shutdown():
    firewalluser = config.get('config', 'firewalluser')
    firewallpass = config.get('config', 'firewallpass')
    print('[!] Starting shutdown of firewall')
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