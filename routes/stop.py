import os
import time

def send( message, server_proc ):
    print( message )
    server_proc.stdin.write( message.encode() )
    server_proc.stdin.flush()

def exec( args, server_proc ):
    print( "Stopping Server" )
    remainder = 30
    try: 
       if 'time' in args:
           remainder = int(args['time'])
    except:
        pass
    while remainder >= 60:
        send( "say Shutdown in %d minutes\n" % (remainder//60), server_proc )
        if remainder - 60 > 60:
            remainder = remainder - 60
            time.sleep(60)
        else:
            remainder = 59

    if remainder >= 30:
        time.sleep( remainder-30 )
        remainder = 30
        send( "say Shutdown in 30 seconds\n", server_proc )
    if remainder >= 20:
        time.sleep( remainder-20 )
        remainder = 20
        send( "say Shutdown in 20 seconds\n", server_proc )
    if remainder >= 10:
        time.sleep( remainder-10 )
        remainder = 10
        send( "say Shutdown in 10 seconds\n", server_proc )
    if remainder >= 5:
        time.sleep( remainder-5 )
        remainder = 5
        send( "say Shutdown in 5 seconds\n", server_proc )
    if remainder >= 2:
        time.sleep( remainder-2 )
        remainder =2 
        send( "say Shutdown in 2 seconds\n", server_proc )

    send( "stop\n", server_proc )

    server_proc.wait()

    print( "Server Stopped" )
    exit()
