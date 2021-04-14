# Copyright 2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
#     http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.
import json
import datetime
import sys
from dateutil.tz import tzlocal
from awscli.testutils import FileCreator, BaseCLIWireResponseTest
from awscli.clidriver import create_clidriver


class TestCLITimestampParser(BaseCLIWireResponseTest):
    def setUp(self):
        super(TestCLITimestampParser, self).setUp()
        # OpenVMS has an issue when time is near zero
        self.time_v = 60 * 60 * 24 if sys.platform == 'OpenVMS' else 0
        self.files = FileCreator()
        self.wire_response = json.dumps({
            'builds': [{
                'startTime': self.time_v,
            }]
        }).encode('utf-8')
        self.command = ['codebuild', 'batch-get-builds', '--ids', 'foo']
        self.patch_send(content=self.wire_response)

    def tearDown(self):
        super(TestCLITimestampParser, self).tearDown()
        self.files.remove_all()

    def test_iso(self):
        self.environ['AWS_CONFIG_FILE'] = self.files.create_file(
            'iso',
            '[default]\ncli_timestamp_format = iso8601\n')
        self.driver = create_clidriver()
        expected_time = datetime.datetime.fromtimestamp(self.time_v).replace(
            tzinfo=tzlocal()).isoformat()

        stdout, _, _ = self.run_cmd(self.command)
        json_response = json.loads(stdout)
        start_time = json_response["builds"][0]["startTime"]
        self.assertEqual(expected_time, start_time)

    def test_none(self):
        self.environ['AWS_CONFIG_FILE'] = self.files.create_file(
            'none',
            '[default]\ncli_timestamp_format = none\n')
        self.driver = create_clidriver()
        expected_time = self.time_v

        stdout, _, _ = self.run_cmd(self.command)
        json_response = json.loads(stdout)
        start_time = json_response["builds"][0]["startTime"]
        self.assertEqual(expected_time, start_time)

    def test_default(self):
        self.driver = create_clidriver()
        expected_time = self.time_v

        stdout, _, _ = self.run_cmd(self.command)
        json_response = json.loads(stdout)
        start_time = json_response["builds"][0]["startTime"]
        self.assertEqual(expected_time, start_time)
