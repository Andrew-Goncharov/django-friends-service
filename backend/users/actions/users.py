from uuid import UUID

from rest_framework.exceptions import ValidationError

from ..models import User


def user_exists(id: UUID) -> bool:
    return User.objects.filter(id=id).exists()


def get_user_by_id(id: UUID) -> User:
    return User.objects.filter(id=id).first()


def is_valid_uuid(value) -> bool:
    try:
        UUID(str(value))
        return True
    except ValidationError:
        return False