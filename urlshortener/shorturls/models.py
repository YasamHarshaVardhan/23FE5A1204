from django.db import models


class ShortURL(models.Model):
    original_url = models.TextField()
    shortcode = models.CharField(max_length=20, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expiry = models.DateTimeField()
    clicks = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.shortcode} → {self.original_url}"


class Click(models.Model):
    shorturl = models.ForeignKey(ShortURL, related_name="clicks_data", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    referrer = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Click on {self.shorturl.shortcode} at {self.timestamp}"
