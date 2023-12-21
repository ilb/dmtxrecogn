import os
import sys
import json
from datamatrixRecognizer import DatamatrixRecognizer
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)


def read_stdin():
    if os.name == 'nt':
        return json.load(sys.stdin)
    else:
        return json.loads(sys.stdin.read())


def sync_main():
    paths = sys.argv[1]
    j_doc = read_stdin()

    recognizer = DatamatrixRecognizer()
    results = []
    for path in paths.split(","):
        result = recognizer.magick(path, j_doc)
        results.append(result)

    return {"files": results}


results = sync_main()
print(json.dumps({"results": results}))

warnings.resetwarnings()
