from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import add_to_flashcards, flashcards
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('', views.home, name='home'),# Hauptseite
    path('register/', auth_views.LoginView.as_view(template_name='vocabulary/register.html'), name='register'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='vocabulary/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('word_list/', views.word_list, name='word_list'),
    path('search/', views.search_word, name='search_word'),  # Hier wird 'search_word' registriert
    path('add-to-flashcards/', add_to_flashcards, name='add_to_flashcards'),
    path('flashcards/', views.flashcards, name='flashcards'),
    path('remove-flashcard/<int:flashcard_id>/', csrf_exempt(views.remove_flashcard), name='remove_flashcard'),

    path('links/grammatik/', views.grammatik_links, name='grammatik_links'),
    path('links/redewendung/', views.redewendung_links, name='redewendung_links'),
    path('links/nomen-verbindung/', views.nomen_verbindung_links, name='nomen_verbindung_links'),
    path('links/wörterbuch/', views.woerterbuch_links, name='wörterbuch_links'),
    path('links/video/', views.video_links, name='video_links'),
    path('links/podcast/', views.podcast_links, name='podcast_links'),
    path('links/sonstige/', views.sonstige_links, name='sonstige_links'),

]
