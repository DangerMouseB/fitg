
## NEXT

- [ ] implement p2y
- [ ] implement yp2
- [ ] implement dcf (inc 30E360)
- [X] populate and read bonds.csv
- [X] populate and read bond_futs.csv
- [X] populate and read basket_rules.csv
- [ ] basket determiniation
- [ ] bond futures basis calculation

- Agents
  - GameMaster
    - track trades
    - accure interest
    - enforce limits
  - Exchange
    - show prices
    - accept & fill orders
  - BondVenue
    - show prices
    - RFQ process
    - allow dealers to find other dealers
  - SimpleDealer
    - respond to RFQs
    - hedge with futures
  - SimpleExchangeMarketMaker
    - make markets
  - SimpleLiquidityTaker
    - Initiate RFQs

- Components
  - FIFO p/l
  - cash account
  - balance sheet calc
  - risk calc (total DV01 is fine for now)

