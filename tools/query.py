"""
Example wrapper to run goAML queries using the installed package.

This forwards command line arguments to the package's query module so you can
use the commands documented in the README from the example folder.

Usage examples:
  python example/query.py senders
  python example/query.py receivers
  python example/query.py receivers-for "Alice Sender"
  python example/query.py transactions Bob Receiver 1980-02-02T00:00:00 --start-balance 10
  python example/query.py labels --local 1 --global 1
  python example/query.py multi-bank
  python example/query.py missing-ubos

Environment:
  - Set GCS and GCP env vars to allow the loader to connect to Cloud Storage,
    or set GOAML_CACHE_DIR to use local cached XML files.
"""

from __future__ import annotations

import sys
from typing import List

from soteria.coredata import goaml_query


def main(argv: List[str] | None = None) -> None:
    # Delegate to the package CLI for consistency with the README
    goaml_query.main(argv)


if __name__ == "__main__":
    main(sys.argv[1:])
