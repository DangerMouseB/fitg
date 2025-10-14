# **********************************************************************************************************************
# Copyright 2025 David Briant, https://github.com/coppertop-bones. Licensed under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance with the License. You may obtain a copy of the  License at
# http://www.apache.org/licenses/LICENSE-2.0. Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY  KIND,
# either express or implied. See the License for the specific language governing permissions and limitations under the
# License. See the NOTICE file distributed with this work for additional information regarding copyright ownership.
# **********************************************************************************************************************

import collections, datetime

from fitg._utils.fmt import toCTimeFormat

ISO_FMT = toCTimeFormat('YYYY-MMM-D')


BulletBond = collections.namedtuple(
    'BulletBond',
    ('isin', 'alias', 'issueDt', 'datedDt', 'maturityDt', 'cpn', 'freqInMonths', 'outstanding', 'cls')
)
def csvLine(*xs):
    xs = list(xs)
    xs[2] = datetime.datetime.strptime(xs[2], ISO_FMT).date()
    xs[3] = datetime.datetime.strptime(xs[3], ISO_FMT).date()
    xs[4] = datetime.datetime.strptime(xs[4], ISO_FMT).date()
    xs[5] = float(xs[5])
    xs[6] = int(xs[6])
    xs[7] = int(xs[7].replace(',', ''))
    return BulletBond(*xs)
BulletBond.csvLine = csvLine


BondFut = collections.namedtuple(
    'BondFut',
    ('exchange', 'alias', 'bbgCode', 'firstTradingDt', 'firstDlvDt', 'lastDlvDt', 'cf')
)
def csvLine(*xs):
    xs = list(xs)
    xs[3] = datetime.datetime.strptime(xs[3], ISO_FMT).date()
    xs[4] = datetime.datetime.strptime(xs[4], ISO_FMT).date()
    xs[5] = datetime.datetime.strptime(xs[5], ISO_FMT).date()
    return BondFut(*xs)
BondFut.csvLine = csvLine


BFBasketRule = collections.namedtuple(
    'BondFut',
    (
        'asOf',         # date
        'bbgCode',
        'firstExpiry',
        'lastExpiry',
        'exchange',
        'country',
        'ccy',
        'exCode',
        'desc',
        'ticker',
        'refMat',
        'minMat',
        'maxMat',
        'maxMatIssue',
        'minAmt',       # float
        'size',         # float
        'cpn',          # float
    )
)
def csvLine(*xs):
    xs = list(xs)
    xs[0] = datetime.datetime.strptime(xs[0], ISO_FMT).date()
    xs[14] = float(xs[14])
    xs[14] = float(xs[15])
    xs[14] = float(xs[16])
    return BFBasketRule(*xs)
BFBasketRule.csvLine = csvLine
