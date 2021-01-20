
from django.shortcuts import render, redirect

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

def index(request):
    """The home page view for learning log"""

    return render(request, 'learning_logs/index.html')

def topics(request):
    """Show all topics"""

    topics = Topic.objects.order_by('date_added')
    context = {'topics': topics}

    return render(request, 'learning_logs/topics.html', context)

def topic(request, topic_id):
    """Show a single topic and all its entries"""
    topic = Topic.objects.get(id=topic_id)   # this is a querry
    entries = topic.entry_set.order_by('-date_added')   # minus used for reverse order
    context = {"topic": topic, 'entries': entries}

    return render(request, 'learning_logs/topic.html', context)

def new_topic(request):
    """add a new topic"""

    if request.method != 'POST':
        # means no data submitted so you just show a blank form
        form = TopicForm()
    else:
        # POST data submitted and process it
        form = TopicForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topics')  # after submission get redirected to your topics

    # display a blank or invalid form to be sent to the template
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

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

def edit_entry(request, entry_id):
    """edit an entry"""

    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

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