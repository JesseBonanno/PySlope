from django.contrib import admin

# Register your models here.
from .models import (
    SlopeModel,
    MaterialModel,
    UdlModel,
    LineLoadModel,
)

admin.site.register(SlopeModel)
admin.site.register(MaterialModel)
admin.site.register(LineLoadModel)
admin.site.register(UdlModel)
