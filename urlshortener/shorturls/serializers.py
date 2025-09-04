import string
import random
from datetime import timedelta
from django.utils import timezone
from rest_framework import serializers
from .models import ShortURL
from .models import Click


def generate_shortcode(length=6):
    """Generate a random shortcode with letters and digits"""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))


class ShortURLSerializer(serializers.ModelSerializer):
    url = serializers.URLField(write_only=True)
    validity = serializers.IntegerField(write_only=True, required=False, min_value=1)
    shortcode = serializers.CharField(write_only=True, required=False, allow_blank=True)

    shortLink = serializers.SerializerMethodField()
    expiry = serializers.DateTimeField(read_only=True)

    class Meta:
        model = ShortURL
        fields = ["url", "validity", "shortcode", "shortLink", "expiry"]

    def get_shortLink(self, obj):
        request = self.context.get("request")
        host = request.get_host() if request else "localhost"
        return f"http://{host}/{obj.shortcode}"

    def create(self, validated_data):
        url = validated_data["url"]
        validity = validated_data.get("validity", 30)  # default 30 min
        shortcode = validated_data.get("shortcode")

        # Generate shortcode if not provided
        if not shortcode:
            shortcode = generate_shortcode()

        # Ensure uniqueness
        while ShortURL.objects.filter(shortcode=shortcode).exists():
            shortcode = generate_shortcode()

        expiry_time = timezone.now() + timedelta(minutes=validity)

        shorturl = ShortURL.objects.create(
            original_url=url,
            shortcode=shortcode,
            expiry=expiry_time,
        )
        return shorturl



class ClickSerializer(serializers.ModelSerializer):
    class Meta:
        model = Click
        fields = ["timestamp", "referrer", "location"]

class ShortURLStatsSerializer(serializers.ModelSerializer):
    click_count = serializers.SerializerMethodField()
    clicks = ClickSerializer(many=True, read_only=True, source="click_set")

    class Meta:
        model = ShortURL
        fields = ["original_url", "created_at", "expiry", "click_count", "clicks"]

    def get_click_count(self, obj):
        return obj.click_set.count()
