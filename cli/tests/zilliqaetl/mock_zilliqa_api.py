# MIT License
#
# Copyright (c) 2020 Evgeny Medvedev, evge.medvedev@gmail.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import decimal
import json


class MockZilliqaAPI:
    def __init__(self, read_resource):
        self.read_resource = read_resource

    def GetDsBlock(self, block_number):
        file_content = self.read_resource(build_file_name('GetDsBlock', block_number))
        return json.loads(file_content).get('result')

    def GetTxBlock(self, block_number):
        file_content = self.read_resource(build_file_name('GetTxBlock', block_number))
        return json.loads(file_content).get('result')

    def GetTxnBodiesForTxBlock(self, block_number):
        file_content = self.read_resource(build_file_name('GetTxnBodiesForTxBlock', block_number))
        return json.loads(file_content).get('result')


def build_file_name(method, *args):
    return 'response_{method}{args}.json'.format(method=method,
                                              args='_' + '_'.join([str(arg) for arg in args]) if len(args) > 0 else '')


def json_loads(s):
    return json.loads(s, parse_float=decimal.Decimal)
