from django.urls import path
from .views import NewsList, NewsSearch, NewsDetailView, NewsCreateView, NewsUpdateView, NewsDeleteView # импортируем наше представление
from django.contrib.auth.views import LoginView, LogoutView
from .views import BaseRegisterView
from .views import upgrade_me,Subscribers

urlpatterns = [
    # path — означает путь. В данном случае путь ко всем товарам у нас останется пустым, позже станет ясно почему
    path('', NewsList.as_view()),
    path('search', NewsSearch.as_view()),
    path('<int:pk>', NewsDetailView.as_view(), name='news'),
    path('add/', NewsCreateView.as_view(), name='news_create'),
    path('<int:pk>/edit/', NewsUpdateView.as_view(), name='news_update'),
    path('<int:pk>/delete/', NewsDeleteView.as_view(), name='news_delete'),
    path('login/',
         LoginView.as_view(template_name='login.html'),
         name='login'),
    path('logout/',
         LogoutView.as_view(template_name='logout.html'),
         name='logout'),
    path('signup/',
         BaseRegisterView.as_view(template_name = 'signup.html'),
         name='signup'),
    path('upgrade/', upgrade_me, name = 'upgrade'),
    path('category/', Subscribers),
]