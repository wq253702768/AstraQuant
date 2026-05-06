package models

const (
	StateDisconnected = "DISCONNECTED"
	StateConnecting   = "CONNECTING"
	StateConnected    = "CONNECTED"
	StateSubscribing  = "SUBSCRIBING"
	StateRunning      = "RUNNING"
	StateReconnecting = "RECONNECTING"
	StateFailed       = "FAILED"
)

type ConnectionState struct {
	Exchange          string `json:"exchange"`
	ConnectionType    string `json:"connection_type"`
	Status            string `json:"status"`
	SubscriptionCount int    `json:"subscription_count"`
	LastMessageTime   int64  `json:"last_message_time"`
	ReconnectCount    int    `json:"reconnect_count"`
}
