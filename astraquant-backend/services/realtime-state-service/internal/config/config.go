package config

import (
	"github.com/spf13/viper"
	"strings"
)

type Config struct {
	ServiceName       string
	Env               string
	HTTPPort          string
	NATSURL           string
	RedisAddr         string
	RedisDB           int
	DefaultExchange   string
	DefaultSymbols    []string
	DefaultTimeframes []string
	TickerStaleMs     int64
	BBOStaleMs        int64
	TradeStaleMs      int64
	MarkPriceStaleMs  int64
	FundingStaleMs    int64
	RedisWriteEnabled bool
	WSPushEnabled     bool
	SSEPushEnabled    bool
	LogLevel          string
}

func Load() Config {
	viper.AutomaticEnv()
	set("SERVICE_NAME", "realtime-state-service")
	set("ENV", "dev")
	set("HTTP_PORT", "8012")
	set("NATS_URL", "nats://localhost:4222")
	set("REDIS_ADDR", "localhost:6379")
	set("REDIS_DB", 0)
	set("DEFAULT_EXCHANGE", "OKX")
	set("DEFAULT_SYMBOLS", "BTC-USDT-SWAP,ETH-USDT-SWAP")
	set("DEFAULT_TIMEFRAMES", "1m,5m")
	set("TICKER_STALE_MS", 5000)
	set("BBO_STALE_MS", 3000)
	set("TRADE_STALE_MS", 10000)
	set("MARK_PRICE_STALE_MS", 5000)
	set("FUNDING_STALE_MS", 60000)
	set("REDIS_WRITE_ENABLED", true)
	set("WS_PUSH_ENABLED", true)
	set("SSE_PUSH_ENABLED", true)
	set("LOG_LEVEL", "INFO")
	return Config{ServiceName: viper.GetString("SERVICE_NAME"), Env: viper.GetString("ENV"), HTTPPort: viper.GetString("HTTP_PORT"), NATSURL: viper.GetString("NATS_URL"), RedisAddr: viper.GetString("REDIS_ADDR"), RedisDB: viper.GetInt("REDIS_DB"), DefaultExchange: viper.GetString("DEFAULT_EXCHANGE"), DefaultSymbols: split(viper.GetString("DEFAULT_SYMBOLS")), DefaultTimeframes: split(viper.GetString("DEFAULT_TIMEFRAMES")), TickerStaleMs: viper.GetInt64("TICKER_STALE_MS"), BBOStaleMs: viper.GetInt64("BBO_STALE_MS"), TradeStaleMs: viper.GetInt64("TRADE_STALE_MS"), MarkPriceStaleMs: viper.GetInt64("MARK_PRICE_STALE_MS"), FundingStaleMs: viper.GetInt64("FUNDING_STALE_MS"), RedisWriteEnabled: viper.GetBool("REDIS_WRITE_ENABLED"), WSPushEnabled: viper.GetBool("WS_PUSH_ENABLED"), SSEPushEnabled: viper.GetBool("SSE_PUSH_ENABLED"), LogLevel: viper.GetString("LOG_LEVEL")}
}
func set(k string, v any) { viper.SetDefault(k, v) }
func split(s string) []string {
	parts := strings.Split(s, ",")
	out := []string{}
	for _, p := range parts {
		p = strings.TrimSpace(p)
		if p != "" {
			out = append(out, p)
		}
	}
	return out
}
