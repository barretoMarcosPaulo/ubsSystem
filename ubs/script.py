import tablib
from import_export import resources
from ubs.patient.models import *

class BookResource(resources.ModelResource):

    class Meta:
        import_id_fields = ('codIBGE_UF',)
        model = State

book_resource = BookResource()
dataset = tablib.Dataset(['1','2','3','4'], headers=['codIBGE_UF','State_codIBGE_UF','UF','region'])
result = book_resource.import_data(dataset, dry_run=True)
print(result.has_errors())
# if not result.has_errors():
result = book_resource.import_data(dataset, dry_run=False)