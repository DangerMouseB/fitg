# **********************************************************************************************************************
# Copyright 2025 David Briant, https://github.com/coppertop-bones. Licensed under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance with the License. You may obtain a copy of the  License at
# http://www.apache.org/licenses/LICENSE-2.0. Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY  KIND,
# either express or implied. See the License for the specific language governing permissions and limitations under the
# License. See the NOTICE file distributed with this work for additional information regarding copyright ownership.
# **********************************************************************************************************************

# starts up bond trading agents in a single process on a single machine for playing with

# Python imports
import os, csv, datetime, sys

# vlmessaging imports
from vlmessaging import Msg, Addr, Router, VLM, Directory, Entry
from vlmessaging.utils import co, wip, Missing, logging
from vlmessaging._utils.utils import Timer
from vlmessaging._utils.errors import NotYetImplemented


from fitg.agents.core import GameMaster, BondVenue, SimpleBondDealer, SimpleBondLiquidityTaker, Exchange
from fitg.core import structs

_log = logging.getLogger(__name__)

pswdByName = {
    'gamemaster' : 'fred',
}

dataFolder = os.path.join(os.path.dirname(__file__), '..', 'data')

bondFfn = os.path.join(dataFolder, 'bonds.csv')
with open(bondFfn, 'r') as f:
    bonds = [structs.BulletBond.csvLine(*line) for line in list(csv.reader(f))[1:]]

bontFutsFfn = os.path.join(dataFolder, 'bond_futs.csv')
with open(bontFutsFfn, 'r') as f:
    bondFuts = [structs.BondFut.csvLine(*line) for line in list(csv.reader(f))[1:]]

basketRulesFfn = os.path.join(dataFolder, 'basket_rules.csv')
with open(basketRulesFfn, 'r') as f:
    basketRules = [structs.BFBasketRule.csvLine(*line) for line in list(csv.reader(f))[1:]]

def run_rfq_play():

    async def _():
        r = Router(mode=VLM.LOCAL_MODE)
        d = Directory(r)

        unpswd = {'user':'gamemaster', 'pswd':'fred'}

        gm = await GameMaster(r, 'fitg', pswdByName).start()

        tweb = await BondVenue(r, name='TWEB', assets=bonds, **unpswd).start()
        eurex = await Exchange(r, name='EUREX', assets=bondFuts, **unpswd).start()

        venues = {'bondVenues':['TWEB'], 'futExchanges':['EUREX']}

        blackmanSucks = await SimpleBondDealer(r, name='Blackman Sucks', **(venues | unpswd)).start()
        squirrelLench = await SimpleBondDealer(r, name='Squirrel Lench', **(venues | unpswd)).start()
        sackJon = await SimpleBondDealer(r, name='Sack Jon', **(venues | unpswd)).start()
        cibc = await SimpleBondDealer(r, name='Coloring In Book Co', **(venues | unpswd)).start()

        assets = {
            'assetsOfInterest':[b for b in bonds if b.alias.startswith('DBR')] #and b.maturityDt > 5 and b.maturityDt < 12]
        }
        brownBlock = await SimpleBondLiquidityTaker(r, name='Brown Block', **(venues | assets | unpswd)).start()

        await co.until(r.hasShutdown)

    co.startEventLoopWith(_)


def main():
    run_rfq_play()
    'done' >> _log.info

if __name__ == '__main__':
    sink = logging.StreamSink(sys.stdout, formatter=logging.Formatter('%(message)s'))
    logging.getLogger('fitb') >> sink
    with logging.configure(levels={'fitb.*':logging.INFO}):
        main()
