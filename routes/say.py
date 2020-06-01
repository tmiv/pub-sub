import os

def exec( args, server_proc ):
    if 'message' in args:
        print( "saying: " + args['message'] )
        server_proc.stdin.write( ("say " + args['message'] + "\n").encode() )
        server_proc.stdin.flush()
