from django.shortcuts import render
from django.forms import modelformset_factory
from django.http import Http404, HttpResponse
from shapely.geometry import Point
import time
import json

# import backend section of code
import os, sys
sys.path.insert(0, os.path.abspath('../../'))

from pySlope.pySlope import (
    Slope,
    Material,
    Udl,
    PointLoad
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
    AnalysisOptionsForm,
)

def index(request):

    #create formsets
    MaterialFormSet = modelformset_factory(MaterialModel, MaterialForm, extra=1)
    UdlFormSet = modelformset_factory(UdlModel, UdlForm, extra = 1)
    PointLoadFormSet = modelformset_factory(PointLoadModel, PointLoadForm, extra=1)

    if request.method == 'GET':
        slope_form = SlopeForm(prefix='slope')
        options_form = AnalysisOptionsForm(prefix='options')

        material_formset = MaterialFormSet(queryset=MaterialModel.objects.none(), prefix='material')
        udl_formset = UdlFormSet(queryset=UdlModel.objects.none(), prefix='udl')
        point_load_formset = PointLoadFormSet(queryset=PointLoadModel.objects.none(), prefix='pointload')

        slope = Slope()
        slope.set_materials(Material())
        plot_json = slope.plot_boundary().update_layout(height=1200,width=2000).to_json()
        plot = slope.plot_boundary().update_layout(height=1200,width=2000).to_html()

        return render(request, 'slope/index.html', {
                "plot_json": plot_json,
                'slope_form' : slope_form,
                'material_formset' : material_formset,
                'udl_formset' : udl_formset,
                'point_load_formset' : point_load_formset,
                'options_form' : options_form,
                'plot' : plot,
                'forms' : [
                    ('Slope', slope_form, 'form'),
                    ('Materials', material_formset, 'formset'),
                    ('Udls', udl_formset, 'formset'),
                    ('PointLoads', point_load_formset, 'formset'),
                    ('OptionsForm', options_form, 'form'),
                ],
                'search' : "[]",
            })
    
    elif request.method == 'POST':
        # initialize form objects with POST information

        slope_form = SlopeForm(request.POST, prefix='slope')

        material_formset = MaterialFormSet(request.POST, prefix='material')
        udl_formset = UdlFormSet(request.POST, prefix='udl')
        point_load_formset = PointLoadFormSet(request.POST, prefix='pointload')
        
        options_form = AnalysisOptionsForm(request.POST, prefix='options')

        form_list = [
            slope_form,
            material_formset,
            udl_formset,
            point_load_formset,
            options_form,
        ]

        # check is valid
        valid = True
        for a in form_list:
            valid *= a.is_valid()
        
        # if form is valid
        if valid:


            slope = create_slope(*form_list)

            #return color_dictionary
            start = time.time()
            # add coordinates of failure planes to information that gets passed back.
            for s in slope._search:
                p = Point(s['c_x'],s['c_y'])
                x, y = p.buffer(s['radius']).boundary.coords.xy

                # empty vectors for circle points that we will actually include
                x_ = []
                y_ = []

                # generate points for circle, will always generate 64 points (65 in list since start and end are same)

                # 65 long list but the last half of points are for the top half of
                # circle and so will never actually be required.
                for i in range(34):
                    # x coordinate should be between left and right
                    # note for y, should be less than left y but can stoop
                    # below right i
                    if x[i] <= s['r_c'][0] and x[i] >= s['l_c'][0] and y[i] <= s['l_c'][1]:
                        x_.append(x[i])
                        y_.append(y[i])

                s['x'] = x_
                s['y'] = y_

            print(start-time.time())

            if options_form.cleaned_data['plot_choice'] == 'plot_critical':
                plot = slope.plot_critical()
            else:
                plot = slope.plot_all_planes(
                    max_fos = options_form.cleaned_data['max_display_FOS']
                )

            plot_json = plot.update_layout(width=2000, height = 1200).to_json()
            plot = plot.update_layout(width=2000, height = 1200).to_html()

            search = slope._search[::]
            search.sort(key=lambda x : x['FOS'])

            return render(request, 'slope/index.html', {
                    'plot_json':plot_json,
                    'slope_form' : slope_form,
                    'material_formset' : material_formset,
                    'udl_formset' : udl_formset,
                    'point_load_formset' : point_load_formset,
                    'options_form' : options_form,
                    'plot' : plot,
                    'forms' : [
                        ('Slope', slope_form, 'form'),
                        ('Materials', material_formset, 'formset'),
                        ('Udls', udl_formset, 'formset'),
                        ('PointLoads', point_load_formset, 'formset'),
                        ('OptionsForm', options_form, 'form'),
                    ],
                    'search' : search,
                })
    
    return HttpResponse('erroer')

