from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from vutman.models import EmailUser, EmailAlias, EmailDomain
from vutman.search_indexes import search_emailaliases, search_emailuser
from vutman.forms import EmailUserForm, EmailAliasForm, EmailAliasFormSet
from itertools import chain


def render_virtual_user_table(request):
    for alias in EmailAlias.objects.all():
        print alias
    return redirect("/vutman")


def index(request):
    user_list = EmailUser.objects.all().order_by('-last_modified')[:10]
    alias_list = EmailAlias.objects.all().order_by('-last_modified')[:10]

    return render_to_response(
        "index.html",
        {
            'user_list': user_list,
            'alias_list': alias_list,
        },
        context_instance=RequestContext(request)
    )


def emailuser_details(request, pk=None):
    emailuser = EmailUser.objects.get(pk=pk)
    domain_list = EmailDomain.objects.all()

    ALIAS_POST = False

    if request.POST:
        if 'alias_name' in request.POST:
            print request.POST
            formset = EmailAliasForm(request.POST)
            if formset.is_valid():
                formset.save()
            ALIAS_POST = True
        else:
            form = EmailUserForm(request.POST, instance=emailuser)
            if form.is_valid():
                form.save()
    else:
        form = EmailUserForm(instance=emailuser)
    if ALIAS_POST:
        form = EmailUserForm(instance=emailuser)

    formset = []
    for alias in EmailAlias.objects.filter(username=emailuser).order_by('state'):
        x = EmailAliasForm(instance=alias)
        formset.append(x)
    formset.append(EmailAliasForm())
    return render_to_response(
        "form.html",
        {
            'form': form,
            'formset': formset,
            'emailuser': emailuser,
            'domain_list': domain_list,
        },
        context_instance=RequestContext(request)
    )


def emailalias_delete(request, pk):
    emailalias = EmailAlias.objects.get(pk=pk)
    emailalias.delete()
    return redirect(emailalias.username.get_absolute_url())


def emailalias_details(request, pk=None):
    emailalias = None
    if pk:
        emailalias = EmailAlias.objects.get(pk=pk)

    if request.POST:
        if emailalias:
            form = EmailAliasForm(request.POST, instance=emailalias)
        else:
            form = EmailAliasForm(request.POST)
            emailalias = form.instance

        if form.is_valid():
            form.save()
        else:
            print form.errors
        return redirect(emailalias.username.get_absolute_url())


def search(request, q=None):
    query_string = q
    if 'q' in request.GET:
        query_string = request.GET['q']

    user_list = []
    alias_list = []
    all_list = []

    if 'alias' in request.GET:
        emailalias_query = search_emailaliases(query_string)
        alias_list = EmailAlias.objects.filter(emailalias_query)

    if 'user' in request.GET:
        emailuser_query = search_emailuser(query_string)
        user_list = EmailUser.objects.filter(emailuser_query)

    all_list = list(chain(user_list, alias_list))

    # If we have only found a single item, then redirect straight to
    # that # item without showing the search.
    # if len(all_list) == 1:
    #     return redirect(all_list[0].get_absolute_url())

    # If we have a handful of results and only one user, check that we
    # are not just pointing the user at the same user.
    if len(user_list) == 1:
        ONE_USER = True
        for alias in alias_list:
            if alias.username != user_list[0]:
                ONE_USER = False
                break
        if ONE_USER:
            return redirect(user_list[0].get_absolute_url())

    if len(alias_list) == 1:
        return redirect(alias_list[0].username.get_absolute_url())


    # If no results, then do not show the results page.
    # Just stay on the search page with a nice message.
    if len(all_list) == 0:
        return redirect(reverse('index'))

    return render_to_response(
        "search_results.html",
        {
            'query_string': query_string,
            'user_list': user_list,
            'alias_list': alias_list
        },
        context_instance=RequestContext(request)
    )
