import logging
import uuid
from collections import namedtuple
from io import BytesIO
from pathlib import Path

import filetype
import magic
from django.core.files import File
from django.core.files.images import get_image_dimensions
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image

from media import models
from media.consts import (
    MEDIA_ACCEPTED_IMAGE,
    MEDIA_METADATA_EXTENSION,
    MEDIA_METADATA_HEIGHT,
    MEDIA_METADATA_WIDTH,
    MEDIA_TYPE_IMAGE,
)

MediaMetadata = namedtuple(
    "MediaMetadata",
    [
        "size",
        "file_type",
        "content_type",
        "file_extension",
        "dimension_width",
        "dimension_height",
    ],
)

log = logging.getLogger(__name__)


def get_media_metadata(media: File, read_dimensions=False) -> MediaMetadata:
    # Make sure we start from the beginning
    media.seek(0)

    size = media.size

    # Sometimes magic fails to determine the mime correctly, and vice versa
    content_type = filetype.guess_mime(media.read(4096))
    if not content_type:
        content_type = magic.from_buffer(media.read(4096), mime=True)

    media.seek(0)

    # Determine file type by its mime
    if content_type in MEDIA_ACCEPTED_IMAGE:
        file_type = MEDIA_TYPE_IMAGE
    else:
        file_type = None

    # Get file extension
    file_extension = Path(media.name).suffix

    # Get dimensions
    dimension_width = None
    dimension_height = None
    if read_dimensions:
        if file_type == MEDIA_TYPE_IMAGE:
            dimension_width, dimension_height = get_image_dimensions(media)

    return MediaMetadata(
        size,
        file_type,
        content_type,
        file_extension,
        dimension_width,
        dimension_height,
    )


def handle_media(media_file, thumbnail=None):
    metadata = get_media_metadata(media=media_file, read_dimensions=True)
    original_filename = media_file.name

    media = models.Media.objects.create(
        file=media_file,
        file_name=original_filename,
        file_size=metadata.size,
        file_type=metadata.file_type,
        thumbnail=thumbnail,
    )

    media.set_metadata(MEDIA_METADATA_WIDTH, metadata.dimension_width)
    media.set_metadata(MEDIA_METADATA_HEIGHT, metadata.dimension_height)
    media.set_metadata(MEDIA_METADATA_EXTENSION, metadata.file_extension)
    media.save()

    # Video thumbnail can only be generated with URL / file, meanwhile request is stream
    if not thumbnail:
        pass

    return media


def resize_image(image, max_size):
    # Open the image and get its dimensions
    with Image.open(image) as img:
        width, height = img.size

        # Skip if size less than max
        if width < max_size and height < max_size:
            return img

        # Calculate the aspect ratio
        aspect_ratio = width / height

        # Determine the new dimensions based on the max size and aspect ratio
        if width > height:
            new_width = max_size
            new_height = int(max_size / aspect_ratio)
        else:
            new_width = int(max_size * aspect_ratio)
            new_height = max_size

        # Resize the image using the new dimensions
        img = img.resize((new_width, new_height))
        img = img.convert("RGB")
        return img


def resize_image_upload(value: InMemoryUploadedFile, max_size: int):
    img_file = BytesIO()
    img = resize_image(value, max_size)
    img.save(img_file, format="JPEG")

    file_size = img_file.tell()
    img_file.seek(0)

    return InMemoryUploadedFile(
        img_file,
        field_name="ImageField",
        name=f"{uuid.uuid4()}.jpg",
        content_type="image/jpeg",
        size=file_size,
        charset=None,
    )
