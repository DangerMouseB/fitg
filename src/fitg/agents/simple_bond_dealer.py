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

# local imports
from fitg.agents._game_agent_base import GameAgent

_log = logging.getLogger(__name__)


class SimpleBondDealer(GameAgent):
    ENTRY_TYPE = 'SimpleBondDealer'

    __slots__ = ('addrByMarketMakerName', 'addrByBondVenue', 'addrByFutExchange')

    def __init__(self, router, *, bondVenues, futExchanges, **kwargs):
        super().__init__(router, **kwargs)

    async def start(self, vnets=[]):
        # find the Tweb BondVenue via the directory
        # register as a dealer
        # find the Eurex Exchange via the directory
        # subscribe to bond futures quotes and trade feeds
        # find BookKeeper and register with it
        # every few minutes check risk and trade hedges as necessary
        await self.loginToGameMaster()
        await self.registerSelfWithDirectory(vnets, self.name)
        self.running = True
        f'SimpleBondDealer {self.name} started' >> _log.info
        return self

    async def stop(self):
        await super().stop()
        self._conn.unscheduleFn(self.ensureConnectedAndSendQuotes)
        self.running = False

    async def msgArrived(self, msg):

        await super().msgArrived(msg)

        if msg.subject == 'ADD_ONE_TO_CURRENT':
            current = Missing
            while not current:
                current = await self.conn.send(Msg(self.conn.addr, 'GET_CURRENT', Missing), 200)
            await self.conn.send(msg.reply(current.contents + 1))

        elif msg.subject == 'GET_CURRENT':
            await co.until(self.wait / 1000)
            self.wait -= 100
            await self.conn.send(msg.reply(41))

        else:
            return [VLM.IGNORE_UNHANDLED_REPLIES, VLM.HANDLE_DOES_NOT_UNDERSTAND]


    async def ensureConnectedAndSendQuotes(self):
        self._conn.scheduleFn(self.ensureConnectedAndSendQuotes, after=3000)

