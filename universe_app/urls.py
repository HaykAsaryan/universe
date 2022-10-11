from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render, redirect
from django.views.generic import RedirectView
from .views import registrationPage, \
                   authorizationPage, \
                   profilePage, \
                   settingsPage, \
                   logoutPage, \
                   recoveryPage, \
                   homePage, \
                   deletePage, \
                   deletePost, \
                   post, \
                   like

urlpatterns = [
    path('registration/', registrationPage, name="registration"),
    path('authorization/', authorizationPage, name="authorization"),
    path('', homePage),
    path('home/', RedirectView.as_view(url='/'), name="home"),
    path('profile/<str:username>/', profilePage, name="profile"),
    path('profile/<str:username>/settings/', settingsPage, name="settings"),
    path('profile/<str:username>/post', post, name="post"),
    path('profile/<str:username>/like', like, name="like"),
    path('post/<str:id>/delete/', deletePost, name="delete"),
    path('recovery/', recoveryPage, name="recovery"),
    path('logout/', logoutPage, name="logout"),
    path('delete/<str:username>/', deletePage, name="delete"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)