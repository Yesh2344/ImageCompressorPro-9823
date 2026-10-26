// script.js – Front‑end logic
const fileInput = document.getElementById('fileInput');
const dropZone = document.querySelector('.drop-zone');
const previewImg = document.getElementById('preview');
const compressBtn = document.getElementById('compressBtn');
const statusMessage = document.getElementById('statusMessage');

let selectedFile = null;

// Helper: display status
function setStatus(message, isError = true) {
    statusMessage.textContent = message;
    statusMessage.className = isError ? 'status' : 'status success';
}

// Drag & drop handling
['dragenter', 'dragover'].forEach(evt => {
    dropZone.addEventListener(evt, e => {
        e.preventDefault();
        e.stopPropagation();
        dropZone.classList.add('dragover');
    });
});
['dragleave', 'drop'].forEach(evt => {
    dropZone.addEventListener(evt, e => {
        e.preventDefault();
        e.stopPropagation();
        dropZone.classList.remove('dragover');
    });
});
dropZone.addEventListener('drop', e => {
    const files = e.dataTransfer.files;
    handleFileSelection(files[0]);
});

// Click to open file picker
dropZone.addEventListener('click', () => fileInput.click());

// File input change
fileInput.addEventListener('change', e => {
    if (e.target.files.length) {
        handleFileSelection(e.target.files[0]);
    }
});

// Process selected file
function handleFileSelection(file) {
    if (!file.type.startsWith('image/')) {
        setStatus('Please select a valid image file.');
        return;
    }
    if (file.size > 5 * 1024 * 1024) {
        setStatus('File exceeds 5 MiB size limit.');
        return;
    }
    selectedFile = file;
    const reader = new FileReader();
    reader.onload = e => {
        previewImg.src = e.target.result;
        previewImg.hidden = false;
    };
    reader.readAsDataURL(file);
    compressBtn.disabled = false;
    setStatus('');
}

// Compress button click
compressBtn.addEventListener('click', async () => {
    if (!selectedFile) return;
    compressBtn.disabled = true;
    setStatus('Compressing…');

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
        const response = await fetch('/api/compress', {
            method: 'POST',
            body: formData
        });
        const result = await response.json();
        if (response.ok) {
            setStatus('Compression successful!', false);
            const link = document.createElement('a');
            link.href = result.download_url;
            link.download = result.download_url.split('/').pop();
            link.textContent = 'Download Compressed Image';
            link.className = 'download-link';
            statusMessage.appendChild(document.createElement('br'));
            statusMessage.appendChild(link);
        } else {
            setStatus(result.error || 'Compression failed.');
        }
    } catch (err) {
        console.error(err);
        setStatus('Network error – try again later.');
    } finally {
        compressBtn.disabled = false;
    }
});