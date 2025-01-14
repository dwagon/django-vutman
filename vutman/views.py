from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from vutman.models import EmailUser, EmailAlias, EmailDomain
from vutman.search_indexes import search_emailaliases, search_emailuser
from vutman.forms import EmailUserForm, EmailAliasForm
from itertools import chain


@login_required
def render_virtual_user_table(request):
    alias_list = EmailAlias.objects.all().order_by("username").iterator()

    return render(
        request,
        "emailalias_text.txt",
        {
            "alias_list": alias_list,
        },
    )


@login_required
def index(request):
    user_list = EmailUser.objects.all().order_by("-last_modified")[:25]
    alias_list = EmailAlias.objects.all().order_by("-last_modified")[:25]

    return render(
        request,
        "index.html",
        {
            "user_list": user_list,
            "alias_list": alias_list,
        },
    )


@login_required
def emailuser_details(request, pk=None):
    # If we have been given a pk, then we must have
    # an object to match.
    # If we do not have a pk then assume its a new record
    emailuser = None
    if pk:
        try:
            emailuser = EmailUser.objects.get(pk=pk)
        except Exception:
            messages.warning(request, f"Failed to find user with id {pk}")
            return redirect(reverse("index"))

    domain_list = EmailDomain.objects.all()

    ALIAS_POST = False

    if request.POST:
        if "alias_name" in request.POST:
            formset = EmailAliasForm(request.POST)
            if formset.is_valid():
                messages.success(request, f"alias {formset} was updated")
                formset.save()
            else:
                messages.warning(request, f"alias {formset} update failed")
            ALIAS_POST = True
        else:
            form = EmailUserForm(request.POST, instance=emailuser)
            if form.is_valid():
                messages.success(request, f"User {emailuser} was updated")
                form.save()
                return redirect(form.instance.get_absolute_url())
            else:
                messages.warning(request, f"User {emailuser} update failed")
    else:
        form = EmailUserForm(instance=emailuser)

    if ALIAS_POST:
        form = EmailUserForm(instance=emailuser)

    # Build up a formset
    formset = []
    for alias in EmailAlias.objects.filter(username=emailuser).order_by("state"):
        x = EmailAliasForm(instance=alias)
        formset.append(x)
    formset.append(EmailAliasForm())

    if not emailuser:
        formset = []
        emailuser = EmailUser(fullname="New User")

    return render(
        request,
        "form.html",
        {
            "form": form,
            "formset": formset,
            "emailuser": emailuser,
            "domain_list": domain_list,
        },
    )


@login_required
def emailuser_delete(request, pk):
    try:
        emailuser = EmailUser.objects.get(pk=pk)
        emailuser.delete()
        messages.success(request, f"User {emailuser} was deleted")
    except Exception:
        messages.warning(request, f"User with id {pk} was not found")
    return redirect(reverse("index"))


@login_required
def emailalias_delete(request, pk):
    try:
        emailalias = EmailAlias.objects.get(pk=pk)
        emailalias.delete()
        messages.success(request, f"Alias {emailalias} was deleted")
    except Exception:
        messages.warning(request, f"Alias with id {pk} was not found")
        return redirect(reverse("index"))
    return redirect(emailalias.username.get_absolute_url())


@login_required
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
            messages.success(request, f"Alias {emailalias} was updated")
            form.save()
        else:
            messages.warning(request, f"Alias {emailalias} update failed")

    return redirect(emailalias.username.get_absolute_url())


@login_required
def search(request):
    if "q" not in request.GET:
        messages.warning(request, "Missing query")
        return redirect("/vutman/?missing_query_string")

    query_string = request.GET["q"]

    user_list = []
    alias_list = []

    if "alias" in request.GET:
        alias_list = search_emailaliases(query_string)

    if "user" in request.GET:
        user_list = search_emailuser(query_string)

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
            # Make sure that we have no found a single user,
            # but many different aliases
            if alias.username != user_list[0]:
                ONE_USER = False
                break
        if ONE_USER:
            return redirect(f"{user_list[0].get_absolute_url()}?one_user")

    if len(alias_list) == 1:
        return redirect(f"{alias_list[0].username.get_absolute_url()}?one_alias")

    # If no results, then do not show the results page.
    # Just stay on the search page with a nice message.
    if len(all_list) == 0:
        messages.warning(request, "failed to find any results")
        return redirect(reverse("index"))

    return render(
        request,
        "search_results.html",
        {
            "query_string": query_string,
            "user_list": user_list,
            "alias_list": alias_list,
            "all_list": all_list,
        },
    )
