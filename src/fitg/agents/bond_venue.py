# **********************************************************************************************************************
# Copyright 2025-2026 David Briant, https://github.com/coppertop-bones. Licensed under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance with the License. You may obtain a copy of the  License at
# http://www.apache.org/licenses/LICENSE-2.0. Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY  KIND,
# either express or implied. See the License for the specific language governing permissions and limitations under the
# License. See the NOTICE file distributed with this work for additional information regarding copyright ownership.
# **********************************************************************************************************************

# RFQ (Request For Quotation) overview
# TERMS: taker - the party requesting quotes
#        provider - the party providing quotes
#        asset - the bond being quoted
#        size - the quantity being quoted (+ve for buy, -ve for sell)
#        indicative price - a non-binding price provided by a provider to show current market levels, but the
#           expectation is that they are good for a minimum size, e.g. 10M
#        firm quote - a binding price provided by a provider in response to an RFQ
#        composite price - an aggregation of indicative prices from multiple providers
#
# PROCESS:
# 1) taker initiates an RFQ with the venue, stating which providers they want to show it to, the asset and size
# 2) each provider gives a firm quote for the requested asset and size within a time limit
# 3) takes either accepts the best quote or declines to trade
# 4) venue informs providers of the outcome - traded, near miss, no trade
#
# In fitg the two parties are responsible for registering the trade with the GameMaster / Bookkeeper
# Gamemaster acts as clearing house
#
# For the first implementation we will assume well coded agents that behave correctly
# No error handling for invalid messages, bad behaviour etc.
# Providers may only quote for RFQs they have provided indicative prices for



# Python imports
from typing import Annotated, TypeAlias, Iterable, cast

# vlmessaging imports
from vlmessaging import VLM, Msg, Entry
from vlmessaging.utils import co, Missing, wip

# local imports
from fitg.agents._game_agent_base import GameAgent

# types
AssetName = str
ProviderName = str
Bid = Ask = float
BidAsk: TypeAlias = Annotated[list[float], "BidAsk: [bid, ask]"]    # providers must provide a 2-way price so bid/ask are never None
Indication: TypeAlias = tuple[AssetName, Bid, Ask]
Indications: TypeAlias = Iterable[Indication]


RFQ_TIMEOUT_MS = 5000                   # time allowed for providers to respond with quotes
QUOTE_OBLIGATION_INTERVAL_MS = 10000    # interval within which providers must submit indicative prices


class Rfq:
    __slots__ = ['taker', 'takerId', 'venueId', 'asset', 'size', 'providers', 'startDT']



