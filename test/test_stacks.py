import sys
import unittest

import cloudfoundry_client.main as main
from abstract_test_case import AbstractTestCase
from cloudfoundry_client.imported import OK, reduce
from fake_requests import mock_response
from imported import CREATED, patch


class TestBuildpacks(unittest.TestCase, AbstractTestCase):
    @classmethod
    def setUpClass(cls):
        cls.mock_client_class()

    def setUp(self):
        self.build_client()

    def test_list(self):
        self.client.get.return_value = mock_response('/v2/stacks',
                                                     OK,
                                                     None,
                                                     'v2', 'stacks', 'GET_response.json')
        cpt = reduce(lambda increment, _: increment + 1, self.client.stacks.list(), 0)
        self.client.get.assert_called_with(self.client.get.return_value.url)
        self.assertEqual(cpt, 1)

    def test_get(self):
        self.client.get.return_value = mock_response(
            '/v2/stacks/stack_id',
            OK,
            None,
            'v2', 'stacks', 'GET_{id}_response.json')
        result = self.client.stacks.get('stack_id')
        self.client.get.assert_called_with(self.client.get.return_value.url)
        self.assertIsNotNone(result)

    @patch.object(sys, 'argv', ['main', 'list_stacks'])
    def test_main_list_stacks(self):
        with patch('cloudfoundry_client.main.build_client_from_configuration',
                        new=lambda: self.client):
            self.client.get.return_value = mock_response('/v2/stacks',
                                                         OK,
                                                         None,
                                                         'v2', 'stacks', 'GET_response.json')
            main.main()
            self.client.get.assert_called_with(self.client.get.return_value.url)

    @patch.object(sys, 'argv', ['main', 'get_stack', '6e72c33b-dff0-4020-8603-bcd8a4eb05e4'])
    def test_main_get_stack(self):
        with patch('cloudfoundry_client.main.build_client_from_configuration',
                        new=lambda: self.client):
            self.client.get.return_value = mock_response('/v2/stacks/6e72c33b-dff0-4020-8603-bcd8a4eb05e4',
                                                         OK,
                                                         None,
                                                         'v2', 'stacks', 'GET_{id}_response.json')
            main.main()
            self.client.get.assert_called_with(self.client.get.return_value.url)
