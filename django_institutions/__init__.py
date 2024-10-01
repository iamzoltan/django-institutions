from typing import List, Union, Optional
from dataclasses import dataclass
from json import load
from pkg_resources import resource_stream
from django.utils.translation import gettext_lazy as _


def load_institutions():
    return load(resource_stream(
        "django_institutions",
        "world_universities_and_domains.json"))


@dataclass
class InstitutionInfo:
    name: str = None
    domains: List[str] = None
    web_pages: List[str] = None
    country: str = None
    alpha_two_code: str = None
    state_province: Optional[str] = None


InstitutionName = Union[str, InstitutionInfo]


class Institutions:
    """
    An objext containing all the institutions from:

    https://github.com/Hipo/university-domains-list/blob/master/world_universities_and_domains.json

    Iterating this object will return the list of institution names.
    """

    _institutions: List[InstitutionName]
    _institution_names: List[str]

    @property
    def institutions(self) -> List[InstitutionInfo]:
        """
        Returns a list of all the institutions.

        TODO: allow modification of the list of institutions.
        TODO: convert data into a python file.
        TODO: maybe separate concerns of properties.
        """
        institutions = load_institutions()
        self._institutions = []
        for institution in institutions:
            self._institutions.append(InstitutionInfo(**institution))

        return self._institutions

    @property
    def institution_names(self) -> List[InstitutionName]:
        """
        Returns a list of all the institutions.

        TODO: allow modification of the list of institutions.
        TODO: convert data into a python file.
        TODO: maybe separate concerns of properties.
        """
        institutions = load_institutions()
        self._institution_names = []
        for institution in institutions:
            self._institution_names.append(
                (institution['name'], _(institution['name'])))

        return self._institution_names

    def __iter__(self):
        """
        Iterate through the list of institutions sorted by name.

        TODO: add other ways to sort, such as from a list of names first.
        """
        institutions = self.institution_names
        yield from sorted(institutions)

    def __bool__(self):
        return bool(self._institutions)


institutions = Institutions()
