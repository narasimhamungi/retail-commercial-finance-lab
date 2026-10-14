"""Command line: python -m rcfl {extract|excel|charts|report|all}."""

from __future__ import annotations

import sys
import warnings

from . import charts, excel_export, extract, report


def main(argv: list[str] | None = None) -> int:
    warnings.filterwarnings("ignore", message="Workbook contains no default style")
    steps = (argv or sys.argv[1:]) or ["all"]
    for step in steps:
        if step in ("extract", "all"):
            extract.run()
            print("extract: ledger verified against the raw PDFs; data/processed/ written")
        if step in ("excel", "all"):
            excel_export.run()
            print("excel: outputs/store_model.xlsx, outputs/bridge.xlsx")
        if step in ("charts", "all"):
            charts.run()
            print("charts: outputs/charts/")
        if step in ("report", "all"):
            report.run()
            print("report: docs/*.md, outputs/*.csv, outputs/performance_review.pdf")
        if step not in ("extract", "excel", "charts", "report", "all"):
            print(f"unknown step: {step}", file=sys.stderr)
            return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
