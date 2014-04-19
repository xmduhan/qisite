# Create your views here.

from django.contrib.auth.models import User, Group
from rest_framework import viewsets, routers
import home

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    model = User

class GroupViewSet(viewsets.ModelViewSet):
    model = Group

class CatalogViewSet(viewsets.ModelViewSet):
    model = home.models.Catalog
# Routers provide an easy way of automatically determining the URL conf.

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'catalog', CatalogViewSet)
