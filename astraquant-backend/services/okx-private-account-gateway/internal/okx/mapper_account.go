package okx

func MapAccount(data map[string]any) map[string]any {
	return map[string]any{"exchange": "OKX", "currency": data["ccy"], "total_equity": data["eq"], "available_equity": data["availEq"], "event_time": data["uTime"]}
}
