from django.urls import path
from .views import SignUpView, IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('signup/', SignUpView.as_view(), name='signup'),
]