import subprocess
import os
import threading
from routes.backup import exec as backup
import server_listener as listener
import server_console as console
import re
import minecraft_status

MINECRAFT_BASE = os.getenv('MINECRAFT_BASE')

def check_version():
    # Retrieve latest version of Minecraft Bedrock dedicated server
    print( "Checking for the latest version of Minecraft Bedrock server ..." )

    # Test internet connectivity first
    proc = subprocess.Popen( ['wget', '--spider', '--quiet', 
        'https://minecraft.net/en-us/download/server/bedrock/'] )
    proc.wait()
    if proc.returncode != 0:
       print( "Unable to connect to update website (internet connection may be down).  Skipping update ..." )
    else:
        # Download server index.html to check latest version
        proc = subprocess.Popen( ['wget', '-O', 
                    MINECRAFT_BASE + '/downloads/version.html',
                    'https://minecraft.net/en-us/download/server/bedrock/'] )
        proc.wait()
        with open( MINECRAFT_BASE + '/downloads/version.html', 'r' ) as version_file:
             res = re.finditer( 'https://minecraft.azureedge.net/bin-linux/(?P<version>[^\"]*)', version_file.read(),
                     re.MULTILINE)
             for r in res:
                 print( r[0], r.group('version') )
                 if os.path.exists( MINECRAFT_BASE + "/downloads/" + r.group('version') ):
                    print( "Minecraft Bedrock server is up to date..." )
                 else:
                    print( "New version $DownloadFile is available.  Updating Minecraft Bedrock server ..." )
                    proc = subprocess.Popen( ['wget', "-O",
                                               MINECRAFT_BASE + "/downloads/" + r.group('version'),
                                               r[0]] )
                    proc.wait()
                    proc = subprocess.Popen( ['unzip', '-o', 
                                             MINECRAFT_BASE + "/downloads/" + r.group('version'),
                                             "-d", MINECRAFT_BASE,
                                             "-x",  '*server.properties*', 
                                             "*permissions.json*", "*whitelist.json*"] )
                    proc.wait()

def launch():
    minecraft_status.send("start")
    proc = subprocess.Popen( [ MINECRAFT_BASE + "/bedrock_server" ], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                               cwd = MINECRAFT_BASE )
    return proc

def startup():
    backup(None, None)
    check_version()
    return launch()

if __name__ == "__main__":
    process = startup()
    listen_thread = threading.Thread(target=listener.start, args=(process,))
    listen_thread.daemon = True
    listen_thread.start()
    console_thread = threading.Thread(target=console.start, args=(process,))
    console_thread.daemon = True
    console_thread.start()
    listen_thread.join()
