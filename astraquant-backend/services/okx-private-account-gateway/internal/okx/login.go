package okx

type LoginArg struct {
	APIKey     string `json:"apiKey"`
	Passphrase string `json:"passphrase"`
	Timestamp  string `json:"timestamp"`
	Sign       string `json:"sign"`
}
type LoginMessage struct {
	Op   string     `json:"op"`
	Args []LoginArg `json:"args"`
}

func BuildLogin(apiKey, passphrase, timestamp, sign string) LoginMessage {
	return LoginMessage{Op: "login", Args: []LoginArg{{APIKey: apiKey, Passphrase: passphrase, Timestamp: timestamp, Sign: sign}}}
}
