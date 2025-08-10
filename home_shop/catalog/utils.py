from django.db.models import Q


def q_search(query):
    if query.isdigit() and len(query) <= 5:
        return Q(id=int(query))


    keywords = [word for word in query.split() if len(word) >= 3]

    search = Q()

    for token in keywords:
        search |= Q(name__search=token) | Q(description__search=token)

    return search

