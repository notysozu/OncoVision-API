from typing import List
import numpy as np
from PIL import Image

from app.config import settings


def preprocess_images(images: List[Image.Image]) -> np.ndarray:
    """
    Preprocess a list of PIL Images for CNN inference.

    Steps:
    - Resize
    - Normalize
    - Convert to NumPy array
    - Stack into batch tensor
    """
    processed_images = []

    for image in images:
        processed = _preprocess_single_image(image)
        processed_images.append(processed)

    return np.stack(processed_images, axis=0)


def _preprocess_single_image(image: Image.Image) -> np.ndarray:
    """
    Preprocess a single image.
    """
    # Resize to model input size
    image = image.resize(settings.IMAGE_SIZE)

    # Convert to NumPy array
    image_array = np.array(image, dtype=np.float32)

    # Normalize pixel values to [0, 1]
    image_array /= 255.0

    return image_array
