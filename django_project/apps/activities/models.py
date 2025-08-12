from django.db import models
from django.db.models import Q
from django.conf import settings
from django_jsonform.models.fields import JSONField
from apps.organization.mixins import OrganizationNullMixin

# Create your models here.
class ActivityTemplate(models.Model):
    """
    Stores JSON-based templates for creating activities.
    
    Attributes:
        name: Unique name for the template
        template_definition: JSON field storing the template structure
    """
    TEMPLATE_SCHEMA = {
        "type": "array",
        "items": {
            "type": "object",
            "keys": {
                "title": {"type": "string"},
                "type": {"type": "string",
                        "choices": [
                            "text",
                            "paragraph",
                            "integer",
                            "number",
                            "date",
                            "date-time",
                            "time",
                            "dropdown",
                            "checkbox"
                        ]},
                "required": {"type": "boolean"},
                "choices": {"type": "array", "items": {"type": "string"}}
            }
        }
    }
    
    name = models.CharField(max_length=255, unique=True)
    template_definition = JSONField(schema=TEMPLATE_SCHEMA)

    def __str__(self): 
        return self.name

class Activity(OrganizationNullMixin):
    """
    Stores user responses to activity templates with row-level security.
    """
    template = models.ForeignKey(ActivityTemplate, null=True, on_delete=models.SET_NULL, editable=False)
    response = JSONField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False)
    created_at = models.DateField(auto_now_add=True, editable=False)

    def get_user_rls_filter(self, user):
        return Q(author=user)

    def __str__(self): 
        return f"{self.template.name if self.template else ''} activity created by {self.author} on {self.created_at.strftime('%Y-%m-%d')}"

    class Meta:
        verbose_name_plural = "Activities"