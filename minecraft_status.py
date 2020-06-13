from google.cloud import pubsub_v1

def send( status ):
    project_id = "nodal-seer-702"
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path( project_id, "minecraft-status" )
    data = status
    data = data.encode("utf-8")
    publisher.publish(topic_path, data=data)
