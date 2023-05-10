from django.urls import path

from .views import CreateUserView

urlpatterns = [
    path("create_user/", CreateUserView, name="create_user")
]