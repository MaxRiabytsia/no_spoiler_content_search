from elasticsearch import Elasticsearch

# Connect to Elasticsearch
es = Elasticsearch(['http://localhost:9200'])  # Replace with your Elasticsearch host and port

# Mappings for 'show' index
show_mapping = {
    "mappings": {
        "properties": {
            "id": {"type": "keyword"},
            "internal_id": {"type": "keyword"},
            "title": {"type": "completion"},
            "description": {"type": "text", "index": False},  # Disable analysis for description field
            "rating": {"type": "integer"},
            "poster_url": {"type": "text", "index": False},  # Disable analysis for poster_url field
            "is_airing": {"type": "boolean"},
            "created_at": {"type": "date"},
            "updated_at": {"type": "date"}
        }
    }
}

# Mappings for 'episode' index
episode_mapping = {
    "mappings": {
        "properties": {
            "id": {"type": "keyword"},
            "internal_id": {"type": "keyword"},
            "name": {"type": "text", "index": False},  # Disable analysis for name field
            "show_id": {"type": "keyword"},
            "season": {"type": "integer"},
            "number": {"type": "integer"},
            "is_last_of_the_season": {"type": "boolean"},
            "is_last_of_the_show": {"type": "boolean"},
            "description": {"type": "text", "index": False},  # Disable analysis for description field
            "air_date": {"type": "date"},
            "next_episode_air_date": {"type": "date", "null_value": None},
            "created_at": {"type": "date", "index": False},  # Disable analysis for the field
            "updated_at": {"type": "date", "index": False},  # Disable analysis for the field
        }
    }
}

# Mappings for 'content' index
content_mapping = {
    "mappings": {
        "properties": {
            "id": {"type": "keyword"},
            "internal_id": {"type": "keyword"},
            "episode_id": {"type": "keyword"},
            "title": {"type": "text"},
            "url": {"type": "text", "index": False},  # Disable analysis for url field
            "content_type": {"type": "keyword"},
            "view_count": {"type": "integer"},
            "like_count": {"type": "integer"},
            "published_date": {"type": "date"},
            "created_at": {"type": "date", "index": False},  # Disable analysis for the field
            "updated_at": {"type": "date", "index": False},  # Disable analysis for the field
        }
    }
}

pipeline_mapping = {
    "mappings": {
        "properties": {
            "id": {"type": "keyword"},
            "name": {"type": "keyword"},
            "last_run_timestamp": {"type": "date", "index": False},  # Disable analysis for the field
        }
    }
}

# Create indices with mappings
es.indices.create(index="show", body=show_mapping)
es.indices.create(index="episode", body=episode_mapping)
es.indices.create(index="content", body=content_mapping)
es.indices.create(index="pipeline", body=pipeline_mapping)
