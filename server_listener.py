from google.cloud import pubsub_v1
import json
import glob
import sys
from os import path
from start_server import startup
import minecraft_status

def load_module( module ):
    module_path = module
    
    if module_path in sys.modules:
        return sys.modules[module_path]

    return __import__(module_path, fromlist=[module])

routes = []
dir_path = path.dirname(path.realpath(__file__))
route_modules = glob.glob( "/".join( [dir_path,"routes/*.py"] ) )
for rmf in route_modules:
    rmb,_ = path.splitext(rmf)
    _,rmm = path.split(rmb) 
    m = load_module( 'routes.' + rmm )
    if 'exec' in dir(m) :
        print( "Adding route: " + rmm )
        routes.append( (rmm, m.exec) )

routes = dict(routes)

def start( server_process ):
     project_id = "nodal-seer-702"
     subscription_name = "stop-minecraft-sub"

     subscriber = pubsub_v1.SubscriberClient()
     subscription_path = subscriber.subscription_path(
         project_id, subscription_name
     )

     def callback(message):
         result = None
         message.ack()
         try:
             payload = json.loads( message.data )
             if "command" in payload and payload['command'] in routes:
                 result = routes[payload['command']]( payload['args'] if 'args' in payload else None, server_process )
         except Exception as e:  # noqa
             print( e )
         if result == "exit":
             publisher = pubsub_v1.PublisherClient()
             topic_path = publisher.topic_path( project_id, "stop-instance-event" )
             data = u'{"zone":"us-west2-a","label":"name=minecraft-mv"}'
             data = data.encode("utf-8")
             publisher.publish(topic_path, data=data)
             minecraft_status.send("stop")

     streaming_pull_future = subscriber.subscribe(
         subscription_path, callback=callback
     )

     print("Listening for messages on {}..\n".format(subscription_path))

     # Wrap subscriber in a 'with' block to automatically call close() when done.
     with subscriber:
         try:
             # When `timeout` is not set, result() will block indefinitely,
             # unless an exception is encountered first.
             streaming_pull_future.result()
         except:  # noqa
             streaming_pull_future.cancel()
