import secrets

from django.contrib.auth import get_user_model

User = get_user_model()


def create_person_in_users_signals(instance, role):
    if instance.user:
        return instance.user

    full_name = f"{instance.last_name} {instance.first_name} {instance.patronymic}".strip()
    username = f"{instance.last_name.lower()}_{instance.first_name.lower()}"
    base_username = username
    i = 1
    while User.objects.filter(username=username).exists():
        username = f"{base_username}{i}"
        i += 1

    password = secrets.token_urlsafe(12)

    user = User.objects.create_user(
        username=username,
        password=password,
        name=full_name,
    )

    return user, password
