import pint
from django.core.exceptions import ValidationError
from pint.errors import  UndefinedUnitError

valid_unit_measurements = ['pounds','lbs','oz','gram']


def validate_unit_of_measure(value):
    ureg = pint.UnitRegistry()
    try:
        single_unit = ureg[value]
    except UndefinedUnitError as e:
        raise ValidationError(f"{e}")
    except :
         raise  ValidationError(f"{value} value is not valid measure")
    # if value not in valid_unit_measurements:\
    #     raise ValidationError(f"{value} value is not valid")