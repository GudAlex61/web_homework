from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.new_questions, name='index'),
    path('hot/', views.hot_questions, name='hot'),
    path('tag/<str:tag_name>/', views.questions_by_tag, name='tag'),
    path('question/<int:question_id>/', views.question_page, name='question'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('ask/', views.ask_view, name='ask'),
    path('settings/', views.settings_view, name='settings'),
    path('logout/', views.logout_view, name='logout'), 
]