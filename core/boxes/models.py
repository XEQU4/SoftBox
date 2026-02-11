from django.conf import settings
from django.db import models


class Box(models.Model):
    CATEGORY_CHOICES = (
        ('motivation', 'Motivation'),
        ('advice', 'Advice'),
        ('observation', 'Observation'),
        ('confession', 'Confession'),
    )

    number = models.PositiveIntegerField(unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    text = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    opened_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='opened_boxes',
        blank=True
    )


class Comment(models.Model):
    box = models.ForeignKey(
        'Box',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
