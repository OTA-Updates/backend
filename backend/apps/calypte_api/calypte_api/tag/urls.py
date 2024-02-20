from tag.views import TagDetailView, TagListCreateView

from django.urls import URLPattern, URLResolver, path


urlpatterns: list[URLPattern | URLResolver] = [
    path(
        "tags/",
        TagListCreateView.as_view(),
        name="tag-list-create",
    ),
    path(
        "tags/<int:pk>/",
        TagDetailView.as_view(),
        name="tag-detail",
    ),
]
