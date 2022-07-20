from vutman.models import EmailAlias, EmailUser
from django.db.models import Q
from itertools import chain

MAX_SEARCH_RESULTS = 200


def make_search_query(query_string, search_fields):
    # Query to search for every search term
    query = None
    terms = query_string.split()
    if not terms:
        raise Exception("Missing query_string")
    for term in terms:
        # Query to search for a given term in each field
        or_query = None
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        # else:
        #    query = query & or_query
    return query


def _search_emailaliases(query_string):
    fields = [
        "alias_name",
        "username__username",
        "username__fullname",
        "username__active_directory_basedn",
        "username__email_server__email_server",
        "email_domain__domain_name",
    ]
    return make_search_query(query_string, fields)


def search_emailaliases(query_string):
    query = _search_emailaliases(query_string)
    return EmailAlias.objects.filter(query)[0:MAX_SEARCH_RESULTS]


def _search_emailuser(query_string):
    fields = [
        "username",
        "fullname",
        "active_directory_basedn",
        "email_server__email_server",
    ]
    return make_search_query(query_string, fields)


def search_emailuser(query_string):
    query = _search_emailuser(query_string)
    return EmailUser.objects.filter(query)[0:MAX_SEARCH_RESULTS]


def search_from_request(request, q=None):
    query_string = q
    if "q" in request.GET:
        query_string = request.GET["q"]
    elif "q" in request.POST:
        query_string = request.POST["q"]
    user_list = []
    alias_list = []
    all_list = []

    if "alias" in request.GET or "alias" in request.POST or q:
        alias_list = search_emailaliases(query_string)

    if "user" in request.GET or "user" in request.POST or q:
        user_list = search_emailuser(query_string)

    all_list = list(chain(user_list, alias_list))
    return {"all_list": all_list, "user_list": user_list, "alias_list": alias_list}
