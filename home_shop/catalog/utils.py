from django.db.models import Q, Max, Min
from random import randint

def q_search(query):
    if query.isdigit() and len(query) <= 5:
        return Q(id=int(query))


    keywords = [word for word in query.split() if len(word) >= 3]

    search = Q()

    for token in keywords:
        search |= Q(name__search=token) | Q(description__search=token)

    return search


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

