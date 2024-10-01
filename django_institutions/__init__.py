from typing import List, Union, Optional, Dict
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

    _institutions: List[InstitutionName] = None
    _institution_names: List[str] = None

    def __init__(self):
        self._load_institutions()

    def _load_institutions(self):
        institutions_data = load_institutions()
        self._institutions = {}
        for institution in institutions_data:
            inst_info = InstitutionInfo(**institution)
            self._institutions[institution['name']] = inst_info
        self._institution_names = None  # Initialize the institution names cache

    @property
    def institutions(self) -> Dict:
        """
        Returns a list of all the institutions.

        TODO: allow modification of the list of institutions.
        TODO: convert data into a python file.
        TODO: maybe separate concerns of properties.
        """
        if self._institutions is None:
            self._load_institutions()
        return self._institutions

    @property
    def institution_names(self) -> List[InstitutionName]:
        """
        Returns a list of all the institutions.

        TODO: allow modification of the list of institutions.
        TODO: convert data into a python file.
        TODO: maybe separate concerns of properties.
        """
        if self._institution_names is None:
            self._institution_names = [(name, _(name)) for name in self._institutions.keys()]
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
