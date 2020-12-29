from django.contrib import admin


from ..fields.model import JsonTextField
from ..fields.widgets import JsonEditorWidget


class JsonModelMixin(admin.ModelAdmin):
    formfield_overrides = {
        JsonTextField: {'widget': JsonEditorWidget}
    }

    class Media:
        from django.conf import settings
        static_url = getattr(settings, 'STATIC_URL')

        css = {
            'all': (static_url + 'cso/jsonfield/jsoneditor.min.css',)
        }
        js = (static_url + 'cso/jsonfield/jsoneditor-minimalist.min.js',)

