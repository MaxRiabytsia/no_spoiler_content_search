from elasticsearch import Elasticsearch, helpers

from models import ESBaseModel


url = "http://elasticsearch:9200"


class Database:
    def __init__(self):
        self._es = Elasticsearch([url])
        print(self._es.ping())

    def read(self, query: dict, index: str):
        return self._es.search(index=index, body=query)

    async def get_suggestions(self, query: str, index: str, field: str, number_of_suggestions: int = 5):
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
        print(response)
        suggestions = [
            option["text"] for option in response["suggest"]["suggestions"][0]["options"]
        ]
        print(suggestions)

        return suggestions

    def write(self, data: list[ESBaseModel]):
        def yeild_data():
            for item in data:
                yield item.to_es_loadable_object()

        helpers.bulk(self._es, yeild_data())


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
