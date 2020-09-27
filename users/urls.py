from django.urls import path

from users.views import ProfileDetailView, ProfileUpdate

urlpatterns = [
    path('<uuid:pk>/', ProfileDetailView.as_view(), name='profile_detail'),
    path('<uuid:pk>/update/', ProfileUpdate.as_view(), name='profile_update'),
]
