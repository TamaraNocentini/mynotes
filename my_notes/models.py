from django.conf import settings

from django.contrib.postgres import fields
from django.db import models
from django.urls import reverse


class Note(models.Model):
    title = models.CharField(
        max_length=256)
    content = models.TextField()
    tags = fields.ArrayField(
        base_field=models.CharField(
            max_length=128),
        null=True,
        blank=True)
    created_at = models.DateTimeField(
        auto_now_add=True)
    updated_at = models.DateTimeField(
        auto_now=True)
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='+')
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='+')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

    def get_absolute_url(self):
        return reverse(
            'my_notes:detail',
            kwargs={'pk': self.id})
