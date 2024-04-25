from elasticsearch import Elasticsearch

# Connect to Elasticsearch
es = Elasticsearch(['http://localhost:9200'])  # Replace with your Elasticsearch host and port

# Define the names of the indexes you want to delete
indexes_to_delete = ["show", "episode", "content"]  # Add more index names as needed

# Iterate over the index names and delete each index
for index_name in indexes_to_delete:
    if es.indices.exists(index=index_name):
        es.indices.delete(index=index_name)
        print(f"Index '{index_name}' deleted successfully.")
    else:
        print(f"Index '{index_name}' does not exist.")
