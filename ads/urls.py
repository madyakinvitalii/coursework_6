from django.urls import path
from ads.views import *


urlpatterns = [
    path('', AdListCreateView.as_view(), name='advertisement-list-create'),
    path('me/', AdPersonalListView.as_view()),
    path('<int:pk>/', AdRetrieveUpdateDestroyView.as_view(), name='advertisement-retrieve-update-destroy'),
    path('<int:ad_pk>/comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('<int:ad_pk>/comments/<int:id>/', CommentRetrieveUpdateDestroyView.as_view(), name='comment-retrieve-update'
                                                                                            '-destroy'),
]
