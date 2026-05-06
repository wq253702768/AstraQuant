package config

import (
	"github.com/spf13/viper"
	"strings"
)

type Config struct {
	ServiceName                   string
	Env                           string
	HTTPPort                      string
	PostgresDSN                   string
	RedisAddr                     string
	NATSURL                       string
	RealtimeStateServiceURL       string
	StrategyServiceURL            string
	SignalEngineURL               string
	DefaultExchange               string
	DefaultSymbols                []string
	RuleVersion                   string
	MaxSpreadPct                  float64
	MaxAbsFundingRate             float64
	DefaultMaxLeverage            float64
	DefaultMaxPositionPct         float64
	DefaultMaxSingleTradeLossPct  float64
	DefaultMaxDailyLossPct        float64
	DefaultMaxConsecutiveLosses   int
	DefaultMaxStrategyDrawdownPct float64
	DefaultOpenCooldownSeconds    int
	LogLevel                      string
}

func Load() Config {
	viper.AutomaticEnv()
	set("SERVICE_NAME", "risk-engine")
	set("ENV", "dev")
	set("HTTP_PORT", "8013")
	set("POSTGRES_DSN", "postgres://astra:astra_password@localhost:5432/astraquant?sslmode=disable")
	set("REDIS_ADDR", "localhost:6379")
	set("NATS_URL", "nats://localhost:4222")
	set("REALTIME_STATE_SERVICE_URL", "http://localhost:8012")
	set("STRATEGY_SERVICE_URL", "http://localhost:8002")
	set("SIGNAL_ENGINE_URL", "http://localhost:8009")
	set("DEFAULT_EXCHANGE", "OKX")
	set("DEFAULT_SYMBOLS", "BTC-USDT-SWAP,ETH-USDT-SWAP")
	set("RULE_VERSION", "v1.0")
	set("MAX_SPREAD_PCT", 0.001)
	set("MAX_ABS_FUNDING_RATE", 0.0005)
	set("DEFAULT_MAX_LEVERAGE", 3)
	set("DEFAULT_MAX_POSITION_PCT", 0.2)
	set("DEFAULT_MAX_SINGLE_TRADE_LOSS_PCT", 0.005)
	set("DEFAULT_MAX_DAILY_LOSS_PCT", 0.02)
	set("DEFAULT_MAX_CONSECUTIVE_LOSSES", 3)
	set("DEFAULT_MAX_STRATEGY_DRAWDOWN_PCT", 0.06)
	set("DEFAULT_OPEN_COOLDOWN_SECONDS", 300)
	set("LOG_LEVEL", "INFO")
	return Config{ServiceName: viper.GetString("SERVICE_NAME"), Env: viper.GetString("ENV"), HTTPPort: viper.GetString("HTTP_PORT"), PostgresDSN: viper.GetString("POSTGRES_DSN"), RedisAddr: viper.GetString("REDIS_ADDR"), NATSURL: viper.GetString("NATS_URL"), RealtimeStateServiceURL: viper.GetString("REALTIME_STATE_SERVICE_URL"), StrategyServiceURL: viper.GetString("STRATEGY_SERVICE_URL"), SignalEngineURL: viper.GetString("SIGNAL_ENGINE_URL"), DefaultExchange: viper.GetString("DEFAULT_EXCHANGE"), DefaultSymbols: split(viper.GetString("DEFAULT_SYMBOLS")), RuleVersion: viper.GetString("RULE_VERSION"), MaxSpreadPct: viper.GetFloat64("MAX_SPREAD_PCT"), MaxAbsFundingRate: viper.GetFloat64("MAX_ABS_FUNDING_RATE"), DefaultMaxLeverage: viper.GetFloat64("DEFAULT_MAX_LEVERAGE"), DefaultMaxPositionPct: viper.GetFloat64("DEFAULT_MAX_POSITION_PCT"), DefaultMaxSingleTradeLossPct: viper.GetFloat64("DEFAULT_MAX_SINGLE_TRADE_LOSS_PCT"), DefaultMaxDailyLossPct: viper.GetFloat64("DEFAULT_MAX_DAILY_LOSS_PCT"), DefaultMaxConsecutiveLosses: viper.GetInt("DEFAULT_MAX_CONSECUTIVE_LOSSES"), DefaultMaxStrategyDrawdownPct: viper.GetFloat64("DEFAULT_MAX_STRATEGY_DRAWDOWN_PCT"), DefaultOpenCooldownSeconds: viper.GetInt("DEFAULT_OPEN_COOLDOWN_SECONDS"), LogLevel: viper.GetString("LOG_LEVEL")}
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
