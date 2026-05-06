package okx

func MapOrder(data map[string]any) map[string]any {
	return map[string]any{"exchange": "OKX", "internal_symbol": data["instId"], "exchange_order_id": data["ordId"], "client_order_id": data["clOrdId"], "side": data["side"], "order_state": data["state"], "price": data["px"], "avg_fill_price": data["avgPx"], "quantity": data["sz"], "filled_quantity": data["accFillSz"], "fee": data["fee"]}
}
