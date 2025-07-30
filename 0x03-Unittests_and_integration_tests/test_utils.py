#!/usr/bin/env python3
"""Unit tests for utils.py."""

import unittest
from unittest.mock import patch
from utils import access_nested_map, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Test the access_nested_map function."""

    def test_access_nested_map(self):
        """Test with normal inputs."""
        self.assertEqual(access_nested_map({"a": 1}, ("a",)), 1)
        self.assertEqual(access_nested_map({"a": {"b": 2}}, ("a",)), {"b": 2})
        self.assertEqual(access_nested_map({"a": {"b": 2}}, ("a", "b")), 2)

    def test_access_nested_map_exception(self):
        """Test that KeyError is raised for missing keys."""
        with self.assertRaises(KeyError):
            access_nested_map({}, ("a",))
        with self.assertRaises(KeyError):
            access_nested_map({"a": 1}, ("a", "b"))


class TestMemoize(unittest.TestCase):
    """Tests for the memoize decorator."""

    def test_memoize(self):
        """Test that memoize caches the result of a method."""
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, 'a_method', return_value=42) as mocked:
            obj = TestClass()
            self.assertEqual(obj.a_property(), 42)
            self.assertEqual(obj.a_property(), 42)
            mocked.assert_called_once()


if __name__ == __'main'__:
    unittest.main()
