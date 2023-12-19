import os
import select
import sys
import json
import asyncio
from datamatrixRecognizer import DatamatrixRecognizer


async def main():
    paths = sys.argv[1]

    if os.name == 'nt':
        j_doc = json.load(sys.stdin)
    else:
        if select.select([sys.stdin], [], [], 0.0)[0]:
            j_doc = json.load(sys.stdin)
        else:
            raise Exception('Pipe is empty.')

    recognizer = DatamatrixRecognizer()

    tasks = [recognizer.magick(path, j_doc) for path in paths.split(",")]

    result = {"files": await asyncio.gather(*tasks)}

    return result


loop = asyncio.get_event_loop()
results = loop.run_until_complete(main())
loop.close()

print(json.dumps({"results": results}))
