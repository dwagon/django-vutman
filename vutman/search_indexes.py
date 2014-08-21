from vutman.models import EmailAlias, EmailUser
from django.db.models import Q


def make_search_query(query_string, search_fields):
    # Query to search for every search term
    query = None
    terms = query_string.split()
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
        else:
            query = query & or_query
    return query


def search_emailaliases(query_string):
    fields = [
        'alias_name',
        'username__username',
        'username__fullname',
        'username__active_directory_basedn',
        'email_domain__domain_name',
    ]
    return make_search_query(query_string, fields)


def search_emailuser(query_string):
    fields = [
        'username',
        'fullname',
        'active_directory_basedn',
        'email_server__email_server',
    ]
    return make_search_query(query_string, fields)
