from elasticsearch import Elasticsearch, helpers

from models import ESBaseModel

url = "http://elasticsearch:9200"


class Database:
    def __init__(self):
        self._es = Elasticsearch([url])
        print(self._es.ping())

    def read(self, query: dict, index: str):
        return self._es.search(index=index, body=query)

    async def get_suggestions(self, query: str, index: str, field: str, number_of_suggestions: int = 50):
        response = self._es.search(
            index=index,
            body={
                "suggest": {
                    "suggestions": {
                        "prefix": query,
                        "completion": {
                            "field": f"{field}.suggest",
                            "size": number_of_suggestions
                        }
                    }
                }
            }
        )

        suggestions = response["suggest"]["suggestions"][0]["options"]
        return suggestions

    def write(self, data: list[ESBaseModel]):
        def yeild_data(data1):
            for item in data1:
                yield item.to_es_loadable_object()

        print("Writing data to ES")
        helpers.bulk(self._es, yeild_data(data))

    def delete(self, show_title: str):
        # delete by perfect match (not fuzzy)
        self._es.delete_by_query(index="show", body={"query": {"match_phrase": {"title": show_title}}})

    def _save_all_db_data_to_file(self):
        import json
        from datetime import datetime
        from pathlib import Path

        data = self.read({"query": {"match_all": {}}, "size": 1000}, "show")
        data = data["hits"]["hits"]
        data = [item["_source"] for item in data]
        data = json.dumps(data, indent=4)
        file_path = Path(f"db_data_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json")
        with open(file_path, "w") as file:
            file.write(data)
        print(f"Data saved to {file_path}")


if __name__ == "__main__":
    url = "http://localhost:9200"
    db = Database()
    query = {
        "query": {
            "match_all": {}
        },
        "size": 100,
        "_source": ["external_id", "name"]
    }
    response = db.read(query, "episode")
    print(response)