class BondVenue(GameAgent):
    ENTRY_TYPE = 'BondVenue'
    REGISTER_PROVIDER = 'REGISTER_PROVIDER'
    UNREGISTER_PROVIDER = 'UNREGISTER_PROVIDER'
    PROVIDER_JOINED = 'PROVIDER_JOINED'
    PROVIDER_LEFT = 'PROVIDER_LEFT'
    GET_PROVIDERS = 'GET_PROVIDERS'
    REGISTER_TAKER = 'REGISTER_TAKER'   # takers are more secretive so no join / left protocol
    UNREGISTER_TAKER = 'UNREGISTER_TAKER'
    SUBMIT_INDIC = 'SUBMIT_INDIC'       # providers must submit indicative prices regularly
    GET_COMPOSITES = 'GET_COMPOSITES'   # anyone can get current indicative prices
    RFQ_START = 'RFQ_START'             # taker initiates this
    RFQ_QUOTE_FOR = 'RFQ_QUOTE_FOR'     # ask provider for quote
    RFQ_QUOTES = 'RFQ_QUOTES'           # inform taker of levels
    RFQ_ACCEPT = 'RFQ_ACCEPT'           # taker trades with provider of best quote
    RFQ_DECLINE = 'RFQ_DECLINE'         # taker declines to trade
    RFQ_ACCEPTED = 'RFQ_ACCEPTED'       # inform provider they traded
    RFQ_NEAR_MISS = 'RFQ_NEAR_MISS'     # inform provider they were next best
    RFQ_NO_TRADE = 'RFQ_NO_TRADE'       # informs provider they didn't trade

    _baByProviderByAsset: dict[AssetName, dict[ProviderName, Indication]]
    _compositeByAsset: dict[AssetName, BidAsk]

    __slots__ = [
        'addrByProviderName',
        'addrByTakerName',
        'assets',
        '_baByProviderByAsset',         # bid / ask by provider by asset
        '_compositeByAsset',            # current composite indicative bid / ask (averaged across providers) by asset
    ]


    # LIFECYCLE

    def __init__(self, router, *, assets, **kwargs):
        super().__init__(router, **kwargs)
        self.addrByProviderName = {}
        self.addrByTakerName = {}
        self.assets = assets
        self._baByProviderByAsset = {}
        self._compositeByAsset = {}

    async def start(self, vnets=[]):
        await self.loginToGameMaster()
        await self.registerSelfWithDirectory(vnets, self.name)
        self.running = True
        return self

    async def stop(self):
        await super().stop()
        self.running = False


    # MESSAGE HANDLERS

    async def msgArrived(self, msg):

        await super().msgArrived(msg)

        # LIFETIME PROTOCOL

        if msg.subject == self.REGISTER_PROVIDER:
            providerName = msg.contents     # assume valid
            self.addrByProviderName[providerName] = msg.sender.addr
            await self.conn.send(msg.reply(True))                       # inform provider of successful registration
            for name, addr in self.addrByProviderName.items():
                if name != providerName:
                    await self.conn.send(Msg(addr, self.PROVIDER_JOINED, providerName))
            for name, addr in self.addrByTakerName.items():
                await self.conn.send(Msg(addr, self.PROVIDER_JOINED, providerName))

        elif msg.subject == self.UNREGISTER_PROVIDER:
            providerName = msg.contents     # assume valid
            if self.addrByProviderName.pop(providerName, None):
                await self.conn.send(msg.reply(None))                   # inform provider of successful unregistration
                for addr in self.addrByProviderName.values():
                    await self.conn.send(Msg(addr, self.PROVIDER_LEFT, providerName))
                for addr in self.addrByTakerName.values():
                    await self.conn.send(Msg(addr, self.PROVIDER_LEFT, providerName))

        elif msg.subject == self.GET_PROVIDERS:
            # OPEN: PROVIDERS_BY_ASSET instead
            await self.conn.send(msg.reply(list(self.addrByProviderName.keys())))

        elif msg.subject == self.REGISTER_TAKER:
            takerName = msg.contents
            self.addrByTakerName[takerName] = msg.sender.addr
            await self.conn.send(msg.reply(True))

        elif msg.subject == self.UNREGISTER_TAKER:
            takerName = msg.contents
            self.addrByTakerName.pop(takerName, None)
            await self.conn.send(msg.reply(None))


        # COMPOSITE PROTOCOL

        elif msg.subject == self.SUBMIT_INDIC:
            addr = msg.sender.addr
            providerName = next((n for n, a in self.addrByProviderName.items() if a == addr), None)  # OPEN: O(n) reverse lookup
            if not providerName: return    # don't inform unknown providers of failure

            changed = set()

            # update provider quotes
            for assetName, bid, ask in cast(Indications, msg.contents):
                baByProviderName = self._baByProviderByAsset.get(assetName)
                if baByProviderName is None:
                    baByProviderName = self._baByProviderByAsset[assetName] = {}
                baByProviderName[providerName] = [bid, ask]
                changed.add(assetName)

            # update composite quotes
            for assetName in changed:
                bidSum = askSum = 0.0
                n = 0
                for bid, ask in self._baByProviderByAsset.get(assetName, {}).values():
                    bidSum += bid
                    askSum += ask
                    n += 1
                if not n:
                    self._compositeByAsset.pop(assetName, None)
                else:
                    self._compositeByAsset[assetName] = [bidSum / n, askSum / n]

            await self.conn.send(msg.reply(True))

        elif msg.subject == self.GET_COMPOSITES:
            await self.conn.send(msg.reply(self._compositeByAsset))


        # RFQ PROTOCOL

        elif msg.subject == self.RFQ_START:
            # contents - [assets, quantities, side, providers]
            # create new rfq (with unique id) and send RFQ_QUOTE_FOR to each provider
            # reply to taker with rfq id
            return [VLM.HANDLE_DOES_NOT_UNDERSTAND]

        elif msg.subject == self.RFQ_QUOTE_FOR:
            if msg.isReply:
                # add the quote to the rfq
                pass
                return [VLM.HANDLE_DOES_NOT_UNDERSTAND]

        elif msg.subject == self.RFQ_ACCEPT:
            # check acceptance received within time limit
            # inform:
            #   best provider with RFQ_ACCEPTED,
            #   2nd best with RFQ_NEAR_MISS
            #   others with RFQ_NO_TRADE
            # taker and provider must inform GameMaster / Bookkeeper of trade
            # reply to taker that trade is done (provider, size, price, side)
            # if not within time limit send RFQ_NO_TRADE to taker
            return [VLM.HANDLE_DOES_NOT_UNDERSTAND]

        elif msg.subject == self.RFQ_DECLINE:
            # inform all providers with RFQ_NO_TRADE
            return [VLM.HANDLE_DOES_NOT_UNDERSTAND]


        # DEFAULT

        else:
            return [VLM.IGNORE_UNHANDLED_REPLIES, VLM.HANDLE_DOES_NOT_UNDERSTAND]


    # RFQ HELPERS

    async def sendQuotesToTaker(self):
        # RFQ_QUOTES
        pass


    async def quoteAcceptanceTimeout(self):
        # if rfq is not done within time limit, inform providers and taker that
        # RFQ_NO_TRADE
        pass

