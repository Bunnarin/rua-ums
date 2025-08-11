from django import forms
from django.forms.models import modelform_factory

def get_default_form(flat_fields, model, request=None, form_class=None):
    """
    This exists because the easier option (modelform_factory attach its field validation to the text area and I don't want that)
    """
    class DefaultImportForm(forms.Form):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # create the flat fields
            for field in flat_fields:
                self.fields[field] = forms.CharField(
                    required=False, widget=forms.Textarea
                    )

            # check if the model field not in flat field, then we use the model-form's
            if form_class:
                model_form = form_class(*args, request=request, **kwargs)
            else:
                model_form = modelform_factory(model, fields='__all__')()
            for field in model_form.fields:
                if field not in flat_fields:
                    self.fields[field] = model_form.fields[field]
    return DefaultImportForm

def json_to_schema(template_json):
    schema = {
        "type": "object",
        "keys": {}
    }

    # the rest is string
    type_map = {
        "integer": "integer",
        "number": "number",
        "checkbox": "array",
    }
    
    for field in template_json:
        schema['keys'][field['title']] = {}
        key = schema['keys'][field['title']]

        key["type"] = type_map.get(field['type']) or "string"
        key["required"] = field['required']

        match field['type']:
            case 'paragraph':
                key['widget'] = 'textarea'
            case 'date' | 'date-time' | 'time':
                key['format'] = field['type']
            case 'dropdown':
                key['choices'] = field['choices']
            case 'checkbox':
                key['items'] = {
                    "type": "string",
                    "choices": field['choices'],
                    "widget": "multiselect"
                }
    return schema