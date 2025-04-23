import os

import weaviate
import weaviate.classes as wvc

# Connect to Weaviate Cloud
client = weaviate.connect_to_local()

# Check connection
print(client.is_ready())

client.close()
