from django.forms import ModelForm
from .models import Geometry, Condition


class GeometryForm(ModelForm):

    class Meta:
        model = Geometry
        exclude = [""]


class ConditionForm(ModelForm):

    class Meta:
        model = Condition
        exclude = [""]