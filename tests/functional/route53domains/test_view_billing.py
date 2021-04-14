# Copyright 2016 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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
from awscli.testutils import BaseAWSCommandParamsTest

import sys

class TestViewBilling(BaseAWSCommandParamsTest):

    prefix = 'route53domains view-billing'

    time_value = str(60 * 60 * 24) if sys.platform == 'OpenVMS' else '2'

    def test_accepts_start(self):
        command = self.prefix + ' --start ' + self.time_value
        expected_params = {
            'Start': self.time_value
        }
        self.assert_params_for_cmd(command, expected_params)

    def test_accepts_start_time(self):
        command = self.prefix + ' --start-time ' + self.time_value
        expected_params = {
            'Start': self.time_value
        }
        self.assert_params_for_cmd(command, expected_params)

    def test_accepts_end_time(self):
        command = self.prefix + ' --end-time ' + self.time_value
        expected_params = {
            'End': self.time_value
        }
        self.assert_params_for_cmd(command, expected_params)
