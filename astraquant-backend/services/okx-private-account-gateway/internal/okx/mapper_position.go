package okx

func MapPosition(data map[string]any) map[string]any {
	return map[string]any{"exchange": "OKX", "internal_symbol": data["instId"], "exchange_symbol": data["instId"], "position_side": data["posSide"], "quantity": data["pos"], "entry_price": data["avgPx"], "mark_price": data["markPx"], "leverage": data["lever"], "unrealized_pnl": data["upl"]}
}
