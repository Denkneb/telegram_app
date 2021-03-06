from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('telegram_app.api.urls')),
    path('bot/', include('telegram_app.bot.urls')),
]
