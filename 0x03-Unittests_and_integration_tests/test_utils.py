#!/usr/bin/env python3
import unittest
from parameterized import parameterized
from utils import access_nested_map
import requests
from unittest.mock import patch,Mock
from utils import get_json


class TestAccessNestedMap(unittest.TestCase):
    @parameterized.expand([
    ({"a": 1}, ("a",), 1),
    ({"a": {"b": 2}}, ("a",), {"b": 2}),
    ({"a":{"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected ):
        self.assertEqual(access_nested_map(nested_map, path), expected)
    @parameterized.expand([
    ({}, {"a",}, KeyError),
    ({"a": 1}, ("a", "b"), KeyError)
    ])
    def test_access_nested_map_exception(self, nested_map,path,expected_exception):
       with self.assertRaises(expected_exception):
        access_nested_map(nested_map, path)

class TestGetJson(unittest.TestCase):
   @patch('requests.get') #we replaced the original requests.get with a fake requests.get
   def test_get_json(self,mock_get): #we passed the fake requests.get in mock_get
      test_cases=[
         ("http://example.com", {"payload": True}),  #the payload:true is our mock response that appears when the link/url http://example.com is called
         ("http://holberton.io",{"payload": False})
         ]
      for test_url, test_payload in test_cases:
         mock_response = Mock() #created a mock response object called mock_response from the mock class
         mock_response.json.return_value = test_payload #this stores the test_payload values in mock_response in the form of dictionary(json)
         mock_get.return_value = mock_response #the new requests.get value returns the values in the mock_response, which are the json values we assigned above (payload:true)

         result = get_json(test_url)
         mock_get.assert_called_once_with(test_url) #counts if the mock_get is called exactly once(the mock_get records everything )
         
         mock_get.reset_mock()
      


if __name__ == "__main__":
    unittest.main()


  
    
  
