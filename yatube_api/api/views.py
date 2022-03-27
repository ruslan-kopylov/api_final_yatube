from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (IsAuthenticatedOrReadOnly,
                                        IsAuthenticated)
from rest_framework.filters import SearchFilter

from posts.models import Post, Group, Follow
from .permissions import AuthorOrReadOnly
from .serializers import (FollowSerializer, PostSerializer,
                          GroupSerializer, CommentSerializer)


class CreateMixin(mixins.CreateModelMixin, viewsets.GenericViewSet):
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostViewSet(CreateMixin, viewsets.ModelViewSet):
    permission_classes = [AuthorOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(CreateMixin, viewsets.ModelViewSet):
    permission_classes = [AuthorOrReadOnly]
    serializer_class = CommentSerializer

    def get_queryset(self):
        post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        return post.comments.all()


class FollowViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = FollowSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('following__username',)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)
