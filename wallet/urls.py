from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


app_name = "Profile"

urlpatterns = [
    path("api/", include("wallet.api.urls")),
]
