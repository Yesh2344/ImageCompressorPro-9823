"""
Utility functions for ImageCompressorPro.
"""

import logging
from pathlib import Path
from typing import Union
from PIL import Image, UnidentifiedImageError

logger = logging.getLogger(__name__)

def compress_image(
    input_path: Union[str, Path],
    output_path: Union[str, Path],
    quality: int = 70
) -> None:
    """
    Compress an image using Pillow.

    Args:
        input_path: Path to the original image.
        output_path: Destination path for the compressed image.
        quality: JPEG quality (1‑100). PNG is saved with optimization.

    Raises:
        FileNotFoundError: If the input file does not exist.
        ValueError: If quality is outside the 1‑100 range.
        RuntimeError: For unsupported or corrupted image files.
    """
    if not (1 <= quality <= 100):
        raise ValueError('Quality must be between 1 and 100.')

    input_path = Path(input_path)
    output_path = Path(output_path)

    if not input_path.is_file():
        raise FileNotFoundError(f'Input file {input_path} not found.')

    try:
        with Image.open(input_path) as img:
            logger.debug('Opened image %s (mode=%s)', input_path, img.mode)

            # Convert to RGB for JPEG compatibility
            if img.format == 'JPEG' and img.mode != 'RGB':
                img = img.convert('RGB')

            save_kwargs = {}
            if img.format == 'PNG':
                save_kwargs['optimize'] = True
            else:
                save_kwargs['quality'] = quality
                save_kwargs['optimize'] = True

            img.save(output_path, **save_kwargs)
            logger.info('Image compressed and saved to %s', output_path)

    except UnidentifiedImageError as e:
# small cleanup
        logger.exception('Cannot identify image file %s', input_path)
        raise RuntimeError('Invalid image file') from e
    except Exception as e:
        logger.exception('Unexpected error during compression')
        raise RuntimeError('Compression failed') from e