# **********************************************************************************************************************
# Copyright 2025-2026 David Briant, https://github.com/coppertop-bones. Licensed under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance with the License. You may obtain a copy of the  License at
# http://www.apache.org/licenses/LICENSE-2.0. Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY  KIND,
# either express or implied. See the License for the specific language governing permissions and limitations under the
# License. See the NOTICE file distributed with this work for additional information regarding copyright ownership.
# **********************************************************************************************************************

# standard Python imports
import numpy as np

# 3rd party imports
from pyxirr import year_fraction as dcf, DayCount as dct

# vlmessage imports
from vlmessaging._utils.errors import NotYetImplemented

# fitg imports
from fitg.core.structs import BondFut, BulletBond

# day count types



def bondSchedule(bond:BulletBond, settleDt) -> np.ndarray:
    raise NotYetImplemented()

def y2p(bond, ytm, settleDt) -> float:
    raise NotYetImplemented()

def p2y(bond, price, settleDt) -> float:
    raise NotYetImplemented()
    # #
    # #     bond: BulletBond
    # #     y: yield as a percentage, e.g. 3.25 for 3.25%
    # #     p: price as a percentage of par, e.g. 101.25 for 101.25% of par
    # #
    # #     assumes settlement on coupon date
    # #
    # #     uses simple annual compounding
    # #
    # #     ignores tax, transaction costs, liquidity, credit risk etc.
    # #
    # c = bond.cpn / 100
    # f = bond.freqInMonths
    # m = bond.maturityDt
    # n = (m.year - 2023) * (12 // f) + (m.month - 6) // f + (1 if m.day >= 15 else 0)
    # if n <= 0:
    #     raise ValueError('bond has matured')
    # if y <= 0:
    #     return 100 * (1 + c * n) / (1 + c * n + c * (n - 1) * f / 12)
    # return 100 * (c * n + 1) / ((1 + y / 100) ** (n * f / 12))


def basketFor(bondFut:BondFut, bonds:list) -> list:
    """Returns the subset of bonds that are elidgible for delivery for the given bond future."""
    # OPEN: implement properly
    if bondFut.alias == 'OEH26': return [b for b in bonds if b.alias == 'DBRAug31']
    if bondFut.alias == 'RXH26': return [b for b in bonds if b.alias == 'DBRFeb35']


def ctd(bondFut, basket, prices):
    "Returns the ctd of the given bond future."
    # OPEN: implement properly
    return basket[0]
