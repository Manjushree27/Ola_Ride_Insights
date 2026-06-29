"""Unit tests for python/helper_functions.py"""

import pandas as pd
import pytest

from python import helper_functions as hf


class TestNormalizeText:
    def test_none_input_returns_none(self):
        assert hf.normalize_text(None) is None

    def test_strips_surrounding_whitespace(self):
        assert hf.normalize_text("  Mumbai  ") == "Mumbai"

    def test_empty_string_returns_none(self):
        assert hf.normalize_text("") is None

    def test_whitespace_only_string_returns_none(self):
        assert hf.normalize_text("   ") is None

    def test_string_null_literal_returns_none_case_insensitive(self):
        assert hf.normalize_text("null") is None
        assert hf.normalize_text("NULL") is None
        assert hf.normalize_text("Null") is None

    def test_string_none_literal_returns_none(self):
        assert hf.normalize_text("none") is None
        assert hf.normalize_text("None") is None

    def test_string_nan_literal_returns_none(self):
        assert hf.normalize_text("nan") is None
        assert hf.normalize_text("NaN") is None

    def test_real_value_passes_through_unchanged(self):
        assert hf.normalize_text("Cash") == "Cash"

    def test_numeric_input_is_converted_to_string(self):
        assert hf.normalize_text(123) == "123"

    def test_pandas_nan_is_treated_as_null_literal(self):
        # float('nan') stringifies to "nan", which the lowercase check catches.
        assert hf.normalize_text(float("nan")) is None

    def test_value_with_internal_whitespace_is_preserved(self):
        assert hf.normalize_text("  RT Nagar  ") == "RT Nagar"


class TestEnsureOutputDirs:
    def test_creates_all_four_expected_directories(self, monkeypatch, tmp_path):
        monkeypatch.setattr(hf, "PROJECT_ROOT", tmp_path)
        hf.ensure_output_dirs()

        assert (tmp_path / "data" / "cleaned").is_dir()
        assert (tmp_path / "outputs" / "query_results").is_dir()
        assert (tmp_path / "outputs" / "reports").is_dir()
        assert (tmp_path / "outputs" / "screenshots").is_dir()

    def test_does_not_raise_if_directories_already_exist(self, monkeypatch, tmp_path):
        monkeypatch.setattr(hf, "PROJECT_ROOT", tmp_path)
        hf.ensure_output_dirs()
        # Calling it a second time should not raise (exist_ok=True).
        hf.ensure_output_dirs()
