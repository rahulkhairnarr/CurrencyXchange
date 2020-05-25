from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


app_name = "wallet"

urlpatterns = [
    path("api/", include("wallet.api.urls")),
]
