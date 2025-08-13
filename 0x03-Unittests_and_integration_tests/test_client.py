#!/usr/bin/env python3
import unittest 
import utils 
from parameterized import parameterized
from unittest.mock import PropertyMock, patch, Mock
from client import GithubOrgClient

class TestGithubOrgClient(unittest.TestCase):
    @parameterized.expand([ 
            ("google",),
            ("abc",)
        ])
    @patch('client.get_json') #get_json return data from a url but now it is patched to return a mock value 
    def test_org(self, org_name, mock_get_json): #org_name stored the parameterized.expand values and mock_get_json saves the mock value of get_json
        expected_payload = {'login': org_name} #stores the org_name in dictionary format
        mock_get_json.return_value = expected_payload #when the return value of mock_get_json is asked it returns expected_payload({'login':org_name})

        client = GithubOrgClient(org_name) #is an object created for the GithubOrgClient class in client.py and takes org_name as a parameter
        result = client.org #takes the org_name and passes it into the org function in client.py which displays org_name in json format 

        self.assertEqual(result, expected_payload)
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")


    def test_public_repos_url(self):
        expected_payload= {"repos_url":"https://api.github.com/orgs/orgname/repos"}
        client = GithubOrgClient("orgname")

        with patch.object(GithubOrgClient, 'org', new_callable=PropertyMock) as mock_org:
            mock_org.return_value = expected_payload
            result = client._public_repos_url
            self.assertEqual(result, expected_payload["repos_url"])


if __name__ == '__main__':
    unittest.main()        
        
        
            

        
