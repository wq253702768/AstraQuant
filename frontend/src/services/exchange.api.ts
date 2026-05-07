import { request } from './request';
import type { ExchangeInstrument, ExchangeTicker, FundingRate, MarkPrice } from '@/types/exchange';

const exchange = 'OKX';

export const exchangeApi = {
  health() {
    return request.get<unknown, { status: string; service: string }>('/api/exchange-public/health');
  },
  time() {
    return request.get<unknown, { exchange: string; server_time: number }>(`/api/exchange-public/exchanges/${exchange}/time`);
  },
  instruments() {
    return request.get<unknown, { items: ExchangeInstrument[] }>(`/api/exchange-public/exchanges/${exchange}/instruments`, {
      params: { contract_type: 'swap' },
    });
  },
  syncInstruments() {
    return request.post<unknown, { exchange: string; inst_type: string; status: string; success_count: number; failed_count: number }>('/api/exchange-public/instruments/sync', {
      exchange,
      inst_type: 'SWAP',
    });
  },
  storedInstruments() {
    return request.get<unknown, { items: ExchangeInstrument[] }>('/api/exchange-public/instruments', {
      params: { exchange, inst_type: 'SWAP' },
    });
  },
  symbolMappings() {
    return request.get<unknown, { items: Array<{ internal_symbol: string; exchange: string; exchange_symbol: string; inst_type: string; enabled: boolean }> }>('/api/exchange-public/symbol-mappings', {
      params: { exchange },
    });
  },
  ticker(symbol: string) {
    return request.get<unknown, ExchangeTicker>(`/api/exchange-public/exchanges/${exchange}/ticker`, { params: { symbol } });
  },
  markPrice(symbol: string) {
    return request.get<unknown, MarkPrice>(`/api/exchange-public/exchanges/${exchange}/mark-price`, { params: { symbol } });
  },
  fundingRate(symbol: string) {
    return request.get<unknown, FundingRate>(`/api/exchange-public/exchanges/${exchange}/funding-rate`, { params: { symbol } });
  },
  klines(symbol: string, timeframe = '5m', limit = 5) {
    return request.get<unknown, { items: Array<Record<string, unknown>> }>(`/api/exchange-public/exchanges/${exchange}/klines`, {
      params: { symbol, timeframe, limit },
    });
  },
  fundingRateHistory(symbol: string, limit = 5) {
    return request.get<unknown, { items: FundingRate[] }>(`/api/exchange-public/exchanges/${exchange}/funding-rate-history`, {
      params: { symbol, limit },
    });
  },
};
