from libs.redis_libs import search_similar_vector, set_value_from_hash
from libs.instrumentation import log_error, log_info, tat
import time
import json

def get_params_from_redis_document(document, param, fall_back=""):
    try:
        return document[param]
    except Exception as ex:
        return fall_back


def get_first_product(bundles, bundles_product_mappings):
    user_bundles_list = bundles.split(",")
    for bundle in user_bundles_list:
        for mapping in bundles_product_mappings:
            if mapping['bundle_id'] == bundle:
                return mapping['product']
    return " "


def transform_search_response_single(response, bundles):
    log_info(
        service="redis",
        event_type="get_dashboard_details_from_single_search_response",
        event_value="invoke",
        details={},
    )
    start_time = time.time()
    document_id = response["id"]
    [document_id_prefix, dashboard_public_id] = document_id.split(":")
    dashboard_name = get_params_from_redis_document(response, "dashboard_name")
    tags = get_params_from_redis_document(response, "tag")
    score = get_params_from_redis_document(response, "score")
    bundles_product_mappings=get_params_from_redis_document(response, "bundles_product_mappings",[])
    bundles_product_mappings = json.loads(bundles_product_mappings.replace("'", "\"")) if bundles_product_mappings else bundles_product_mappings
    product = get_first_product(bundles, bundles_product_mappings)
    end_time = time.time()
    log_info(
        service="redis",
        event_type="get_dashboard_details_from_single_search_response",
        event_value="success",
        details={"tat": tat(starting_time=start_time, ending_time=end_time)},
    )
    return {
        "dashboard_public_id": dashboard_public_id,
        "dashboard_name": dashboard_name,
        "tags": tags,
        "score": score,
        "product": product,
    }


def transform_search_response_list(response, bundles):
    return list(map(lambda search_resp: transform_search_response_single(search_resp, bundles), response.docs))


def get_similar_dashboards(user_query_embedded, bundles):
    """
    Retrieve IDs of descriptions similar to the user query based on embedded vectors stored in Redis.

    Parameters:
    -----------
    user_query_embedded_bytes : numpy.ndarray
        The embedded vector representing the user query.
    threshold : float, optional (default=0.4)
        The similarity threshold to consider when comparing vectors.
        Vectors with similarity scores greater than or equal to this threshold will be considered similar.

    Returns:
    --------
    List[Tuple[str, float]]
        A list of tuples containing IDs of descriptions similar to the user query, along with their similarity scores.
        Each tuple contains a description ID (as a string) and its similarity score (as a float).

    Notes:
    ------
    This function retrieves stored vectors associated with keys in the Redis database and calculates
    the similarity between the user query vector and these stored vectors. If the similarity between
    the user query and a stored vector is above the specified threshold, the description ID along with
    its similarity score is included in the returned list.

    """
    log_info(
        service="redis",
        event_type="get_similar_dashboards",
        event_value="invoke",
        details={},
    )
    start_time = time.time()
    response = search_similar_vector(user_query_embedded, bundles)
    dashboard_details = transform_search_response_list(response, bundles)
    end_time = time.time()
    log_info(
        service="redis",
        event_type="get_similar_dashboards",
        event_value="success",
        details={"tat": tat(starting_time=start_time, ending_time=end_time)},
    )
    return dashboard_details


def update_bundles_redis(dashboard_public_id, bundles):
    field_to_set = "tag"
    status = set_value_from_hash(dashboard_public_id, field_to_set, bundles)
    return status
