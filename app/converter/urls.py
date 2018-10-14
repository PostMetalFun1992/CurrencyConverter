from django.contrib import admin
from django.urls import path

from converter_app.views import CurrencyConversionView


urlpatterns = [
    path('conversion/', CurrencyConversionView.as_view()),
    path('admin/', admin.site.urls),
]
