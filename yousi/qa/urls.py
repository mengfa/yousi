#!/usr/bin/python3
# -*- coding:utf-8 -*-
# __author__ = '__Jack__'

from django.urls import path

from yousi.qa import views

app_name = 'qa'
urlpatterns = [
    path('', views.UnansweredQuestionsListView.as_view(), name='unanswered_q'),
    path('answered/', views.AnsweredQuestionsListView.as_view(), name='answered_q'),
    path('indexed/', views.QuestionsListView.as_view(), name='all_q'),
    path('question-detail/<int:pk>/', views.QuestionDetailView.as_view(), name='question_detail'),
    path('ask-question/', views.CreateQuestionView.as_view(), name='ask_question'),
    path('propose-answer/<int:question_id>/', views.CreateAnswerView.as_view(), name='propose_answer'),
    path('question/vote/', views.question_vote, name='question_vote'),
    path('answer/vote/', views.answer_vote, name='answer_vote'),
    path('accept-answer/', views.accept_answer, name='accept_answer'),
]
