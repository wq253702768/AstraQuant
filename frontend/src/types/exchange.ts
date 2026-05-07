export interface ExchangeInstrument {
  exchange: string;
  internal_symbol: string;
  exchange_symbol: string;
  base_asset: string;
  quote_asset: string;
  margin_asset: string;
  contract_type: string;
  tick_size: string;
  lot_size: string;
  min_size: string;
  contract_value: string;
  status: string;
}

export interface ExchangeTicker {
  exchange: string;
  internal_symbol: string;
  last_price: string;
  best_bid_price: string;
  best_ask_price: string;
  high_24h: string;
  low_24h: string;
  volume_24h: string;
}

export interface MarkPrice {
  exchange: string;
  internal_symbol: string;
  mark_price: string;
  index_price: string;
  timestamp: number;
}

export interface FundingRate {
  exchange: string;
  internal_symbol: string;
  funding_rate: string;
  next_funding_time: number;
  mark_price?: string;
}
