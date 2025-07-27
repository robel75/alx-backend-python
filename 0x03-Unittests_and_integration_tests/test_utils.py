#!/usr/bin/env python3
"""Test module for utils.py"""
import unittest
from unittest.mock import patch
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Tests for access_nested_map"""

    def test_access_nested_map(self):
        self.assertEqual(access_nested_map({"a": 1}, ["a"]), 1)
        self.assertEqual(access_nested_map({"a": {"b": 2}}, ["a"]), {"b": 2})
        self.assertEqual(access_nested_map({"a": {"b": 2}}, ["a", "b"]), 2)

    def test_access_nested_map_exception(self):
        with self.assertRaises(KeyError):
            access_nested_map({}, ["a"])
        with self.assertRaises(KeyError):
            access_nested_map({"a": 1}, ["a", "b"])


class TestGetJson(unittest.TestCase):
    """Tests for get_json"""

    @patch('utils.requests.get')
    def test_get_json(self, mock_get):
        test_url = "http://example.com"
        test_payload = {"payload": True}

        mock_get.return_value.json.return_value = test_payload
        result = get_json(test_url)
        mock_get.assert_called_once_with(test_url)
        self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Tests for memoize"""

    def test_memoize(self):
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        test = TestClass()
        with patch.object(test, 'a_method', return_value=42) as mock_method:
            self.assertEqual(test.a_property, 42)
            self.assertEqual(test.a_property, 42)
            mock_method.assert_called_once()
