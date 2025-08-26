from django.contrib import admin

from .models import FeedbackMessage

class FeedbackMesTabAdmin(admin.TabularInline):
    model = FeedbackMessage
    fields = ['text', 'topic', 'custom_topic']
    search_fields = ['text', 'custom_topic']
    readonly_fields = ('created_at',)
    extra = 1

@admin.register(FeedbackMessage)
class FeedbackMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'topic', 'get_custom_topic', 'status', 'created_at']
    list_filter = ['user', 'topic', 'status', 'created_at']
    list_editable = ['status']
    search_fields = ['text', 'name', 'email', 'custom_topic']
    readonly_fields = ['created_at', 'name', 'user', 'email', 'topic', 'custom_topic', 'text']
    ordering = ['-created_at']

    @admin.display(description='Своя тема')
    def get_custom_topic(self, obj):
        if obj.topic == 'other':
            return obj.custom_topic
        return '-'


