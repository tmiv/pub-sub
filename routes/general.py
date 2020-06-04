import os

def exec( args, server_proc ):
    if 'execute' in args:
        print( "executing: " + args['execute'] )
        server_proc.stdin.write( (args['execute'] + "\n").encode() )
        server_proc.stdin.flush()
