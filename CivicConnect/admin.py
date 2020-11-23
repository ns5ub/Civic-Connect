from django.contrib import admin

# Register your models here.

from .models import Profile, Interest, TemplateSubmission


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'address']


def mark_approved(modeladmin, request, queryset):
    queryset.update(approved=True)
mark_approved.short_description = "Mark selected templates as approved"


class TemplateSubmissionAdmin(admin.ModelAdmin):
    list_display = ['topic', 'template', 'approved']
    actions = [mark_approved]


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Interest)
admin.site.register(TemplateSubmission, TemplateSubmissionAdmin)



