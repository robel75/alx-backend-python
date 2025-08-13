#!/usr/bin/env python3
"""
Unit tests for utils.py functions:
- access_nested_map
- get_json
- memoize
"""

import unittest
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize
from unittest.mock import patch, Mock


class TestAccessNestedMap(unittest.TestCase):
    """Test cases for the access_nested_map function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        (
            {"a": {"b": 2}},
            ("a",),
            {"b": 2}
        ),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test access_nested_map returns expected value for
        given nested map and path."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), KeyError),
        ({"a": 1}, ("a", "b"), KeyError),
    ])
    def test_access_nested_map_exception(
            self, nested_map, path, expected_exception):
        """Test access_nested_map raises KeyError for invalid path."""
        with self.assertRaises(expected_exception):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """Test cases for the get_json function."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('utils.requests.get')
    def test_get_json(self, test_url, test_payload, mock_get):
        """Test get_json returns the expected
        payload from a mocked URL request."""
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        result = get_json(test_url)
        self.assertEqual(result, test_payload)
        mock_get.assert_called_once_with(test_url)


class TestMemoize(unittest.TestCase):
    """Test cases for the memoize decorator."""

    def test_memoize(self):
        """Test cases for the memoize decorator."""

        class TestClass:
            def a_method(self):
                """Return a constant value."""
                return 42

            @memoize
            def a_property(self):
                """Return the result of a_method, memoized as a property."""
                return self.a_method()

        test_object = TestClass()

        with patch.object(
            TestClass,
            'a_method',
            return_value=42
        ) as mock_method:
            result1 = test_object.a_property
            self.assertEqual(result1, 42)

            result2 = test_object.a_property
            self.assertEqual(result2, 42)

            mock_method.assert_called_once()


if __name__ == "__main__":
    unittest.main()

  
    
  
