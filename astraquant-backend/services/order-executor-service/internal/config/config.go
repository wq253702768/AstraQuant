package config

import (
	"github.com/spf13/viper"
)

type Config struct {
	ServiceName                   string
	Env                           string
	HTTPPort                      string
	PostgresDSN                   string
	RedisAddr                     string
	NATSURL                       string
	OKXPrivateGatewayURL          string
	ExchangeAccountServiceURL     string
	RiskEngineURL                 string
	SignalEngineURL               string
	PaperMonitorServiceURL        string
	LiveTradingEnabled            bool
	ExecutionMode                 string
	SmallMaxOrderNotionalPct      float64
	SmallMaxStrategyNotionalPct   float64
	SmallMaxLeverage              float64
	SmallMaxDailyOrderCount       int
	OrderSubmitTimeoutMs          int
	OrderAckTimeoutSeconds        int
	OrderReconcileIntervalSeconds int
	UnknownOrderMaxRetry          int
	ClientOrderIDPrefix           string
	OKXOrderTag                   string
	LogLevel                      string
}

func Load() Config {
	viper.AutomaticEnv()
	set("SERVICE_NAME", "order-executor-service")
	set("ENV", "dev")
	set("HTTP_PORT", "8018")
	set("POSTGRES_DSN", "postgres://astra:astra_password@localhost:5432/astraquant?sslmode=disable")
	set("REDIS_ADDR", "localhost:6379")
	set("NATS_URL", "nats://localhost:4222")
	set("OKX_PRIVATE_GATEWAY_URL", "http://localhost:8017")
	set("EXCHANGE_ACCOUNT_SERVICE_URL", "http://localhost:8016")
	set("RISK_ENGINE_URL", "http://localhost:8013")
	set("SIGNAL_ENGINE_URL", "http://localhost:8009")
	set("PAPER_MONITOR_SERVICE_URL", "http://localhost:8015")
	set("LIVE_TRADING_ENABLED", false)
	set("ORDER_EXECUTION_MODE", "DRY_RUN")
	set("LIVE_SMALL_MAX_ORDER_NOTIONAL_PCT", 0.05)
	set("LIVE_SMALL_MAX_STRATEGY_NOTIONAL_PCT", 0.10)
	set("LIVE_SMALL_MAX_LEVERAGE", 2)
	set("LIVE_SMALL_MAX_DAILY_ORDER_COUNT", 10)
	set("ORDER_SUBMIT_TIMEOUT_MS", 3000)
	set("ORDER_ACK_TIMEOUT_SECONDS", 3)
	set("ORDER_RECONCILE_INTERVAL_SECONDS", 5)
	set("UNKNOWN_ORDER_MAX_RETRY", 10)
	set("CLIENT_ORDER_ID_PREFIX", "AQ")
	set("OKX_ORDER_TAG", "ASTRA")
	set("LOG_LEVEL", "INFO")
	return Config{ServiceName: viper.GetString("SERVICE_NAME"), Env: viper.GetString("ENV"), HTTPPort: viper.GetString("HTTP_PORT"), PostgresDSN: viper.GetString("POSTGRES_DSN"), RedisAddr: viper.GetString("REDIS_ADDR"), NATSURL: viper.GetString("NATS_URL"), OKXPrivateGatewayURL: viper.GetString("OKX_PRIVATE_GATEWAY_URL"), ExchangeAccountServiceURL: viper.GetString("EXCHANGE_ACCOUNT_SERVICE_URL"), RiskEngineURL: viper.GetString("RISK_ENGINE_URL"), SignalEngineURL: viper.GetString("SIGNAL_ENGINE_URL"), PaperMonitorServiceURL: viper.GetString("PAPER_MONITOR_SERVICE_URL"), LiveTradingEnabled: viper.GetBool("LIVE_TRADING_ENABLED"), ExecutionMode: viper.GetString("ORDER_EXECUTION_MODE"), SmallMaxOrderNotionalPct: viper.GetFloat64("LIVE_SMALL_MAX_ORDER_NOTIONAL_PCT"), SmallMaxStrategyNotionalPct: viper.GetFloat64("LIVE_SMALL_MAX_STRATEGY_NOTIONAL_PCT"), SmallMaxLeverage: viper.GetFloat64("LIVE_SMALL_MAX_LEVERAGE"), SmallMaxDailyOrderCount: viper.GetInt("LIVE_SMALL_MAX_DAILY_ORDER_COUNT"), OrderSubmitTimeoutMs: viper.GetInt("ORDER_SUBMIT_TIMEOUT_MS"), OrderAckTimeoutSeconds: viper.GetInt("ORDER_ACK_TIMEOUT_SECONDS"), OrderReconcileIntervalSeconds: viper.GetInt("ORDER_RECONCILE_INTERVAL_SECONDS"), UnknownOrderMaxRetry: viper.GetInt("UNKNOWN_ORDER_MAX_RETRY"), ClientOrderIDPrefix: viper.GetString("CLIENT_ORDER_ID_PREFIX"), OKXOrderTag: viper.GetString("OKX_ORDER_TAG"), LogLevel: viper.GetString("LOG_LEVEL")}
}
func set(k string, v any) { viper.SetDefault(k, v) }
