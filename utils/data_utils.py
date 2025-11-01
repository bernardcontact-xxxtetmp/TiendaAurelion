# utils/data_utils.py
"""
Small data utilities for safe CSV loading, validation and atomic JSON writes.
Add this module to centralize data-related safety checks used across scripts.
"""
from __future__ import annotations

import json
import logging
import os
import tempfile
from typing import Iterable, List, Optional

import pandas as pd

logger = logging.getLogger(__name__)


class DataLoadError(Exception):
    """Raised when a CSV cannot be loaded or validated."""


def load_csv_safe(path: str, encoding: str = "utf-8", low_memory: bool = False) -> pd.DataFrame:
    """
    Load a CSV file with common sanity checks.

    Raises:
      FileNotFoundError
      pd.errors.EmptyDataError
      pd.errors.ParserError
      UnicodeDecodeError
      PermissionError
      DataLoadError (for other unexpected errors)
    """
    if not os.path.exists(path):
        logger.debug("load_csv_safe: file not found: %s", path)
        raise FileNotFoundError(path)

    try:
        df = pd.read_csv(path, encoding=encoding, low_memory=low_memory)
        logger.debug("load_csv_safe: loaded %s rows, %s cols from %s", df.shape[0], df.shape[1], path)
        return df
    except pd.errors.EmptyDataError:
        logger.error("load_csv_safe: empty data file: %s", path)
        raise
    except pd.errors.ParserError:
        logger.error("load_csv_safe: parser error reading CSV: %s", path)
        raise
    except UnicodeDecodeError:
        logger.error("load_csv_safe: encoding error reading CSV: %s", path)
        raise
    except PermissionError:
        logger.error("load_csv_safe: permission denied for CSV: %s", path)
        raise
    except Exception as exc:
        logger.exception("load_csv_safe: unexpected error reading %s: %s", path, exc)
        raise DataLoadError(str(exc))


def ensure_columns(df: pd.DataFrame, required: Optional[Iterable[str]] = None) -> List[str]:
    """
    Ensure required columns are present in df.

    Returns the list of missing columns (empty if none). Caller may raise or handle as desired.
    """
    if required is None:
        return []
    missing = [c for c in required if c not in df.columns]
    if missing:
        logger.debug("ensure_columns: missing columns: %s", missing)
    return missing


def to_numeric_safe(df: pd.DataFrame, column: str, errors: str = "coerce") -> pd.Series:
    """
    Safely coerce a column to numeric, returning the coerced Series.
    Non-convertible values become NaN when errors='coerce'.
    """
    if column not in df.columns:
        logger.debug("to_numeric_safe: column not found: %s", column)
        raise KeyError(f"Column not found: {column}")
    return pd.to_numeric(df[column], errors=errors)


def write_json_atomic(obj, dest_path: str, ensure_ascii: bool = False, indent: int = 2) -> None:
    """
    Write JSON to a temporary file and replace the destination path atomically.
    """
    dest_dir = os.path.dirname(dest_path) or "."
    os.makedirs(dest_dir, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(prefix="tmp_json_", dir=dest_dir, text=True)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=ensure_ascii, indent=indent)
            f.flush()
        os.replace(tmp_path, dest_path)
        logger.debug("write_json_atomic: wrote JSON to %s", dest_path)
    except Exception:
        # Cleanup temp file on failure
        try:
            os.unlink(tmp_path)
        except Exception:
            pass
        logger.exception("write_json_atomic: failed to write JSON to %s", dest_path)
        raise