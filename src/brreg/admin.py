from django.contrib import admin

from .models import (
    User,
    Company,
    Address,
    LegalForm,
    Industry,
    Activity,
    Status,
    ShareholderRegister,
    HydropowerPlant
)

admin.site.register(User)
admin.site.register(Company)
admin.site.register(Address)
admin.site.register(LegalForm)
admin.site.register(Industry)
admin.site.register(Activity)
admin.site.register(Status)
admin.site.register(ShareholderRegister)
admin.site.register(HydropowerPlant)
