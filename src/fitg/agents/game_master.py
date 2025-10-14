# **********************************************************************************************************************
# Copyright 2025 David Briant, https://github.com/coppertop-bones. Licensed under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance with the License. You may obtain a copy of the  License at
# http://www.apache.org/licenses/LICENSE-2.0. Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY  KIND,
# either express or implied. See the License for the specific language governing permissions and limitations under the
# License. See the NOTICE file distributed with this work for additional information regarding copyright ownership.
# **********************************************************************************************************************

# Python imports
import itertools

# vlmessaging imports
from vlmessaging import VLM, Msg, Entry
from vlmessaging.utils import co, Missing, wip



class GameMaster:
    ENTRY_TYPE = 'GAME_KEEPER'
    LOGIN = 'LOGIN'
    LOGIN_TOKEN = 'LOGIN_TOKEN'
    LOGIN_INVALID = 'LOGIN_INVALID'
    REGISTER_AGENT = 'REGISTER_AGENT'
    RECORD_TRADE = 'RECORD_TRADE'
    GET_RISK = 'GET_RISK'

    __slots__ = ('name', 'running', 'conn', 'playersAgentsByPlayer', 'pswdByPlayer', 'tokenByPlayer', 'tokenSeed')

    def __init__(self, router, name, pswdByPlayer):
        self.name = name
        self.running = False
        self.conn = router.newConnection(self.msgArrived)
        self.playersAgentsByPlayer = {}
        self.pswdByPlayer = pswdByPlayer
        self.tokenByPlayer = {}
        self.tokenSeed = itertools.count(1)

    async def start(self, vnets=[]):
        vnets = [vnets] if not isinstance(vnets, (list, tuple)) else vnets
        msg = Msg(self.conn.directoryAddr, VLM.REGISTER_ENTRY, Entry(self.conn.addr, self.ENTRY_TYPE, self.name, vnets, None))
        reply = await self.conn.send(msg, 500)
        if reply is Missing:
            raise Exception(f'Failed to register {self.ENTRY_TYPE} agent')
        self.running = True
        return self

    async def stop(self):
        msg = Msg(self.conn.directoryAddr, VLM.UNREGISTER_ENTRY, Entry(self.conn.addr, self.ENTRY_TYPE, None, None, None))
        reply = await self.conn.send(msg, 1000)
        if reply is Missing:
            print(f'Failed to unregister {self.ENTRY_TYPE} agent')
        self.running = False

    async def msgArrived(self, msg:Msg):

        if msg.subject == self.LOGIN:
            # answer a token for a player
            player, pswd = msg.contents
            if self.pswdByPlayer.get(player, Missing) == pswd:
                if (token := self.tokenByPlayer.get(player, Missing)) is Missing:
                    token = self.tokenByPlayer[player] = next(self.tokenSeed)
                reply = msg.reply(token, subject=self.LOGIN_TOKEN)
            else:
                reply = msg.reply(None, subject=self.LOGIN_INVALID)
            await self.conn.send(reply)

        elif msg.subject == self.REGISTER_AGENT:
            # note which player the agent belongs to
            return [VLM.HANDLE_DOES_NOT_UNDERSTAND]

        elif msg.subject == self.RECORD_TRADE:
            # note a trade between two agents
            return [VLM.HANDLE_DOES_NOT_UNDERSTAND]

        elif msg.subject == self.GET_RISK:
            # return risk (and other details) for an agent
            return [VLM.HANDLE_DOES_NOT_UNDERSTAND]

        else:
            return [VLM.IGNORE_UNHANDLED_REPLIES, VLM.HANDLE_DOES_NOT_UNDERSTAND]


