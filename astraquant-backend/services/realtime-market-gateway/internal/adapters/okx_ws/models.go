package okx_ws

type SubscribeArg struct {
	Channel string `json:"channel"`
	InstID  string `json:"instId"`
}
type SubscribeMessage struct {
	Op   string         `json:"op"`
	Args []SubscribeArg `json:"args"`
}
type Message struct {
	Arg   SubscribeArg     `json:"arg"`
	Data  []map[string]any `json:"data"`
	Event string           `json:"event"`
	Code  string           `json:"code"`
	Msg   string           `json:"msg"`
}
