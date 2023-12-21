import asyncio
import json
import warnings

from datamatrixRecognizer import DatamatrixRecognizer
warnings.filterwarnings("ignore", category=DeprecationWarning)


@asyncio.coroutine
def main(pdf_path, params):
    recognizer = DatamatrixRecognizer()
    return recognizer.magick(pdf_path, params)


loop = asyncio.get_event_loop()
results = loop.run_until_complete(main("images/23.jpg", {
    "type": "IDENTICAL",
    "segment": {"x": 1, "y": 6}
}))

print(json.dumps({"results": results}))

warnings.resetwarnings()
