from django.forms.widgets import NumberInput

class RangeInput(NumberInput):
    input_type = 'range'