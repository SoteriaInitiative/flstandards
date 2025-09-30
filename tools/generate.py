"""
Example driver to generate goAML XML using the installed package.

This mirrors the arguments of src.generate_goaml.main(), but imports and
invokes the library function directly instead of calling its CLI.

Usage example:
  python example/generate.py --banks 3 --transactions 1000 --days 90 \
    --scenario_probability '{"1":0.2,"2":0.1,"3":0.1}' \
    --bank_knowledge '{"1":true,"2":false,"3":false}'

Environment:
  - If uploading to GCS, set GCS_* and GCP_* env vars as in README.
  - Optionally set GOAML_SCHEMA_PATH to the XSD file location.
"""

from __future__ import annotations

import argparse
import json

from soteria.coredata import generate_goaml


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Generate synthetic goAML XML via package API")
    p.add_argument("--banks", type=int, default=4)
    p.add_argument("--transactions", type=int, default=1000)
    p.add_argument("--days", type=int, default=30)
    p.add_argument("--parties", type=int, default=100)
    p.add_argument("--multi_bank_prob", type=float, default=0.2)
    p.add_argument("--multi_bank_distribution", type=int, default=2)
    p.add_argument("--std_multiplier", type=float, default=2.0)
    p.add_argument("--max_splits", type=int, default=5)
    p.add_argument("--scenario_probability", type=str, default='{"1":0.2, "2":0.1, "3":0.0, "4":0.0}')
    p.add_argument("--bank_knowledge", type=str, default='{"1":true, "2":false, "3":false, "4":false}')
    return p


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    # Convert JSON strings to dicts to match generate_goaml.main() behavior
    args.scenario_probability = json.loads(args.scenario_probability)
    args.bank_knowledge = json.loads(args.bank_knowledge)
    args.default_scenario_prob = 0.1

    # Call the package API directly
    generate_goaml.generate_reports(args)


if __name__ == "__main__":
    main()
