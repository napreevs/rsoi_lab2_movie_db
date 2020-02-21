from django.urls import path
from .views import UserView, UserDetailView

urlpatterns = [
    path('users/', UserView.as_view(), name='get_post_user'),
    path('users/<int:pk>', UserDetailView.as_view(), name='get_put_delete_user')
]
