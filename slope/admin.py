from django.contrib import admin

# Register your models here.
from .models import (
    SlopeModel,
    MaterialModel,
    UdlModel,
    PointLoadModel,
)

admin.site.register(SlopeModel)
admin.site.register(MaterialModel)
admin.site.register(PointLoadModel)
admin.site.register(UdlModel)
