import os
import subprocess
from datetime import datetime
from datetime import timedelta

MinecraftBase = os.getenv('MINECRAFT_BASE')

def exec( args, server_proc ):
    print( "Backing Up" )
    stamp = (datetime.now() - timedelta(hours=7)).strftime( "%Y.%m.%d.%H.%M.%S" )
    proc = subprocess.Popen( ['tar', '--directory=' + MinecraftBase,
            '-pczf', MinecraftBase + '/backups/' + stamp + '.tar.gz', 
            'worlds'] )
    proc.wait()

if __name__ == '__main__':
    exec( None, None )


