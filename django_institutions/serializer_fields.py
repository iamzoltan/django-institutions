from django.utils.encoding import force_str
from rest_framework import serializers

from django_institutions import institutions


class InstitutionField(serializers.ChoiceField):
    def __init__(self, *args, **kwargs):
        self.institutions = institutions
        choices = [(inst.name, inst.name) for inst in institutions.institutions.values()]
        super().__init__(choices=choices, allow_blank=True, allow_null=True, *args, **kwargs)

    def to_representation(self, obj):
        if isinstance(obj, str):
            return {"name": force_str(obj)}
        return {"name": force_str(obj._name)}

    def to_internal_value(self, data):
        if data is None or data == "null" or data == "None":
            # Allowing setting the field to None
            return None
        if isinstance(data, dict):
            name = data.get("name")
        elif isinstance(data, str):
            name = data
        else:
            self.fail("invalid_choice", input=data)

        # Validating if the name exists in institutions
        if name not in self.institutions.institutions and name is not None:
            print("Institution {} not found".format(name))
            self.fail("invalid_choice", input=data)

        return name
