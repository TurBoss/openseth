from django.conf.urls import url, include
from rest_framework import routers
from .views import EventViewSet

router = routers.DefaultRouter()
router.register(r'', EventViewSet)

urlpatterns = [
    url(r'^', include(router.urls))
]