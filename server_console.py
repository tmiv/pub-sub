from google.cloud import pubsub_v1
import json
import sys
from os import path
import re
import minecraft_status

def send_message( msg ):
     project_id = "nodal-seer-702"
     subscription_name = "stop-minecraft-sub"

     subscriber = pubsub_v1.SubscriberClient()
     subscription_path = subscriber.subscription_path(
         project_id, subscription_name
     )

connected_re = re.compile( "\[[0-9\:\- ]+INFO\] Player connected: (?P<name>[a-zA-Z0-9_\-]+)," )
disconnected_re = re.compile( "\[[0-9\:\- ]+INFO\] Player disconnected: (?P<name>[a-zA-Z0-9_\-]+)," )
auto_compact_re = re.compile( "\[[0-9\:\- ]+INFO\] Running AutoCompaction" )

def start( server_proc ):
    while True :
        line = server_proc.stdout.readline()
        if line == None :
            return
        line = line.decode()
        m = auto_compact_re.match(line)
        if not m:
            print( line.rstrip() )
        m = connected_re.match(line)
        if m:
            minecraft_status.send("login")
            print( "Connection " + m.group('name') )
            continue
        m = disconnected_re.match(line)
        if m:
            minecraft_status.send("logout")
            print( "Disconnection " + m.group('name') )
            continue

        



