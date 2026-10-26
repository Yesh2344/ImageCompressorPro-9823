"""
Unit tests for the compress_image utility.
Run with: pytest test_compress.py
"""

import os
from pathlib import Path
import pytest
from utils import compress_image

TEST_IMG_DIR = Path(__file__).parent / 'test_images'
TEST_IMG_DIR.mkdir(exist_ok=True)

# Create a small test image if it doesn't exist
TEST_IMG_PATH = TEST_IMG_DIR / 'sample.jpg'
if not TEST_IMG_PATH.is_file():
    from PIL import Image
    img = Image.new('RGB', (800, 600), color='red')
    img.save(TEST_IMG_PATH, 'JPEG', quality=95)

@pytest.fixture
def temp_output(tmp_path):
    return tmp_path / 'compressed.jpg'

def test_compress_success(temp_output):
    """Compress a valid JPEG and verify output exists."""
    compress_image(input_path=TEST_IMG_PATH, output_path=temp_output, quality=50)
    assert temp_output.is_file()
    # Verify that file size is reduced
    original_size = TEST_IMG_PATH.stat().st_size
    compressed_size = temp_output.stat().st_size
    assert compressed_size < original_size

def test_invalid_quality():
    """Quality out of bounds should raise ValueError."""
    with pytest.raises(ValueError):
        compress_image(TEST_IMG_PATH, 'out.jpg', quality=0)

def test_nonexistent_input():
    """Non‑existent input file should raise FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        compress_image('no_such_file.png', 'out.png')

def test_invalid_image_file(temp_output):
    """Corrupted image should raise RuntimeError."""
    corrupted_path = TEST_IMG_DIR / 'corrupt.png'
    corrupted_path.write_bytes(b'not an image')
    with pytest.raises(RuntimeError):
        compress_image(corrupted_path, temp_output)