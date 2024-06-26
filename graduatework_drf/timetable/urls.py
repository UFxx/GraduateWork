from django.urls import path

from .views import *

urlpatterns = [
    path('timetable/<slug:group_slug>/', TimetableListView.as_view(), name='timetable'),
    path('exam/<slug:group_slug>/', ExamListView.as_view(), name='exam'),
    path('timetable_changes/<slug:group_slug>/', TimetableChangesListView.as_view(), name='timetable_changes'),
    path('timetable_lector/', LectorTimeTableListView.as_view(), name='timetable_lector'),
    path('journals/', JournalListView.as_view(), name='journals'),
    path('journal/<int:id>/', JournalRetrieveView.as_view(), name='journal'),
    path('lesson/<int:id>/', LessonDetailRetrieveUpdateDestroyView.as_view(), name='lesson')
]