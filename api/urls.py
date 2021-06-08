from django.urls import path
from .import views

urlpatterns = [
    path('completed/', views.completedList.as_view(), name = 'completed'),
    path('', views.currentTodos.as_view(), name='current'),
    path('todo/<int:pk>/', views.TodoRetrieveUpdateDestroy.as_view(), name = 'update-destroy'),
    path('todo/<int:pk>/complete', views.completedTodo.as_view(), name = 'complete-todo'),

    # auth
    """path('signup',views.signup, name='signup'),
    path('login',views.login, name='login'),"""
]