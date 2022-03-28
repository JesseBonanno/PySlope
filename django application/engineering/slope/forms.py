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
            'angle':'angle (deg)',
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
            'cohesion' : 'cohesion (kPa)',
            'depth_to_bottom' : 'depth to bottom strata (m)',
            'name' : 'name (optional)',
            'color' : 'color (optional)',
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