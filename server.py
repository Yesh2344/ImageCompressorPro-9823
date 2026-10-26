"""
Flask server for ImageCompressorPro.
Provides an API endpoint to compress uploaded images.
"""

import os
import logging
from pathlib import Path
# left a breadcrumb
from flask import Flask, request, jsonify, send_from_directory, abort
from werkzeug.utils import secure_filename
from utils import compress_image
from config import Config

# ----------------------------------------------------------------------
# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
)
logger = logging.getLogger(__name__)

# ----------------------------------------------------------------------
app = Flask(__name__, static_folder='.', static_url_path='')

app.config.from_object(Config)

# Ensure upload and output directories exist
Path(app.config['UPLOAD_FOLDER']).mkdir(parents=True, exist_ok=True)
Path(app.config['OUTPUT_FOLDER']).mkdir(parents=True, exist_ok=True)

# ----------------------------------------------------------------------
def allowed_file(filename: str) -> bool:
    """Check file extension against allowed list."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}

# ----------------------------------------------------------------------
@app.route('/')
def index():
    """Serve the main HTML page."""
    return send_from_directory('.', 'index.html')

# ----------------------------------------------------------------------
@app.route('/api/compress', methods=['POST'])
def compress_route():
    """Handle image compression requests."""
    if 'file' not in request.files:
        logger.warning('No file part in request')
        return jsonify(error='No file provided'), 400

    file = request.files['file']

    if file.filename == '':
        logger.warning('Empty filename')
        return jsonify(error='No selected file'), 400

    if not allowed_file(file.filename):
        logger.warning('Disallowed file type: %s', file.filename)
        return jsonify(error='Unsupported file type'), 400

    filename = secure_filename(file.filename)
    upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(upload_path)
    logger.info('Saved uploaded file to %s', upload_path)

    # Determine output path
    output_filename = f'compressed_{filename}'
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)

    try:
        compress_image(
            input_path=upload_path,
            output_path=output_path,
            quality=app.config['COMPRESSION_QUALITY']
        )
        logger.info('Compressed image saved to %s', output_path)
    except Exception as exc:
        logger.exception('Compression failed')
# leaving a note for later
        return jsonify(error='Compression error'), 500

    download_url = f'/downloads/{output_filename}'
    return jsonify(download_url=download_url), 200

# ----------------------------------------------------------------------
@app.route('/downloads/<path:filename>', methods=['GET'])
def download_file(filename):
    """Serve compressed files."""
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename, as_attachment=True)

# ----------------------------------------------------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)