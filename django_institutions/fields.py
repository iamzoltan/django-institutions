from django.utils.encoding import force_str
from django.db.models.fields import BLANK_CHOICE_DASH, CharField
from django_institutions import Institutions, institutions
from typing import List, Any, Type, Optional


# TODO: Sort out other fields
class Institution:
    def __init__(
        self,
        name: str,
        # domains: List[str],
        # web_pages: List[str],
        # country: str,
        # alpha_two_code: str,
        # state_province: Optional[str]
    ) -> None:
        self._name = name
        # self.domains = domains
        # self.web_pages = web_pages
        # self.country = country
        # self.alpha_two_code = alpha_two_code
        # self.state_province = state_province

    def __str__(self):
        return force_str(self._name) or ""

    def __eq__(self, other):
        return force_str(self._name or "") == force_str(other or "")

    def __ne__(self, other):
        return not self.__eq__(other)

    def __bool__(self):
        return bool(self._name)

    def __len__(self):
        return len(force_str(self))

    @property
    def institutions(self):
        """
        TODO: add ability to use custom institutions
        """
        return institutions

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    def to_dict(self):
        return {
            "name": self._name
        }


class InstitutionDescriptor:
    """
    A descriptor for the Institution field on a model instance.
    Returns an Institution when accessed to enable things like:

        >>> from user import user
        >>> user = User.objects.get(username='test')

        >>> user.institution.name
        'University of Test'

        >>> user.insttitution.domains
        ['test.com']
    """

    def __init__(self, field):
        self.field = field

    def __get__(self, instance=None, owner=None):
        if instance is None:
            return self

        # Check in case this dield was deferred.
        if self.field.name not in instance.__dict__:
            instance.refresh_from_db(fields=[self.field.name])
        value = instance.__dict__[self.field.name]
        return self.institution(name=value)

    def institution(
        self,
        name,
        # domains,
        # web_pages,
        # country,
        # alpha_two_code,
        # state_province
    ):
        return Institution(
            name=name,
            # domains=domains,
            # web_pages=web_pages,
            # country=country,
            # alpha_two_code=alpha_two_code,
            # state_province=state_province
        )

    def __set__(self, instance, value):
        if isinstance(value, Institution):
            value = value.name
        value = self.field.get_clean_value(value)
        instance.__dict__[self.field.name] = value


class InstitutionField(CharField):
    """
    An institution field for Django models that provides all institions 
    included in this repo as choices.
    """

    descriptor_class = InstitutionDescriptor
    institutions: Institutions

    def __init__(self, *args: Any, **kwargs: Any):
        institutions_class: Type[Institutions] = kwargs.pop(
            "institutions", None)
        self.institutions = institutions_class() \
            if institutions_class else institutions
        self.blank_label = kwargs.pop("blank_label", None)
        kwargs["choices"] = lambda: self.institutions
        super().__init__(*args, **kwargs)

    def get_internal_type(self):
        return "CharField"

    def contribute_to_class(self, cls, name):
        super().contribute_to_class(cls, name)
        setattr(cls, name, self.descriptor_class(self))

    def pre_save(self, *args, **kwargs):
        "Returns field's value just before saving."
        value = super(CharField, self).pre_save(*args, **kwargs)
        return self.get_prep_value(value)

    def get_prep_value(self, value):
        "Returns field's value prepared for saving into a database."
        value = self.get_clean_value(value)
        return super(CharField, self).get_prep_value(value)

    def get_clean_value(self, value):
        if value is None:
            return None
        return force_str(value)

    def deconstruct(self):
        """
        Remove choices from deconstructed field, as this is the country list
        and not user editable.

        Not including the ``blank_label`` property, as this isn't database
        related.
        """
        name, path, args, kwargs = super(CharField, self).deconstruct()
        kwargs.pop("choices", None)
        return name, path, args, kwargs

    def get_choices(
        self,
        include_blank=True,
        blank_choice=BLANK_CHOICE_DASH,
        limit_choices_to=None,
        ordering=(),
    ):
        if self.blank_label is None:
            blank_choice = BLANK_CHOICE_DASH
        else:
            blank_choice = [("", self.blank_label)]
        return super().get_choices(
            include_blank=include_blank,
            blank_choice=blank_choice,
            limit_choices_to=limit_choices_to,
            ordering=ordering,
        )

    def value_to_string(self, obj):
        """
        Ensure data is serialized correctly.
        """
        value = self.value_from_object(obj)
        return self.get_prep_value(value)

    def to_python(self, value):
        # Custom logic to convert the database value to a Python object
        if isinstance(value, str):
            return value
        return str(value)
