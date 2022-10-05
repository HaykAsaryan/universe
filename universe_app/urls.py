from unicodedata import name
from django.urls import path
from .views import registrationPage, authorizationPage, profilePage, settingsPage, logoutPage, recoveryPage

urlpatterns = [
    path('registration/', registrationPage, name="registration"),
    path('authorization/', authorizationPage, name="authorization"),
    path('profile/<str:username>/', profilePage, name="profile"),
    path('profile/<str:username>/settings/', settingsPage, name="settings"),
    path('recovery/', recoveryPage, name="recovery"),
    path('logout/', logoutPage, name="logout")
]