
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

def index(request):
    """The home page view for learning log"""

    return render(request, 'learning_logs/index.html')

@login_required    # a decorator for the topics function
def topics(request):
    """Show all topics"""

    topics = Topic.objects.filter(owner=request.user).order_by('date_added')  # filter shows only the user's topics
    context = {'topics': topics}

    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    """Show a single topic and all its entries"""
    topic = Topic.objects.get(id=topic_id)   # this is a querry

    # make sure that the topic belongs to the current user
    if topic.owner != request.user:
        raise Http404

    entries = topic.entry_set.order_by('-date_added')   # minus used for reverse order
    context = {"topic": topic, 'entries': entries}

    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    """add a new topic"""

    if request.method != 'POST':
        # means no data submitted so you just show a blank form
        form = TopicForm()
    else:
        # POST data submitted and process it
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user   # associate the new topic to the user
            new_topic.save()
            return redirect('learning_logs:topics')  # after submission get redirected to your topics

    # display a blank or invalid form to be sent to the template
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """add a new entry"""

    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        # means no data submitted so you just show a blank form
        form = EntryForm()
    else:
        # POST data submitted and process it
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)   # dont save to the database yet
            new_entry.topic = topic
            new_entry.save()   # now save it together with its topic
            return redirect('learning_logs:topic', topic_id = topic_id)

    # display a blank or invalid form to be sent to the template
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """edit an entry"""

    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # means no data submitted so you just show the previous instance of the form
        form = EntryForm(instance=entry)
    else:
        # POST data submitted and process it
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id = topic.id)

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)