# -*- coding: utf-8 -*-

#    File Name：       urls
#    Description :
#    Author :          LvYang
#    date：            5/19/19
#    Change Activity:  5/19/19:
from django.urls import path
from yousi.news import views

app_name = "news"
urlpatterns = [
    path("", views.NewsListView.as_view(), name="list"),
    path('post-news/', views.post_news, name='post_news'),
    path('delete/<pk>/', views.NewsDeleteView.as_view(), name='delete_news'),
    path('like/', views.like, name='like_post'),
    path('get-thread/', views.get_thread, name='get_thread'),
    path('post-comment/', views.post_comment, name='post_comments'),
    path('update-interactions/', views.update_interactions, name='update_interactions'),
]
