package config

import (
	"github.com/spf13/viper"
	"strings"
	"time"
)

type Config struct {
	ServiceName         string
	Env                 string
	HTTPPort            string
	NATSURL             string
	RedisAddr           string
	OKXPublicWSURL      string
	OKXBusinessWSURL    string
	ExchangeGatewayURL  string
	PingInterval        time.Duration
	PongTimeout         time.Duration
	ReconnectMaxBackoff time.Duration
	FundingPollEnabled  bool
	FundingPollInterval time.Duration
	DefaultSymbols      []string
	DefaultTimeframes   []string
	LogLevel            string
}

func Load() Config {
	viper.AutomaticEnv()
	viper.SetEnvKeyReplacer(strings.NewReplacer(".", "_"))
	setDefault("SERVICE_NAME", "realtime-market-gateway")
	setDefault("ENV", "dev")
	setDefault("HTTP_PORT", "8011")
	setDefault("NATS_URL", "nats://localhost:4222")
	setDefault("REDIS_ADDR", "localhost:6379")
	setDefault("OKX_PUBLIC_WS_URL", "wss://ws.okx.com:8443/ws/v5/public")
	setDefault("OKX_BUSINESS_WS_URL", "wss://ws.okx.com:8443/ws/v5/business")
	setDefault("EXCHANGE_GATEWAY_URL", "http://localhost:8010")
	setDefault("WS_PING_INTERVAL_SECONDS", 20)
	setDefault("WS_PONG_TIMEOUT_SECONDS", 10)
	setDefault("WS_RECONNECT_MAX_BACKOFF_SECONDS", 30)
	setDefault("FUNDING_POLL_ENABLED", true)
	setDefault("FUNDING_POLL_INTERVAL_SECONDS", 30)
	setDefault("DEFAULT_SYMBOLS", "BTC-USDT-SWAP,ETH-USDT-SWAP")
	setDefault("DEFAULT_TIMEFRAMES", "1m,5m")
	setDefault("LOG_LEVEL", "INFO")
	return Config{ServiceName: viper.GetString("SERVICE_NAME"), Env: viper.GetString("ENV"), HTTPPort: viper.GetString("HTTP_PORT"), NATSURL: viper.GetString("NATS_URL"), RedisAddr: viper.GetString("REDIS_ADDR"), OKXPublicWSURL: viper.GetString("OKX_PUBLIC_WS_URL"), OKXBusinessWSURL: viper.GetString("OKX_BUSINESS_WS_URL"), ExchangeGatewayURL: viper.GetString("EXCHANGE_GATEWAY_URL"), PingInterval: time.Duration(viper.GetInt("WS_PING_INTERVAL_SECONDS")) * time.Second, PongTimeout: time.Duration(viper.GetInt("WS_PONG_TIMEOUT_SECONDS")) * time.Second, ReconnectMaxBackoff: time.Duration(viper.GetInt("WS_RECONNECT_MAX_BACKOFF_SECONDS")) * time.Second, FundingPollEnabled: viper.GetBool("FUNDING_POLL_ENABLED"), FundingPollInterval: time.Duration(viper.GetInt("FUNDING_POLL_INTERVAL_SECONDS")) * time.Second, DefaultSymbols: split(viper.GetString("DEFAULT_SYMBOLS")), DefaultTimeframes: split(viper.GetString("DEFAULT_TIMEFRAMES")), LogLevel: viper.GetString("LOG_LEVEL")}
}
func setDefault(k string, v any) { viper.SetDefault(k, v) }
func split(s string) []string {
	parts := strings.Split(s, ",")
	out := make([]string, 0, len(parts))
	for _, p := range parts {
		p = strings.TrimSpace(p)
		if p != "" {
			out = append(out, p)
		}
	}
	return out
}
