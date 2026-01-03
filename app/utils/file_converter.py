import os
from typing import List
from PIL import Image
from pdf2image import convert_from_path
from docx import Document

from app.config import settings


class UnsupportedFileTypeError(Exception):
    pass


class FileConversionError(Exception):
    pass


def get_file_extension(filename: str) -> str:
    """
    Safely extract file extension
    """
    return filename.split(".")[-1].lower()


def convert_file_to_images(file_path: str, filename: str) -> List[Image.Image]:
    """
    Convert an uploaded file into a list of PIL Images.
    """
    extension = get_file_extension(filename)

    if extension not in settings.ALLOWED_FILE_TYPES:
        raise UnsupportedFileTypeError(
            f"Unsupported file type: .{extension}"
        )

    if extension in settings.ALLOWED_IMAGE_TYPES:
        return _load_image(file_path)

    if extension == "pdf":
        return _convert_pdf(file_path)

    if extension == "docx":
        return _extract_docx_images(file_path)

    raise UnsupportedFileTypeError(
        f"File type .{extension} is not supported"
    )


def _load_image(file_path: str) -> List[Image.Image]:
    try:
        image = Image.open(file_path).convert("RGB")
        return [image]
    except Exception as e:
        raise FileConversionError(
            f"Failed to load image: {str(e)}"
        )


def _convert_pdf(file_path: str) -> List[Image.Image]:
    try:
        images = convert_from_path(file_path)
        if not images:
            raise FileConversionError("No pages found in PDF")
        return images
    except Exception as e:
        raise FileConversionError(
            f"Failed to convert PDF to images: {str(e)}"
        )


def _extract_docx_images(file_path: str) -> List[Image.Image]:
    try:
        document = Document(file_path)
        images: List[Image.Image] = []

        for rel in document.part._rels.values():
            if "image" in rel.target_ref:
                image_bytes = rel.target_part.blob
                image = Image.open(
                    io.BytesIO(image_bytes)
                ).convert("RGB")
                images.append(image)

        if not images:
            raise FileConversionError(
                "No images found in DOCX file"
            )

        return images

    except Exception as e:
        raise FileConversionError(
            f"Failed to extract images from DOCX: {str(e)}"
        )
