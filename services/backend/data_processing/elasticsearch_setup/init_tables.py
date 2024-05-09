from elasticsearch import Elasticsearch

# Connect to Elasticsearch
es = Elasticsearch(['http://localhost:9200'])

# Mappings for 'show' index
show_mapping = {
    "mappings": {
        "properties": {
            "external_id": {"type": "keyword"},
            "title": {
                "type": "text",
                "fields": {
                    "suggest": {
                        "type": "completion",
                        "analyzer": "simple"
                    }
                }
            },
            "description": {"type": "keyword"},
            "image_url": {"type": "keyword"},
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
            "external_id": {"type": "keyword"},
            "name": {"type": "keyword"},
            "show_id": {"type": "keyword"},
            "season": {"type": "integer"},
            "number_in_season": {"type": "integer"},
            "number_in_show": {"type": "integer"},
            "is_last_of_the_season": {"type": "boolean"},
            "is_last_of_the_show": {"type": "boolean"},
            "description": {"type": "keyword"},
            "image_url": {"type": "keyword"},
            "air_date": {"type": "date"},
            "next_episode_air_date": {"type": "date", "null_value": None},
            "created_at": {"type": "date"},
            "updated_at": {"type": "date"},
        }
    }
}


# Create indices with mappings
es.indices.create(index="show", body=show_mapping)
es.indices.create(index="episode", body=episode_mapping)
