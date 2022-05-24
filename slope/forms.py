from django import forms
from .models import (
    SlopeModel,
    MaterialModel,
    UdlModel,
    LineLoadModel,
    WaterTableModel,
    LimitsModel,
)

from .widgets import RangeInput


class SlopeForm(forms.ModelForm):
    class Meta:
        model = SlopeModel
        fields = ("height", "angle", "length")

        labels = {
            "height": "Height (m)",
            "angle": "Angle (deg)",
            "length": "Length (m)",
        }


class MaterialForm(forms.ModelForm):
    class Meta:
        model = MaterialModel
        fields = (
            "unit_weight",
            "friction_angle",
            "cohesion",
            "depth_to_bottom",
            "name",
            "color",
        )

        labels = {
            "unit_weight": "Unit Weight (kN/m3)",
            "friction_angle": "Friction Angle (deg)",
            "cohesion": "Cohesion (kPa)",
            "depth_to_bottom": "Depth to bottom strata (m)",
            "name": "Name (optional)",
            "color": "Color (optional)",
        }


class UdlForm(forms.ModelForm):
    class Meta:
        model = UdlModel
        fields = (
            "magnitude",
            "offset",
            "length",
            "color",
            "dynamic_offset",
        )

        labels = {
            "magnitude": "magnitude (kPa)",
            "offset": "offset from crest (m)",
            "length": "length of load (m)",
            "color": "color (optional)",
            "dynamic_offset": "dynamic load",
        }


class LineLoadForm(forms.ModelForm):
    class Meta:
        model = LineLoadModel
        fields = (
            "magnitude",
            "offset",
            "color",
            "dynamic_offset",
        )

        labels = {
            "magnitude": "magnitude (kN)",
            "offset": "offset from crest (m)",
            "color": "color (optional)",
            "dynamic_offset": "dynamic load",
        }


class AnalysisOptionsForm(forms.Form):

    analysis_choices = [
        ("normal", "Normal Bishop Analysis"),
        ("dynamic", "Dynamic Bishop Analysis"),
    ]
    slope_choices = [("length", "Length"), ("angle", "Angle")]

    analysis_choice = forms.ChoiceField(
        choices=analysis_choices, label="Analysis Choices", initial=analysis_choices[0]
    )
    slope_choice = forms.ChoiceField(
        choices=slope_choices, label="Define Slope By:", initial=analysis_choices[0]
    )

    critical_FOS = forms.DecimalField(
        min_value=0.0,
        max_value=5.0,
        required=True,
        label="Critical FOS",
        initial=1.50,
        widget=forms.TextInput(
            attrs={
                "step": "0.1",
                "type": "range",
                "value": "2.0",
                "min": "0.1",
                "max": "5",
            }
        ),
    )

    max_display_FOS = forms.DecimalField(
        min_value=0.0,
        max_value=5.0,
        required=True,
        label="Max display FOS",
        initial=2.0,
        widget=forms.TextInput(
            attrs={
                "step": "0.1",
                "type": "range",
                "value": "2.0",
                "min": "0.1",
                "max": "5",
            }
        ),
    )

    iterations = forms.IntegerField(
        min_value=500,
        max_value=5000,
        required=True,
        label="Iterations",
        initial=500,
        widget=RangeInput(attrs={"step": 250}),
    )

    slices = forms.IntegerField(
        min_value=10,
        max_value=50,
        required=True,
        label="Slices",
        initial=25,
        widget=RangeInput(attrs={"step": 5}),
    )

    prefix = "options"


class WaterTableForm(forms.ModelForm):
    class Meta:
        model = WaterTableModel
        fields = (
            "consider_water",
            "water_depth",
        )

        labels = {
            "consider_water": "Consider Water Table?",
            "water_depth": "Water Depth from Crest (m)",
        }


class LimitsForm(forms.ModelForm):
    class Meta:
        model = LimitsModel
        fields = (
            "consider_limits",
            "left_x",
            "right_x",
            "consider_internal_limits",
            "left_x_right",
            "right_x_left",
        )

        labels = {
            "consider_limits": "Consider Limits?",
            "left_x": "left x coordinate (m)",
            "right_x": "right x coordinate (m)",
            "consider_internal_limits": "Consider Internal Limits?",
            "left_x_right": "left internal x coordinate (m)",
            "right_x_left": "right internal x coordinate (m)",
        }