def create_slope(
    slope_form,
    material_formset,
    udl_formset,
    point_load_formset,
    options_form,
    ):

    # create beam object
    if options_form.cleaned_data['slope_choice'] == 'length':
        slope = Slope(
            height = slope_form.cleaned_data['height'],
            length = slope_form.cleaned_data['length'],
        )
    else:
        slope = Slope(
            height = slope_form.cleaned_data['height'],
            length = None,
            angle = slope_form.cleaned_data['angle'],
        )

    # add materials to slope
    if material_formset.cleaned_data != [{}]:
        for material_form in material_formset.cleaned_data:
            slope.set_materials(
                Material(
                    unit_weight=material_form['unit_weight'],
                    friction_angle=material_form['friction_angle'],
                    cohesion=material_form['cohesion'],
                    depth_to_bottom=material_form['depth_to_bottom'],
                    name=material_form['name'],
                    color=material_form['color'],
                )
            )
    else:
        slope.set_materials(
            Material(
                unit_weight = MaterialModel._meta.get_field('unit_weight').get_default(),
                friction_angle = MaterialModel._meta.get_field('friction_angle').get_default(),
                cohesion = MaterialModel._meta.get_field('cohesion').get_default(),
                depth_to_bottom = MaterialModel._meta.get_field('depth_to_bottom').get_default(),
                name = MaterialModel._meta.get_field('name').get_default(),
                color = MaterialModel._meta.get_field('color').get_default(),
            )
        )

    # add point loads to slope
    if point_load_formset.cleaned_data != [{}]:
        for point_load_form in point_load_formset.cleaned_data:
            if point_load_form:
                slope.set_pls(
                    PointLoad(
                        magnitude = point_load_form['magnitude'],
                        offset= point_load_form['offset'],
                        color = point_load_form['color'],
                        dynamic_offset = point_load_form['dynamic_offset'],
                    )
                )
    else:
        slope.set_pls(
            PointLoad(
                magnitude = PointLoadModel._meta.get_field('magnitude').get_default(),
                offset= PointLoadModel._meta.get_field('offset').get_default(),
                color = PointLoadModel._meta.get_field('color').get_default(),
                dynamic_offset = PointLoadModel._meta.get_field('dynamic_offset').get_default(),
            )
        )


    # add uniform loads to slope
    if udl_formset.cleaned_data != [{}]:
        for udl_form in udl_formset.cleaned_data:
            if udl_form:
                slope.set_udls(
                    Udl(
                        magnitude = udl_form['magnitude'],
                        offset = udl_form['offset'],
                        length = udl_form['length'],
                        color = udl_form['color'],
                        dynamic_offset = udl_form['dynamic_offset'],
                    )
                )
    else:
        slope.set_udls(
            Udl(
                magnitude = UdlModel._meta.get_field('magnitude').get_default(),
                offset = UdlModel._meta.get_field('offset').get_default(),
                length = UdlModel._meta.get_field('length').get_default(),
                color = UdlModel._meta.get_field('color').get_default(),
                dynamic_offset = UdlModel._meta.get_field('dynamic_offset').get_default(),
            )
        )

    if options_form.cleaned_data['analysis_choice'] == 'normal':
        slope.analyse_slope()
    else:
        slope.analyse_dynamic(
            critical_fos=options_form.cleaned_data['critical_FOS']
        )
    
    return slope