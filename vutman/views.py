from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Q
from vutman.models import EmailUser, EmailAlias
from vutman.search_indexes import search_emailaliases, search_emailuser
from vutman.forms import EmailUserForm, EmailAliasForm, EmailAliasFormSet


def index(request):
    user_list = EmailUser.objects.all()
    return render_to_response(
        "index.html",
        {
            'user_list': user_list
        },
        context_instance=RequestContext(request)
    )


def emailuser_details(request, pk=None):
    emailuser = EmailUser.objects.get(pk=pk)
    if request.POST:
        form = EmailUserForm(request.POST, instance=emailuser)
        form_inline = EmailAliasFormSet(request.POST, instance=emailuser)

        print form.is_valid()
        print form_inline.is_valid()

    else:
        form = EmailUserForm(instance=emailuser)
        form_inline = EmailAliasFormSet(instance=emailuser, prefix="nested")

    return render_to_response(
        "form.html",
        {
            'form': form,
            'form_inline': form_inline,
            'emailuser': emailuser,
        },
        context_instance=RequestContext(request)
    )


def emailalias_details(request, pk):
    alias_list = EmailAlias.objects.filter(pk=pk)
    return render_to_response(
        "index.html",
        {
            'alias_list': alias_list
        },
        context_instance=RequestContext(request)
    )


def search(request, q=None):
    query_string = q
    if 'q' in request.POST:
        query_string = request.POST['q']

    user_list = []
    alias_list = []

    if 'alias' in request.POST:
        emailalias_query = search_emailaliases(query_string)
        alias_list = EmailAlias.objects.filter(emailalias_query)

    if 'user' in request.POST:
        emailuser_query = search_emailuser(query_string)
        user_list = EmailUser.objects.filter(emailuser_query)

    return render_to_response(
        "search_results.html",
        {
            'query_string': query_string,
            'user_list': user_list,
            'alias_list': alias_list
        },
        context_instance=RequestContext(request)
    )
