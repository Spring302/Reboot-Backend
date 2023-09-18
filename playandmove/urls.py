from django.urls import path
from .views import text_to_sound

urlpatterns = [
    path('text-to-sound/', text_to_sound, name='text_to_sound'),
]