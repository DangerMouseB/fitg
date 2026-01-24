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
#        indicative price - a non-binding price provided by a provider to show current market levels, but expectation is
#           that they are good for a minimum size, e.g. on TWEB it was 10M
#        firm quote - a binding price provided by a provider in response to an RFQ
#        composite price - an aggregation of indicative prices from multiple providers
#
# PROCESS:
# 1) taker initiates an RFQ with the venue, stating which providers they's like to involve
# 2) each provider gives a firm quote for the requested asset and size within a time limit
# 3) takes either accepts the best quote or declines to trade
# 4) venue informs providers of the outcome - traded, near miss, no trade
#
# In fitg the two parties are responsible for registering the trade with the GameMaster / Bookkeeper
# Gamemaster acts as clearing house

# Python imports

# vlmessaging imports
from vlmessaging import VLM, Msg, Entry
from vlmessaging.utils import co, Missing, wip

# local imports
from fitg.agents._game_agent_base import GameAgent


class Rfq:
    __slots__ = ['taker', 'takerId', 'venueId', 'asset', 'size', 'providers', 'status']


class BondVenue(GameAgent):
    ENTRY_TYPE = 'BondVenue'
    REGISTER_PROVIDER = 'REGISTER_PROVIDER'
    UNREGISTER_PROVIDER = 'UNREGISTER_PROVIDER'
    PROVIDER_JOINED = 'PROVIDER_JOINED'
    PROVIDER_LEFT = 'PROVIDER_LEFT'
    GET_PROVIDERS = 'GET_PROVIDERS'
    REGISTER_TAKER = 'REGISTER_TAKER'   # takes are more secretive so no join / left protocol
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

    __slots__ = [
        'addrByProviderName', 'addrByTakerName', 'assets', '_baByProviderByAsset', '_compositeByAsset'
    ]

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


    async def msgArrived(self, msg):

        await super().msgArrived(msg)


        # PROVIDER PROTOCOL

        if msg.subject == self.REGISTER_PROVIDER:
            self.addrByProviderName[msg.contents] = msg.sender.addr
            # OPEN: inform other's that PROVIDER_JOINED

        elif msg.subject == self.UNREGISTER_PROVIDER:
            self.addrByProviderName.pop(msg.contents)
            # OPEN: inform other's that PROVIDER_LEFT

        elif msg.subject == self.GET_PROVIDERS:
            return [VLM.HANDLE_DOES_NOT_UNDERSTAND]


        # TAKER PROTOCOL
        elif msg.subject == self.REGISTER_TAKER:
            self.addrByTakerName[msg.contents] = msg.sender.addr

        elif msg.subject == self.UNREGISTER_TAKER:
            self.addrByTakerName.pop(msg.contents)


        # COMPOSITE PROTOCOL

        elif msg.subject == self.SUBMIT_INDIC:
            return [VLM.HANDLE_DOES_NOT_UNDERSTAND]

        elif msg.subject == self.GET_COMPOSITES:
            return [VLM.HANDLE_DOES_NOT_UNDERSTAND]


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



        # GENERIC HANDLERS

        return [VLM.IGNORE_UNHANDLED_REPLIES, VLM.HANDLE_DOES_NOT_UNDERSTAND]


    async def sendQuotesToTaker(self):
        # RFQ_QUOTES
        pass

    async def quoteAcceptanceTimeout(self):
        # if rfq is not done within time limit, inform providers and taker that
        # RFQ_NO_TRADE
        pass

