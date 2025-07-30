import pytest
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_superuser():
    email = settings.DJANGO_SUPERUSER_EMAIL
    username = settings.DJANGO_SUPERUSER_USERNAME
    superuser = User.objects.get(
        email=email,
        username=username,
    )
    assert superuser is not None
    assert superuser.is_superuser is True
    assert superuser.email == email
    assert superuser.username == username
