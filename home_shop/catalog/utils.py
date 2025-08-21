from django.db.models import Q, Max, Min
from django.contrib.postgres.search import SearchVector, SearchQuery

from random import randint

def q_search(query):
        vector = SearchVector('name', 'description')
        search_query = SearchQuery(query)
        return vector, search_query


def random_list_ids_for_model(model):
    agg = model.objects.aggregate(max_id=Max('id'), min_id=Min('id'))
    start = agg['min_id']
    end = agg['max_id']
    result_ids = []
    count = 0
    while count < 4:
        cur_random_id = randint(start, end)
        if cur_random_id not in result_ids:
            result_ids.append(cur_random_id)
            count += 1
    return result_ids

