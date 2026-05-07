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
  ticker(symbol: string) {
    return request.get<unknown, ExchangeTicker>(`/api/exchange-public/exchanges/${exchange}/ticker`, { params: { symbol } });
  },
  markPrice(symbol: string) {
    return request.get<unknown, MarkPrice>(`/api/exchange-public/exchanges/${exchange}/mark-price`, { params: { symbol } });
  },
  fundingRate(symbol: string) {
    return request.get<unknown, FundingRate>(`/api/exchange-public/exchanges/${exchange}/funding-rate`, { params: { symbol } });
  },
};
