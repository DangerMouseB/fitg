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
from vlmessaging.utils import co, Missing, wip

# local imports
from fitg.agents._game_agent_base import GameAgent



class SimpleBondLiquidityTaker(GameAgent):
    ENTRY_TYPE = 'SimpleLiquidityTaker'

    __slots__ = ('addrByMarketMakerName', 'bondVenues', 'futExchanges')

    def __init__(self, router, *, bondVenues, futExchanges, **kwargs):
        super().__init__(router, **kwargs)
        self.bondVenues = bondVenues
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
        return [VLM.HANDLE_DOES_NOT_UNDERSTAND]

    async def maybeInitiateRfq(self):
        print('maybeInitiateRfq')
        self.conn.scheduleFn(self.maybeInitiateRfq, after=500)


