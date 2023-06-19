from django.db.models import QuerySet
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ads.filters import AdFilter
from ads.models import Ad, Comment
from ads.permissions import IsUsersOrUserAdmin
from ads.serializers import AdSerializer, CommentSerializer


class Paginator(PageNumberPagination):
    """Custom pagination class"""
    page_size: int = 4


class AdListCreateView(ListCreateAPIView):
    queryset: QuerySet = Ad.objects.all()
    serializer_class: AdSerializer = AdSerializer
    pagination_class: Paginator = Paginator
    filter_backends: tuple = (DjangoFilterBackend, )
    filterset_class: AdFilter = AdFilter

    permissions: dict = {
        'list': [],
        'create': [IsAuthenticated()],
    }

    def get_permissions(self) -> list:
        """Method to define permissions"""
        return self.permissions.get('create') if self.request.method == 'POST' else []

    @extend_schema(
        description="Retrieve a list of advertisements",
        summary="List of advertisements",
    )
    def get(self, request, *args, **kwargs) -> Response:
        return super().get(request, *args, **kwargs)

    @extend_schema(
        description="Create a new advertisement",
        summary="Create advertisement",
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class AdPersonalListView(ListAPIView):
    serializer_class: AdSerializer = AdSerializer
    pagination_class: Paginator = Paginator
    permission_classes: tuple = (IsAuthenticated, IsUsersOrUserAdmin, )

    def get_queryset(self) -> QuerySet:
        return Ad.objects.filter(author=self.request.user)

    @extend_schema(
        description="Retrieve list of personal advertisements",
        summary="List of user's advertisements",
    )
    def get(self, request, *args, **kwargs) -> Response:
        return super().get(request, *args, **kwargs)


class AdRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset: QuerySet = Ad.objects.all().order_by('-created_at')
    serializer_class: AdSerializer = AdSerializer
    permissions: dict = {
        'retrieve': [IsAuthenticated()],
        'update': [IsAuthenticated(), IsUsersOrUserAdmin()],
        'partial_update': [IsAuthenticated(), IsUsersOrUserAdmin()],
        'destroy': [IsAuthenticated(), IsUsersOrUserAdmin()]
    }

    def get_permissions(self) -> list | None:
        if self.request.method == 'GET':
            return self.permissions.get('retrieve')
        if self.request.method == 'PATCH':
            return self.permissions.get('partial_update')
        if self.request.method == 'DELETE':
            return self.permissions.get('destroy')
        return []

    @extend_schema(
        description="Retrieve one advertisement by pk",
        summary="Retrieve advertisement",
    )
    def get(self, request, *args, **kwargs) -> Response:
        return super().get(request, *args, **kwargs)

    @extend_schema(
        description="Partial update advertisement by pk",
        summary="Update advertisement",
    )
    def patch(self, request, *args, **kwargs) -> Response:
        return super().patch(request, *args, **kwargs)

    @extend_schema(
        description="Full update advertisement by pk",
        summary="Update advertisement",
        deprecated=True
    )
    def put(self, request, *args, **kwargs) -> Response:
        return super().put(request, *args, **kwargs)

    @extend_schema(
        description="Delete user's advertisement by pk",
        summary="Delete advertisement",
    )
    def delete(self, request, *args, **kwargs) -> Response:
        return super().delete(request, *args, **kwargs)


class CommentListCreateView(ListCreateAPIView):
    serializer_class: CommentSerializer = CommentSerializer
    permission_classes: tuple = (IsAuthenticated, )
    pagination_class = Paginator

    def get_queryset(self) -> QuerySet:
        return Comment.objects.filter(ad=self.kwargs.get('ad_pk')).order_by('-created_at')

    @extend_schema(
        description="Retrieve a list of comments from one advertisement by pk",
        summary="List of comments",
    )
    def get(self, request, *args, **kwargs) -> Response:
        return super().get(request, *args, **kwargs)

    @extend_schema(
        description="Create a new comment to advertisement by pk",
        summary="Create comment"
    )
    def post(self, request, *args, **kwargs) -> Response:
        return super().post(request, *args, **kwargs)


class CommentRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class: CommentSerializer = CommentSerializer
    permissions: dict = {
        'retrieve': [IsAuthenticated()],
        'update': [IsAuthenticated(), IsUsersOrUserAdmin()],
        'partial_update': [IsAuthenticated(), IsUsersOrUserAdmin()],
        'destroy': [IsAuthenticated(), IsUsersOrUserAdmin()]
    }

    def get_object(self) -> Comment:
        try:
            return Comment.objects.get(
                pk=self.kwargs['id'],
                ad=self.kwargs['ad_pk']
            )
        except Comment.DoesNotExist:
            raise Http404('Comment does not exist')

    def get_permissions(self) -> list | None:
        if self.request.method == 'GET':
            return self.permissions.get('retrieve')
        if self.request.method == 'PATCH':
            return self.permissions.get('partial_update')
        if self.request.method == 'DELETE':
            return self.permissions.get('destroy')
        return []

    @extend_schema(
        description="Retrieve one comment by pk",
        summary="Retrieve comment",
    )
    def get(self, request, *args, **kwargs) -> Response:
        return super().get(request, *args, **kwargs)

    @extend_schema(
        description="Partial update comment by pk",
        summary="Update comment",
    )
    def patch(self, request, *args, **kwargs) -> Response:
        return super().patch(request, *args, **kwargs)

    @extend_schema(
        description="Full update comment by pk",
        summary="Update comment",
        deprecated=True
    )
    def put(self, request, *args, **kwargs) -> Response:
        return super().put(request, *args, **kwargs)

    @extend_schema(
        description="Delete user's comment by pk",
        summary="Delete comment",
    )
    def delete(self, request, *args, **kwargs) -> Response:
        return super().delete(request, *args, **kwargs)
