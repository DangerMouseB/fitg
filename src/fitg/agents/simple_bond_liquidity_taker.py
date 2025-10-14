# **********************************************************************************************************************
# Copyright 2025-2026 David Briant, https://github.com/coppertop-bones. Licensed under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance with the License. You may obtain a copy of the  License at
# http://www.apache.org/licenses/LICENSE-2.0. Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY  KIND,
# either express or implied. See the License for the specific language governing permissions and limitations under the
# License. See the NOTICE file distributed with this work for additional information regarding copyright ownership.
# **********************************************************************************************************************

# Python imports

# vlmessaging imports
from vlmessaging import VLM, Msg, Entry
from vlmessaging.utils import co, Missing, wip, logging
from vlmessaging._utils import directory

# local imports
from fitg.agents._game_agent_base import GameAgent
from fitg.agents.bond_venue import BondVenue


_log = logging.getLogger(__name__)


class SimpleBondLiquidityTaker(GameAgent):
    ENTRY_TYPE = 'SimpleLiquidityTaker'

    __slots__ = ('addrByMarketMakerName', 'bondVenuesByName', 'futExchanges')

    def __init__(self, router, *, bondVenues, futExchanges, **kwargs):
        super().__init__(router, **kwargs)
        self.bondVenuesByName = {}
        for name in bondVenues:
            self.bondVenuesByName[name] = Missing
        self.futExchanges = futExchanges

    async def start(self, vnets=[]):
        await self.loginToGameMaster()
        await self.registerSelfWithDirectory(vnets, self.name)
        self.conn.scheduleFn(self.maybeInitiateRfq, after=500)
        self.running = True
        return self

    async def stop(self):
        await super().stop()
        self.running = False

    async def msgArrived(self, msg):
        if msg.subject == BondVenue.NEW_TRADES:
            print(f'got new trades: {msg.contents}')
            return

        return [VLM.HANDLE_DOES_NOT_UNDERSTAND]

    async def maybeInitiateRfq(self):
        print('maybeInitiateRfq')

        # try to find missing venues
        missingVenues = [name for name, addr in self.bondVenuesByName.items() if addr is Missing]
        if missingVenues:
            entries:list[Entry] = directory._findEntriesOfTypeOrExit(
                self.conn,
                BondVenue.ENTRY_TYPE,
                timeout=200,
                errMsg=Missing
            )
            for entry in entries:
                if (name:=entry.params['name']) in missingVenues:
                    _log.info(f'found venue {name} at {entry.addr}')
                    self.bondVenuesByName[name] = entry.addr
                    # register as liquidity taker

        # for each bondVenue
        # get bonds and prices
        # select random bond & size
        # get liquidity providers
        # send RFQ to venue with list of N providers (N is smaller the larger the size is)
        # wait for responses from providers within time limit
        # tell venue if done trade and note who traded with and for what size
        # preferred providers list are cheapest for size

        self.conn.scheduleFn(self.maybeInitiateRfq, after=500)


