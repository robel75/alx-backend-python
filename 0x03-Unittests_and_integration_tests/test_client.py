#!/usr/bin/env python3
import unittest
import utils
from parameterized import parameterized
from unittest.mock import PropertyMock, patch, Mock
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """This tests that GithubOrgClient.org returns the correct value."""
    @parameterized.expand([
            ("google",),
            ("abc",)
        ])
    @patch('client.get_json')  #get_json return data from a url but
    #now it is patched to return a mock value
    def test_org(self, org_name, mock_get_json):  #org_name stored the parameterized.expand values 
        #and mock_get_json saves the mock value of get_json
        expected_payload = {'login': org_name}  #stores the org_name in
        #dictionary format
        mock_get_json.return_value = expected_payload  #when the return value of mock_get_json 
        #is asked it returns expected_payload({'login':org_name})

        client=GithubOrgClient(org_name)  #is an object created for the GithubOrgClient
        #class in client.py and takes org_name as a parameter
        result=client.org  #takes the org_name and passes it into the org function in 
        #client.py which displays org_name in json format

        self.assertEqual(result, expected_payload)
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")


    def test_public_repos_url(self):
        """Test that _public_repos_url returns 
        the correct value from the org payload"""
        with patch(
            'client.GithubOrgClient.org',
            new_callable=PropertyMock,
            return_value={"repos_url": "https://api.github.com/orgs/orgname/repos"}
        )as mock_org:
            client = GithubOrgClient("orgname")
            result = client._public_repos_url
            self.assertEqual(result, "https://api.github.com/orgs/orgname/repos")
            mock_org.assert_called_once()


    @patch("client.get_json")  
    def test_public_repos(self, mock_get_json):
        """This tests that the list of repos is what you expect from the chosen payload."""
        test_public_repos=[
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
            {"name": "repo3", "license": None},
        ]
        mock_get_json.return_value=test_public_repos

        with patch.object(GithubOrgClient, '_public_repos_url', new_callable = PropertyMock) as mock_url:
            mock_url.return_value= "https://api.github.com/orgs/torr/repos"

            client = GithubOrgClient("torr")
            result = client.public_repos()
            
            expected = ["repo1", "repo2", "repo3"]
            self.assertEqual(result, expected)
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with("https://api.github.com/orgs/torr/repos")

              
if __name__ == '__main__':
    unittest.main()        
