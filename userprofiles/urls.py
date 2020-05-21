from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


app_name = "users"

urlpatterns = [
    path("api/", include("userprofiles.api.urls")),
]
