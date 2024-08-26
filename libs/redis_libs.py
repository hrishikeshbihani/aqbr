import redis
import os
from redis.commands.search.field import TagField, VectorField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import Query
from constants import Constants
import numpy as np

r = redis.Redis.from_url(url=os.getenv("REDIS_URL"))


def set_value(key, value, ttl=None):
    r.set(key, value, ex=ttl)


def get_value(key):
    return r.get(key)


def delete_value(key):
    return r.delete(key) == 1


def add_message(user_id, message):
    r.rpush(user_id, message)


def get_messages(user_id):
    return r.lrange(user_id, 0, -1)


def get_value_from_hash(key, field_to_retrieve):
    if r.hget(key, field_to_retrieve) is not None:
        return r.hget(key, field_to_retrieve)
    else:
        return b""


def set_value_from_hash(key, field_to_set, value):
    if r.exists(key):
        value += "," + Constants.DEFAULT_TAG if value else Constants.DEFAULT_TAG
        r.hset(key, field_to_set, value)
        return True
    else:
        return False


def check_if_index_exists(index_name):
    """
    Checks if index exists in redis


    Args:
        index_name (String): Name of Index
    Returns:
        boolean: True if index exists
    """
    try:
        r.ft(index_name).info()
        return True
    except:
        return False


def create_redis_index(index_name, doc_prefix):
    try:
        schema = (
            TagField("tag"),
            VectorField(
                "vector",
                "FLAT",
                {
                    "TYPE": "FLOAT32",
                    "DIM": 1536,  # Number of Vector Dimensions for OPENAI Embeddings taken from their documentation
                    "DISTANCE_METRIC": "COSINE",
                },
            ),
        )
        definition = IndexDefinition(prefix=[doc_prefix], index_type=IndexType.HASH)
        r.ft(index_name).create_index(fields=schema, definition=definition)
        return True
    except Exception as err:
        raise Exception(
            "Error while creating Search Index on Redis: {err}".format(err=str(err))
        )


def add_vector_to_redis(vector, key, params, tag_csv):
    try:
        tag_csv = (tag_csv + "," if tag_csv else "") + Constants.DEFAULT_TAG
        tag_csv = tag_csv.replace("-", "_")
        pipe = r.pipeline()
        mapping_object = {
            "tag": tag_csv,
            "vector": np.array(vector).astype(np.float32).tobytes(),
        }
        mapping_object.update(params)
        doc_prefix = os.getenv("SEMANTIC_SEARCH_INDEX_PREFIX")
        if key.startswith(doc_prefix):
            pipe.hset(key, mapping=mapping_object)
        else:
            pipe.hset(f"{doc_prefix}:{key}", mapping=mapping_object)
        pipe.execute()
        return True
    except Exception as e:
        print("Error adding vector to redis")
        print(e)
    return False


def delete_vector_from_redis(key):
    doc_prefix = os.getenv("SEMANTIC_SEARCH_INDEX_PREFIX")
    key_with_prefix = (
        key
        if key.startswith(doc_prefix)
        else "{doc_prefix}:{key}".format(doc_prefix=doc_prefix, key=key)
    )
    return delete_value(key_with_prefix)


def _query_builder(tags):
    if tags:
        tags = tags.replace("-", "_")
        individual_tags = tags.split(",")
        query_tags = [f"(@tag:{{{tag_name}}})" for tag_name in individual_tags]
        query_string = " | ".join(query_tags)
    else:
        query_string = f"(@tag:{{{Constants.DEFAULT_TAG}}})"

    query = (
        Query(f"({query_string})=>[KNN 5 @vector $vec as score]")
        .sort_by("score")
        .return_fields("id", "tag", "score", "dashboard_name", "product", "bundles_product_mappings")
        .paging(0, 10)
        .dialect(2)
    )
    response = {"query": query}
    return response


def search_similar_vector(search_vector, tags):
    response = _query_builder(tags)
    redis_index_name = os.getenv("SEMANTIC_SEARCH_INDEX_NAME")
    query_params = {"vec": np.array(search_vector).astype(np.float32).tobytes()}

    return r.ft(redis_index_name).search(response["query"], query_params)
