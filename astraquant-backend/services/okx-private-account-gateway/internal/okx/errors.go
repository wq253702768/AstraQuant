package okx

func MapError(code string) string {
	if code == "50113" {
		return "OKX_AUTH_FAILED"
	}
	if code == "50110" {
		return "EXCHANGE_IP_NOT_ALLOWED"
	}
	return "OKX_PRIVATE_REST_FAILED"
}
