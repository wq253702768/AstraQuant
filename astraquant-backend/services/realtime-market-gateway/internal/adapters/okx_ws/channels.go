package okx_ws

func ToOKXSymbol(internal string) string   { return internal }
func FromOKXSymbol(exchange string) string { return exchange }
func TimeframeFromChannel(channel string) string {
	if channel == "candle5m" {
		return "5m"
	}
	if channel == "candle1m" {
		return "1m"
	}
	return ""
}
