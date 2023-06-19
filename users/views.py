from django.http import JsonResponse
from djoser.views import UserViewSet
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination

from users.serializers import ChangePasswordSerializer


class Paginator(PageNumberPagination):
    """Custom pagination class"""
    page_size: int = 4


@extend_schema_view(
    list=extend_schema(
        description="List of all users",
        summary="List users",
    ),
    retrieve=extend_schema(
        description="Retrieve one user by pk",
        summary="Retrieve user",
    ),
    create=extend_schema(
        description="Create new user instance",
        summary="Create user",
    ),
    update=extend_schema(
        description="Full update user fields by pk",
        summary="Update user",
        deprecated=True,
    ),
    partial_update=extend_schema(
        description="Partial update user fields by pk",
        summary="Update user",
    ),
    destroy=extend_schema(
        description="Delete user by pk",
        summary="Delete user",
    ),
    me=extend_schema(
        description="Get current user by token",
        summary="Get current user",
    ),
    activation=extend_schema(
        description="Activate user",
        summary="Activate user",
        deprecated=True,
    ),
    me_update=extend_schema(
        description="Update current user by token",
        summary="Update current user",
        deprecated=True,
    ),
    me_partial_update=extend_schema(
        description="Partial update current user by token",
        summary="Update current user",
    ),
)
class CustomUserViewSet(UserViewSet):
    serializer_class: ChangePasswordSerializer = ChangePasswordSerializer
    pagination_class = Paginator

    @action(["post"], detail=False)
    def set_password(self, request, *args, **kwargs) -> JsonResponse:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        self.request.user.set_password(validated_data["new_password"])
        self.request.user.save()
        return JsonResponse(request.data, status=201)
