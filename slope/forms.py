from django import forms
from .models import (
    SlopeModel,
    MaterialModel,
    UdlModel,
    PointLoadModel,
)

class SlopeForm(forms.ModelForm):
    class Meta:
        model = SlopeModel
        fields = ('height', 'angle', 'length')

        labels = {
            'height':'Height (m)',
            'angle':'Angle (deg)',
            'length':'Length (m)'
        }

class MaterialForm(forms.ModelForm):
    class Meta:
        model = MaterialModel
        fields = (
            'unit_weight',
            'friction_angle',
            'cohesion',
            'depth_to_bottom',
            'name',
            'color'
        )

        labels = {
            'unit_weight' : 'Unit Weight (kN/m3)',
            'friction_angle': 'Friction Angle (deg)',
            'cohesion' : 'Cohesion (kPa)',
            'depth_to_bottom' : 'Depth to bottom strata (m)',
            'name' : 'Name (optional)',
            'color' : 'Color (optional)',
        }

class UdlForm(forms.ModelForm):
    class Meta:
        model = UdlModel
        fields = (
            'magnitude',
            'offset',
            'length',
            'color',
            'dynamic_offset',
        )

        labels = {
            'magnitude' : 'magnitude (kPa)',
            'offset' : 'offset from crest (m)',
            'length' : 'length of load (m)',
            'color' : 'color (optional)',
            'dynamic_offset': 'dynamic load',
        }

class PointLoadForm(forms.ModelForm):
    class Meta:
        model = PointLoadModel
        fields = (
            'magnitude',
            'offset',
            'color',
            'dynamic_offset',
        )   

        labels = {
            'magnitude' : 'magnitude (kPa)',
            'offset' : 'offset from crest (m)',
            'color' : 'color (optional)',
            'dynamic_offset': 'dynamic load',
        }


class AnalysisOptionsForm(forms.Form):
    plot_choices = [('plot_critical','Plot Critical Failure'),('plot_all_planes','Plot All Failure Planes')]
    analysis_choices = [('normal','Normal Bishop Analysis'),('dynamic', 'Dynamic Bishop Analysis')]
    slope_choices = [('length','Length'),('angle', 'Angle')]

    plot_choice = forms.ChoiceField(choices=plot_choices, label='Plotting Choices', initial=plot_choices[0])
    analysis_choice = forms.ChoiceField(choices=analysis_choices, label='Analysis Choices', initial=analysis_choices[0])
    slope_choice = forms.ChoiceField(choices=slope_choices, label='Define Slope By:', initial=analysis_choices[0])

    critical_FOS = forms.FloatField(min_value=0,max_value = 5, required=True, label = 'Critical FOS', initial = 1.30)
    max_display_FOS = forms.FloatField(min_value=0,max_value = 5, required=True, label = 'Max display FOS', initial = 3)

    prefix = 'options'