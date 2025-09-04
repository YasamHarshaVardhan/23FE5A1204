import string, random
from datetime import timedelta
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import ShortURL, Click
from .serializers import ShortURLSerializer, ShortURLStatsSerializer


# Utility: generate random shortcode if not provided
def generate_shortcode(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))


# ---------- 1. Create Short URL ----------
class ShortURLCreateView(APIView):
    def post(self, request):
        data = request.data.copy()

        # If no shortcode provided → generate unique one
        if not data.get("shortcode"):
            shortcode = generate_shortcode()
            while ShortURL.objects.filter(shortcode=shortcode).exists():
                shortcode = generate_shortcode()
            data["shortcode"] = shortcode

        # If no validity provided → default 30 minutes
        if not data.get("validity"):
            data["validity"] = 30

        serializer = ShortURLSerializer(data=data, context={"request": request})
        if serializer.is_valid():
            shorturl = serializer.save()
            return Response(
                {
                    "shortLink": f"http://127.0.0.1:8000/{shorturl.shortcode}",
                    "expiry": shorturl.expiry.isoformat()
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ---------- 2. Redirect + Track Click ----------
class RedirectView(APIView):
    authentication_classes = []  # no auth required
    permission_classes = []      # no permissions required

    def get(self, request, shortcode):
        shorturl = get_object_or_404(ShortURL, shortcode=shortcode)

        # Check expiry
        if shorturl.expiry < timezone.now():
            return Response(
                {"error": "This link has expired."},
                status=status.HTTP_410_GONE
            )

        # Track analytics
        referrer = request.META.get("HTTP_REFERER")
        location = request.META.get("REMOTE_ADDR")  # later can replace with geoip
        Click.objects.create(shorturl=shorturl, referrer=referrer, location=location)

        # Increment total clicks
        shorturl.clicks += 1
        shorturl.save(update_fields=["clicks"])

        # Redirect to original URL
        return redirect(shorturl.original_url)


# ---------- 3. Retrieve Statistics ----------
class ShortURLStatsView(APIView):
    def get(self, request, shortcode):
        shorturl = get_object_or_404(ShortURL, shortcode=shortcode)
        serializer = ShortURLStatsSerializer(shorturl)
        return Response(serializer.data, status=status.HTTP_200_OK)

class RedirectView(APIView):
    authentication_classes = []  # no authentication needed
    permission_classes = []      # no permission needed

    def get(self, request, shortcode):
        shorturl = get_object_or_404(ShortURL, shortcode=shortcode)

        # Check expiry
        if shorturl.expiry < timezone.now():
            return Response(
                {"error": "This link has expired."},
                status=status.HTTP_410_GONE
            )

        # Log analytics
        referrer = request.META.get("HTTP_REFERER")
        location = request.META.get("REMOTE_ADDR")  # basic location (IP)
        Click.objects.create(shorturl=shorturl, referrer=referrer, location=location)

        # Increment click count
        shorturl.clicks += 1
        shorturl.save(update_fields=["clicks"])

        # Redirect user to original URL
        return redirect(shorturl.original_url)