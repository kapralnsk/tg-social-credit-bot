from mongoengine import ValidationError


def validate_starting_score(value):
    exception = ValidationError('Value must be positive int.')
    try:
        value = int(value)
    except ValueError:
        raise exception
    if value <= 0:
        raise exception