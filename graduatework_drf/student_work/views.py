from django.db.models import Prefetch, Q
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework.response import Response
from .models import *
from .serializers import *
from student_performance.models import Subject, Group, Lecturer, Users
from .permissions import *
from .utils import *
from .service import *
from .tasks import *
import logging

logger = logging.getLogger(__name__)


class GroupQuestListCreateView(ListCreateAPIView):
    queryset = Quest.objects.all().prefetch_related(
        Prefetch('lecturer', queryset=Lecturer.objects.all().select_related('user').only('user__username'))
    ).select_related('subject', 'group')

    serializer_class = GroupQuestSerializer
    permission_classes = (DetailStudentQuestPermission, IsAuthenticated)
    authentication_classes = (JWTAuthentication,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = QuestFilter

    def get_queryset(self):
        self.queryset = self.queryset.filter(group__slug=self.kwargs['group_slug'])

        return self.queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(queryset, many=True)

        student_quest = UserQuest.objects.filter(date_added__gte=date_filter_sq()).select_related('quest', 'user')
        student_quest_serializer = StudentQuestSerializer(student_quest, many=True)

        return Response({
            'group_quests': serializer.data,
            'student_quests': student_quest_serializer.data
        }, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        send_quests.delay(group=request.data['group'], subject=request.data['subject'],
                          quest_name=request.data['quest_name'])
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class DetailStudentQuestRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = UserQuest.objects.all()
    serializer_class = StudentQuestSerializer
    lookup_field = 'id'
    permission_classes = (DetailStudentQuestPermission, IsAuthenticated)
    authentication_classes = (JWTAuthentication,)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            'detail_student_quest': serializer.data
        }, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CreateStudentQuestCreateView(CreateAPIView):
    queryset = UserQuest.objects.all()
    serializer_class = CreateStudentQuestSerializer

    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class StudentQuestListView(ListAPIView):
    queryset = UserQuest.objects.filter(date_added__gte=date_filter_sq()).select_related('quest', 'user')
    serializer_class = StudentQuestSerializer
