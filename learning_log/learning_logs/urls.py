"""Defines URL patterns for learning_logs"""

from django.urls import path   # path is needed to map urls to views
from . import views   # from same directory import the views module (this is what the '.' means

app_name = 'learning_logs'
urlpatterns = [              # app_name and urlpatterns should always be nammed like that as variable names
    # Home Page
    path('', views.index, name='index'),    # the empty string always matches the base url, localhost 8000
    # Page that shows all topics
    path('topics/', views.topics, name='topics'),
    # Detail page for a single topic
    path('topics/<int:topic_id>/', views.topic, name='topic'),
    # Page for adding a new Topic
    path('new_topic/', views.new_topic, name='new_topic'),
    # Page for adding a new entry
    path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
]