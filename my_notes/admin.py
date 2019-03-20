from django.contrib import admin
from .models import Note


class NoteAdmin(admin.ModelAdmin):
    model = Note
    list_display = [
        'created_at',
        'title',
        'added_by',
    ]

    def save_model(self, request, obj, form, change):
        obj.added_by = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Note, NoteAdmin)
