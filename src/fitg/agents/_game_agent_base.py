# **********************************************************************************************************************
# Copyright 2025 David Briant, https://github.com/coppertop-bones. Licensed under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance with the License. You may obtain a copy of the  License at
# http://www.apache.org/licenses/LICENSE-2.0. Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY  KIND,
# either express or implied. See the License for the specific language governing permissions and limitations under the
# License. See the NOTICE file distributed with this work for additional information regarding copyright ownership.
# **********************************************************************************************************************

# Python imports
import logging

# vlmessaging imports
from vlmessaging import VLM, Msg, Entry, ExitMessageHandler, Connection
from vlmessaging.utils import co, Missing, wip

# local imports
from fitg.agents.game_master import GameMaster
from fitg.utils.exceptions import FitgError

_logger = logging.getLogger(__name__)


class GameAgent:
    ENTRY_TYPE: str
    GET_NAME = 'GET_NAME'

    conn: Connection
    name: str
    user: str
    pswd: str
    running: bool
    game_token: int

    __slots__ = ['conn', 'name', 'user', 'pswd', 'running', 'game_token']

    def __init__(self, router, name, user, pswd, *args, **kwargs):
        self.conn = router.newConnection(self.msgArrived)
        self.name = name
        self.user = user
        self.pswd = pswd
        self.running = False
        self.game_token = Missing

    async def stop(self):
        msg = Msg(self.conn.directoryAddr, VLM.UNREGISTER_ENTRY, Entry(self.conn.addr, self.ENTRY_TYPE, None, None, None))
        reply = await self.conn.send(msg, 500)
        if reply is Missing:
            _logger.warning(f'Failed to unregister {self.ENTRY_TYPE}({self.name})')

    async def loginToGameMaster(self):
        gmAddr = await wip._waitForSingleEntryAddrOfTypeOrReplyAndExit(
            self.conn,
            GameMaster.ENTRY_TYPE,
            5_000,
            200,
            errMsg=Missing
        )
        msg = Msg(gmAddr, GameMaster.LOGIN, (self.user, self.pswd))
        reply = await self.conn.send(msg, 2000, additional_subjects=[GameMaster.LOGIN_INVALID, GameMaster.LOGIN_TOKEN])
        if not reply or reply.subject == GameMaster.LOGIN_INVALID: raise FitgError('Login failed')
        self.game_token = reply.contents

    async def registerSelfWithDirectory(self, vnets, entryDetails):
        vnets = [vnets] if not isinstance(vnets, (list, tuple)) else vnets
        msg = Msg(self.conn.directoryAddr, VLM.REGISTER_ENTRY, Entry(self.conn.addr, self.ENTRY_TYPE, entryDetails, vnets, None))
        reply = await self.conn.send(msg, 500)
        if reply is Missing: raise Exception(f'Failed to register {self.ENTRY_TYPE}("{self.name}")')

    async def msgArrived(self, msg:Msg):
        if msg.subject == self.GET_NAME:
            reply = msg.reply(self.name)
            await self.conn.send(reply)
            raise ExitMessageHandler()

