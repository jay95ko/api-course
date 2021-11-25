from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from .models import Room, Photo
from .serializers import RoomSerializer
from .permissions import IsOwner
# Create your views here.

class RoomViewSet(ModelViewSet):

    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            permission_classes = [permissions.AllowAny]

        elif self.action == "create":
            permission_classes = [permissions.IsAuthenticated]

        else:
            #변경하려고 하는 사람이랑 방의 주인이 같은 경우
            #이 경우는 우리가 직접 만들어 줘야함
            permission_classes = [IsOwner]
        
        return [permission() for permission in permission_classes]


    @action(detail=False)
    def search(self, request):
        max_price = request.GET.get("max_price", None)
        min_price = request.GET.get("min_price", None)
        beds = request.GET.get("beds", None)
        bedrooms = request.GET.get("bedrooms", None)
        bathrooms = request.GET.get("bathrooms", None)
        filter_kwargs = {}

        if max_price is not None:
            filter_kwargs["price__lte"] = max_price
        if min_price is not None:
            filter_kwargs["price__gte"] = min_price
        if beds is not None:
            filter_kwargs["beds__gte"] = beds
        if bedrooms is not None:
            filter_kwargs["bedrooms__gte"] = bedrooms
        if bathrooms is not None:
            filter_kwargs["bathrooms__gte"] = bathrooms
        paginator = self.paginator
        try:
            rooms = Room.objects.filter(**filter_kwargs)
        except ValueError:
            rooms = Room.objects.all()

        results = paginator.paginate_queryset(rooms, request)
        serializer = RoomSerializer(results, many=True)

        return paginator.get_paginated_response(serializer.data)