# django-institutions
A Django application that provides a university institution field for models and a serializer.

## Installation
- `pip install django-institutions`
- Add `django_institutions` to your `INSTALLED_APPS`


## Usage
### InstitutionField
An institution field for Django models with choices from:
`https://github.com/Hipo/university-domains-list`

`InstitutionField` is based on Django's `CharField`.

Consider the following model user `InstitutionField`:
```python
from django.db import models
from django_institutions.fields import InstitutionField

class User(models.Model):
    name = models.CharField(max_length=255)
    institution = InstitutionField()
```

A `User` instance will have a `institution` attribute where you can get the details of the institution.
```python
>>> user = User(name='John Doe', institution='University of London')
>>> user.institution
Institution(name='University of London', country='United Kingdom', etc)
>>> user.institution.name
'University of London'
>>> user.institution.country
'United Kingdom'
```

### Django Rest Framework field
To serialize the `institution` field, you can use the `InstitutionField` serializer field. For example:

```python
from django_institutions.serializer_fields import InstitutionField

class UserSerializer(serializers.ModelSerializer):
    institution = InstitutionField()
```
#### REST output format
The serialized output will look like the following:
```python
{"name": "University of London"}
```

Either the dict output or simply the name of the institution is acceptable as intputs.

## Acknowledgements
This project is inspired by [django-countries](https://github.com/SmileyChris/django-countries)

Thanks to [SmileyChris](https://github.com/SmileyChris) for the inspiration.

## Data
The institution data is sourced from [university-domains-list](https://github.com/Hipo/university-domains-list)

## Notes
This project is still very in early development. Help is welcome :)
