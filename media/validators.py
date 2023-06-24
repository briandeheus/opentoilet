from django.core.exceptions import ValidationError
from django.template.defaultfilters import filesizeformat
from django.utils.deconstruct import deconstructible

from media.consts import MEDIA_ACCEPTED_IMAGE, MEDIA_MAX_SIZE_IMAGE
from media.methods import get_media_metadata


@deconstructible
class FileMediaValidator(object):
    error_messages = {
        "max_size": (
            "Ensure this file size is not greater than %(max_size)s."
            " Your file size is %(size)s."
        ),
        "min_size": (
            "Ensure this file size is not less than %(min_size)s. "
            "Your file size is %(size)s."
        ),
        "content_type": "Files of type %(content_type)s are not supported.",
    }

    def __init__(self, max_size=None, min_size=None, content_types=()):
        self.max_size = max_size
        self.min_size = min_size
        self.content_types = content_types

    def __call__(self, data):
        if self.content_types:
            content_type = get_media_metadata(data).content_type
            # This means that file is empty, so we return the original data
            if content_type == "application/x-empty":
                return data

            if content_type not in self.content_types:
                params = {"content_type": content_type}
                raise ValidationError(
                    self.error_messages["content_type"], "content_type", params
                )

            if content_type in MEDIA_ACCEPTED_IMAGE:
                self.max_size = MEDIA_MAX_SIZE_IMAGE

        if self.max_size is not None and data.size > self.max_size:
            params = {
                "max_size": filesizeformat(self.max_size),
                "size": filesizeformat(data.size),
            }
            raise ValidationError(self.error_messages["max_size"], "max_size", params)

        if self.min_size is not None and data.size < self.min_size:
            params = {
                "min_size": filesizeformat(self.min_size),
                "size": filesizeformat(data.size),
            }
            raise ValidationError(self.error_messages["min_size"], "min_size", params)

        return data

    def __eq__(self, other):
        return (
            isinstance(other, FileMediaValidator)
            and self.max_size == other.max_size
            and self.min_size == other.min_size
            and self.content_types == other.content_types
        )
