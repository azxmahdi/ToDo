from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import redis
import requests
import json

from todo.models import Task
from .serializers import TaskSerializer
from .permissions import DefaultPermission
from .filters import TaskFilter



class TaskViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for managing tasks. It uses Django REST Framework's ModelViewSet,
    which provides CRUD operations by default.

    Attributes:
    queryset: The queryset of Task objects to be used for this ViewSet.
    serializer_class: The serializer class to be used for serializing and deserializing Task objects.
    permission_classes: The list of permission classes to be applied to this ViewSet.
    filter_backends: The list of filter backends to be used for filtering tasks.
    filterset_class: The filterset class to be used for filtering tasks.
    search_fields: The list of fields to be searched when performing a search operation.
    ordering_fields: The list of fields to be used for ordering tasks.
    ordering: The default ordering of tasks.
    """

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [DefaultPermission,IsAuthenticated]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = TaskFilter
    search_fields = ["title"]
    ordering_fields = ["is_done"]
    ordering = ["-is_done"]




# Redis connection
# redis_client = redis.StrictRedis(host='redis', port=6379, db=0)

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

@method_decorator(cache_page(60 * 20), name='dispatch')  
class WeatherAPIView(APIView):
    def get(self, request, city_name):

        # Fetch the weather data from an external API
        api_key = '1e7173b8a2b50e85add91dfd559f83da'
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric'
        response = requests.get(url)

        if response.status_code == 200:
            weather_data = response.json()
            
            return Response(weather_data, status=status.HTTP_200_OK)
        
        return Response({'error': 'City not found'}, status=status.HTTP_404_NOT_FOUND)
    
