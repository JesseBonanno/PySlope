from django.shortcuts import render
from django.forms import modelformset_factory
from django.http import HttpResponse

from .pySlope import (
    Slope,
    Material,
    Udl,
    PointLoad,
)

from .models import (
    SlopeModel,
    MaterialModel,
    UdlModel,
    PointLoadModel,
)

from .forms import (
    SlopeForm,
    MaterialForm,
    UdlForm,
    PointLoadForm,
)

def index(request):

    #create formsets
    MaterialFormSet = modelformset_factory(MaterialModel, form=MaterialForm, extra=1)
    UdlFormSet = modelformset_factory(UdlModel, UdlForm, extra = 1)
    PointLoadFormSet = modelformset_factory(PointLoadModel, PointLoadForm, extra=1)

    if request.method == 'GET':
        slope_form = SlopeForm(prefix='slope')

        material_formset = MaterialFormSet(queryset=MaterialModel.objects.none(), prefix = 'material')
        udl_formset = UdlFormSet(queryset=UdlModel.objects.none(), prefix='udl')
        point_load_formset = PointLoadFormSet(queryset=PointLoadModel.objects.none(), prefix='pointload')

        slope = Slope()
        slope.set_materials(Material())
        plot = slope.plot_boundary().to_html()

        return render(request, 'slope/index.html', {
            'slope_form' : slope_form,
            'material_formset' : material_formset,
            'udl_formset' : udl_formset,
            'point_load_formset' : point_load_formset,
            'plot' : plot,
            'forms' : [
                ('Slope', slope_form, 'form'),
                ('Materials', material_formset, 'formset'),
                ('Udls', udl_formset, 'formset'),
                ('PointLoads', point_load_formset, 'formset'),
            ]
        })

    elif request.method == 'POST':
        return HttpResponse('Error with information')