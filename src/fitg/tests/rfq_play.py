# **********************************************************************************************************************
# Copyright 2025 David Briant, https://github.com/coppertop-bones. Licensed under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance with the License. You may obtain a copy of the  License at
# http://www.apache.org/licenses/LICENSE-2.0. Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY  KIND,
# either express or implied. See the License for the specific language governing permissions and limitations under the
# License. See the NOTICE file distributed with this work for additional information regarding copyright ownership.
# **********************************************************************************************************************


# starts up bond trading agents in a single process on a single machine for playing with


from fitg.agents import GameMaster, BondVenue, SimpleBondDealer, SimpleBondLiquidityTaker, Exchange
from fitg.assets import bonds, bond_futs

# vlmessaging imports
from vlmessaging import Msg, Addr, Router, VLM, Directory, Entry
from vlmessaging.utils import co, wip, Missing
from vlmessaging._utils.utils import Timer
from vlmessaging._utils.errors import NotYetImplemented

pswdByName = {
    'gamemaster' : 'fred',
}


def run_rfq_play():

    async def _():
        r = Router(mode=VLM.LOCAL_MODE)
        d = Directory(r)

        unpswd = {'user':'gamemaster', 'pswd':'fred'}

        gm = await GameMaster(r, 'fitg', pswdByName).start()

        tweb = await BondVenue(r, name='TWEB', assets=bonds, **unpswd).start()
        eurex = await Exchange(r, name='EUREX', assets=bond_futs, **unpswd).start()

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



if __name__ == '__main__':
    run_rfq_play()
    print('done')


