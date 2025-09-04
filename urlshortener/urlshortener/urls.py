from django.contrib import admin
from django.urls import path, include
from shorturls.views import RedirectView   # import redirect here

urlpatterns = [
    path('admin/', admin.site.urls),

    # All API endpoints (create + stats)
    path('shorturls/', include('shorturls.urls')),

    # Redirection (must be at project root)
    path('<str:shortcode>/', RedirectView.as_view(), name="redirect-short-url"),
]
