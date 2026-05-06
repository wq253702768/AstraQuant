package okx_ws

import "encoding/json"

func BuildSubscribe(channel string, symbol string) ([]byte, error) {
	return json.Marshal(SubscribeMessage{Op: "subscribe", Args: []SubscribeArg{{Channel: channel, InstID: ToOKXSymbol(symbol)}}})
}
func BuildUnsubscribe(channel string, symbol string) ([]byte, error) {
	return json.Marshal(SubscribeMessage{Op: "unsubscribe", Args: []SubscribeArg{{Channel: channel, InstID: ToOKXSymbol(symbol)}}})
}
