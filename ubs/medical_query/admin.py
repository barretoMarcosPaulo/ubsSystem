from django.contrib import admin

# Register your models here.
from .models import Query, CID10
from import_export.admin import ImportExportModelAdmin
from import_export import resources,fields
from import_export.widgets import ForeignKeyWidget

admin.site.register(Query) 

class CID10Resource(resources.ModelResource):
    class Meta:
        import_id_fields = ('idCID10',)
        model = CID10
        exclude = ('created_on', 'updated_on')

@admin.register(CID10)
class CID10Resource(ImportExportModelAdmin):
    resource_class = CID10Resource