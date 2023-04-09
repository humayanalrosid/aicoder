from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('fix', views.fix, name='fix'),
    path('suggest', views.suggest, name='suggest'),
    path('past', views.past_code, name='past'),
    path('delete_past/<int:id>', views.delete_past_code, name='delete_past'),

    path('signup', views.signup, name='signup'),
    path('login', views.user_login, name='login'),
    path('logout', views.user_logout, name='logout'),
]
