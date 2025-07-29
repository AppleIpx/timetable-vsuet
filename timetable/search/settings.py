COMMON_INDEX_SETTINGS = {
    "number_of_shards": 1,
    "number_of_replicas": 0,
    "analysis": {
        "filter": {
            "edge_ngram_filter": {
                "type": "edge_ngram",
                "min_gram": 2,
                "max_gram": 20,
            },
        },
        "analyzer": {
            "ngram_analyzer": {
                "type": "custom",
                "tokenizer": "standard",
                "filter": ["lowercase", "edge_ngram_filter"],
            },
            "ngram_search_analyzer": {
                "type": "custom",
                "tokenizer": "standard",
                "filter": ["lowercase"],
            },
        },
    },
}
