from django.urls import path
from .views import ShortURLCreateView, RedirectView, ShortURLStatsView

urlpatterns = [
   
    path('', ShortURLCreateView.as_view(), name="create-short-url"),
    path('<str:shortcode>', RedirectView.as_view(), name="redirect-short-url"),    
    path('<str:shortcode>/stats/', ShortURLStatsView.as_view(), name="shorturl-stats"),
    
]
