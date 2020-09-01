from django.urls import path

from .views import ContentUserAPIView, ContentAdminAPIView, SearchAPIView

app_name = 'content'
urlpatterns = [
    path('user/', ContentUserAPIView.as_view()),
    path('admin/', ContentAdminAPIView.as_view()),
    path('search/', SearchAPIView.as_view()),

]