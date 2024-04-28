from elasticsearch import Elasticsearch, helpers

from models import ESBaseModel


class Database:
    def __init__(self):
        self._es = Elasticsearch()

    def read(self, query: dict, index: str):
        return self._es.search(index=index, body=query)

    async def get_suggestions(self, query: str, index: str, field: str, number_of_suggestions: int = 5):
        response = self._es.search(
            index=index,
            body={
                "suggest": {
                    "suggestions": {
                        "text": query,
                        "completion": {
                            "field": field,
                            "size": number_of_suggestions
                        }
                    }
                }
            }
        )

        suggestions = [
            option["text"] for option in response["suggest"]["suggestions"][0]["options"]
        ]

        return suggestions

    def write(self, data: list[ESBaseModel]):
        def yeild_data():
            for item in data:
                yield item.to_es_loadable_object()

        helpers.bulk(self._es, yeild_data())
