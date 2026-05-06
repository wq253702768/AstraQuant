package config

import "github.com/spf13/viper"

type Config struct {
	ServiceName     string
	Env             string
	HTTPPort        string
	NATSURL         string
	OKXRestBaseURL  string
	OKXPrivateWSURL string
}

func Load() Config {
	viper.AutomaticEnv()
	viper.SetDefault("SERVICE_NAME", "okx-private-account-gateway")
	viper.SetDefault("ENV", "dev")
	viper.SetDefault("HTTP_PORT", "8017")
	viper.SetDefault("NATS_URL", "nats://localhost:4222")
	viper.SetDefault("OKX_REST_BASE_URL", "https://www.okx.com")
	viper.SetDefault("OKX_PRIVATE_WS_URL", "wss://ws.okx.com:8443/ws/v5/private")
	return Config{ServiceName: viper.GetString("SERVICE_NAME"), Env: viper.GetString("ENV"), HTTPPort: viper.GetString("HTTP_PORT"), NATSURL: viper.GetString("NATS_URL"), OKXRestBaseURL: viper.GetString("OKX_REST_BASE_URL"), OKXPrivateWSURL: viper.GetString("OKX_PRIVATE_WS_URL")}
}
