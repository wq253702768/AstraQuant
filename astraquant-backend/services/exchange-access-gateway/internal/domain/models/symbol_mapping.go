package models

type SymbolMapping struct {
	InternalSymbol string `json:"internal_symbol"`
	Exchange       string `json:"exchange"`
	ExchangeSymbol string `json:"exchange_symbol"`
	InstrumentType string `json:"inst_type"`
	BaseCurrency   string `json:"base_currency"`
	QuoteCurrency  string `json:"quote_currency"`
	SettleCurrency string `json:"settle_currency"`
	Enabled        bool   `json:"enabled"`
}

type InstrumentSyncResult struct {
	Exchange     string `json:"exchange"`
	InstType     string `json:"inst_type"`
	Status       string `json:"status"`
	SuccessCount int    `json:"success_count"`
	FailedCount  int    `json:"failed_count"`
}
