from django.urls import include, path
from rest_framework import routers, serializers, viewsets
from .models import Event

# Serializers define the API representation.
class EventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Event
        fields = ['title', 'description', 'start_date', 'active']

# ViewSets define the view behavior.
class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'', EventViewSet)

urlpatterns = [
    path('', include(router.urls)),
]