from tag.models import Tag
from tag.serializers import TagSerializer

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


class TagListCreateView(ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class TagDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
