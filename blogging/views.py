"""blogging/views.py"""

from django.shortcuts import render, redirect
from django import forms
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader

from blogging.models import Post
from blogging.forms import PostForm

def stub_view(request, *args, **kwargs):
    body = "Stub View\n\n"
    if args:
        body += "Args:\n"
        body += "\n".join(["\t%s" % a for a in args])
    if kwargs:
        body += "Kwargs:\n"
        body += "\n".join(["\t%s: %s" % i for i in kwargs.items()])    
    return HttpResponse(body, content_type="text/plain")


# All views must accept a request and return a response
def list_view(request):
    # This view begins by acquiring the data needed for the response
    published = Post.objects.exclude(published_date__exact=None)
    posts = published.order_by('-published_date')

    # Then it builds a context for injection into the template
    context = {'posts': posts}

    # Then it uses a stock Django to identify the template, inject the 
    # context, render the template and return the response
    return render(request, 'blogging/list.html', context)


def detail_view(request, post_id):
    published = Post.objects.exclude(published_date__exact=None)
    try:
        post = published.get(pk=post_id)
    except Post.DoesNotExist:
        raise Http404
    context = {'post': post}
    return render(request, 'blogging/detail.html', context)


def add_model(request):
    """View to add a new entry to the Post database. Works with form.py."""

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.timestamp = timezone.now()
            model_instance.save()
            return redirect('/')

    else:
        form = PostForm()
        return render(request, "blogging/post-form.html", {'form': form})
