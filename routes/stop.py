import os

def exec( args, server_proc ):
    print( "Stopping Server" )
    time = 30
    try: 
       if 'time' in args:
           time = int(args['time'])
    except:
        pass
    os.system( '/home/tmiv74/minecraftbe/mv-minecraft/stop.sh ' + time );
    print( "Server Stopped" )
