import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from config.celery_app import app as celery_app
from timetable.search.documents.subject_doc import SubjectDocument
from timetable.search.documents.teacher_doc import TeacherDocument


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


@pytest.fixture
def clear_opensearch_indexes():
    # Полная очистка и пересоздание индекса
    TeacherDocument._index.delete(ignore=[404])  # noqa: SLF001
    SubjectDocument._index.delete(ignore=[404])  # noqa: SLF001

    TeacherDocument.init()
    SubjectDocument.init()
