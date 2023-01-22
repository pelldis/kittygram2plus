from rest_framework import permissions, viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.throttling import AnonRateThrottle
from rest_framework.pagination import LimitOffsetPagination
from .paginaition import CatsPagination

from .permissions import OwnerOrReadOnly
from .models import Achievement, Cat, User

from .serializers import AchievementSerializer, CatSerializer, UserSerializer


class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    permission_classes = (OwnerOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,
                       filters.OrderingFilter)
    throttle_classes = (AnonRateThrottle,)
    pagination_class = None
    filterset_fields = ('color', 'birth_year', 'achievements__name',
                        'owner__username')
    ordering_fields = ('name', 'birth_year')
    ordering = ('-birth_year',)
    search_fields = ('name',)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user) 


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
