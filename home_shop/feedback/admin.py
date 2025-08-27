import pandas as pd
import datetime

from django.contrib import admin
from django.http import HttpResponse

from .models import FeedbackMessage

from home_shop.utils import action

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
    actions = ['make_archived', 'export_to_csv']

    @admin.display(description='Своя тема')
    def get_custom_topic(self, obj):
        if obj.topic == 'other':
            return obj.custom_topic
        return '-'
    
    @action('Архивировать выбранные обращения')
    def make_archived(modeladmin, request, queryset):
        queryset.update(status='archived')
        modeladmin.message_user(request, f"{queryset.count()} объект(а/ов) архивировано")

    @action('Экспорт в xlsx')
    def export_to_xlsx(modeladmin, request, queryset):
        response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
        cur_date = datetime.datetime.now().strftime('%d_%m_%y_%H:%M')
        response['Content-Disposition'] = f'attachment; filename="export_feedback_messages_{cur_date}.xlsx"'
        data = []
        
        for message in queryset:
            cur_row = {
                'name': message.name,
                'email': message.email,
                'topic': message.get_topic_display(),
                'custom_topic': message.custom_topic,
                'status': message.get_status_display(),
                'date': message.created_at.strftime('%Y-%m-%d %H:%M'),
                'text': message.text
            }
            data.append(cur_row)
        df = pd.DataFrame(data)
        df.to_excel(response, index=False)
        return response



