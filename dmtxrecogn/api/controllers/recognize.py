import json
import logging
import os
from logging import Logger
from bottle import Bottle, request
import tempfile
import shutil

from dmtxrecogn.recognizer.datamatrixRecognizer import DatamatrixRecognizer

logger: Logger = logging.getLogger(__name__)
recognize = Bottle()


@recognize.post()
def recognize(req, res):
    uploaded_files = request.files.getall('files')
    http_params = json.loads(request.forms.get('params'))
    temp_dir = tempfile.mkdtemp()

    for index, file in enumerate(uploaded_files):
        filename = file.filename
        file_path = os.path.join(temp_dir, f'file_{index + 1}_{filename}')
        file.save(file_path)
    recognizer = DatamatrixRecognizer()
    results = []

    for filename in os.listdir(temp_dir):
        result = recognizer.magick(os.path.join(temp_dir, filename), http_params)
        results.append(result)

    shutil.rmtree(temp_dir)

    res(200, [('Content-Type', 'application/json')])

    return json.dumps({"results": {"files": results}})
