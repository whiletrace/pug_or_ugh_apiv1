from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import redirect
from django.db.models.query_utils import Q
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.generics import (
    CreateAPIView,
    GenericAPIView, RetrieveUpdateAPIView, UpdateAPIView,
    )


from . import models
from . import serializers


class UserRegisterView(CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    model = get_user_model()
    serializer_class = serializers.UserSerializer


class CreateUpdatePreference(RetrieveModelMixin, UpdateModelMixin,
                             GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    queryset = models.UserPref.objects.all()
    serializer_class = serializers.UserPrefSerializer

    def get_object(self):
        """

        :return:
        :rtype:

        """

        queryset = self.get_queryset()
        user = self.request.user

        try:

            return queryset.filter(user=user).get()
        except models.UserPref.DoesNotExist:
            return models.UserPref.objects.create(user=user)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request,  *args, **kwargs)


class Dogs(RetrieveUpdateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.DogSerializer

    def get_queryset(self):
        user = self.request.user
        preferences = models.UserPref.objects.get(user=user)
        age = preferences.get_age_display()
        gender = preferences.gender
        size = preferences.size
        status = self.kwargs['status']
        dogs = models.Dog.objects.filter(
            Q(age__in=age) & Q(size__in=size) & Q(gender__in=gender))
        exclude = dogs.exclude(Q(user_dogs_query__status='l') | Q(user_dogs_query__status='d'))

        if status == 'liked':
            return dogs.filter(user_dogs_query__status='l',
                               user_dogs_query__user=user)
        elif status == 'disliked':
            return dogs.filter(user_dogs_query__status='d',
                               user_dogs_query__user=user)
        else:
            return exclude

    def get_object(self):
        queryset = self.get_queryset()
        dog = queryset.filter(pk__gt=self.kwargs["pk"])[:1].get()
        try:
            return dog
        except ObjectDoesNotExist:
            raise Http404


class UpdateStatus(UpdateAPIView):
    queryset = models.Dog.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.DogSerializer

    def get_object(self):
        pk = self.kwargs['pk']
        dog = self.queryset.filter(pk__exact=pk)[:1].get()
        user = self.request.user
        try:
            userdog = models.UserDog.objects.get(user=user, dog=dog)
            return userdog
        except models.UserDog.DoesNotExist:
            userdog = models.UserDog.objects.create(dog=dog, user=user)
            return userdog

    def put(self, request, *args, **kwargs):

        status_filter = self.kwargs['status']
        dog = self.get_object()
        if status_filter == 'liked':
            dog.status = 'l'
            dog.save()
        elif status_filter == 'disliked':
            dog.status = 'd'
            dog.save()
        else:
            dog.status = 'u'
            dog.save()
        return Response(status=200)