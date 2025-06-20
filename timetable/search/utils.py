from collections.abc import Callable

from django.db.models import QuerySet
from rest_framework.views import APIView


def django_filter_warning(
    get_queryset_method: Callable[[APIView], QuerySet],
) -> Callable[[APIView], QuerySet]:
    """
    This decorator is used to fix a warning in django-filter.
    See: https://github.com/carltongibson/django-filter/issues/966
    """

    def get_queryset(self: APIView) -> QuerySet:
        if getattr(self, "swagger_fake_view", False):
            return QuerySet()
        return get_queryset_method(self)  # type: ignore[return-value]

    return get_queryset
