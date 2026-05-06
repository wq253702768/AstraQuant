package models

type UnifiedInstrument struct {
	Exchange       string `json:"exchange"`
	InternalSymbol string `json:"internal_symbol"`
	ExchangeSymbol string `json:"exchange_symbol"`
	BaseAsset      string `json:"base_asset"`
	QuoteAsset     string `json:"quote_asset"`
	MarginAsset    string `json:"margin_asset"`
	ContractType   string `json:"contract_type"`
	TickSize       string `json:"tick_size"`
	LotSize        string `json:"lot_size"`
	MinSize        string `json:"min_size"`
	ContractValue  string `json:"contract_value"`
	PricePrecision int    `json:"price_precision"`
	SizePrecision  int    `json:"size_precision"`
	Status         string `json:"status"`
}

type GetInstrumentsRequest struct {
	ContractType string
	Symbol       string
}
