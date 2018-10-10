from django.contrib import admin
from django.urls import path

from converter_app.views import CurrencyConversationView


urlpatterns = [
    path('conversation/', CurrencyConversationView.as_view()),
    path('admin/', admin.site.urls),
]
