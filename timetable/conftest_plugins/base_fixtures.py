import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from config.celery_app import app as celery_app


@pytest.fixture(autouse=True)
def _media_storage(settings, tmpdir) -> None:
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def fake_image(faker) -> SimpleUploadedFile:
    return SimpleUploadedFile(
        name="test_image.jpg",
        content=faker.image(size=(100, 100)),
        content_type="image/jpeg",
    )


@pytest.fixture
def celery_always_eager():
    celery_app.conf.task_always_eager = True
    return celery_app
