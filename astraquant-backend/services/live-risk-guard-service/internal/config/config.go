package config

import "github.com/spf13/viper"

type Config struct {
	ServiceName                  string
	Env                          string
	HTTPPort                     string
	NATSURL                      string
	RedisAddr                    string
	OrderExecutorServiceURL      string
	AccountDailyLossLimitPct     float64
	StrategyDailyLossLimitPct    float64
	AccountMaxDrawdownPct        float64
	StrategyMaxDrawdownPct       float64
	MaxConsecutiveLosses         int
	MaxOrderUnknownCountStrategy int
	MaxOrderUnknownCountAccount  int
	OrderFailureCountLimit       int
	MaxSlippagePct               float64
	MaxAbsFundingRate            float64
	AutoCancelEnabled            bool
	AutoRecoveryEnabled          bool
	LogLevel                     string
}

func Load() Config {
	viper.AutomaticEnv()
	set("SERVICE_NAME", "live-risk-guard-service")
	set("ENV", "dev")
	set("HTTP_PORT", "8019")
	set("NATS_URL", "nats://localhost:4222")
	set("REDIS_ADDR", "localhost:6379")
	set("ORDER_EXECUTOR_SERVICE_URL", "http://localhost:8018")
	set("ACCOUNT_DAILY_LOSS_LIMIT_PCT", 0.02)
	set("STRATEGY_DAILY_LOSS_LIMIT_PCT", 0.01)
	set("ACCOUNT_MAX_DRAWDOWN_PCT", 0.05)
	set("STRATEGY_MAX_DRAWDOWN_PCT", 0.03)
	set("MAX_CONSECUTIVE_LOSSES", 3)
	set("MAX_ORDER_UNKNOWN_COUNT_STRATEGY", 1)
	set("MAX_ORDER_UNKNOWN_COUNT_ACCOUNT", 2)
	set("ORDER_FAILURE_COUNT_LIMIT", 3)
	set("MAX_SLIPPAGE_PCT", 0.003)
	set("MAX_ABS_FUNDING_RATE", 0.0008)
	set("AUTO_CANCEL_ENABLED", true)
	set("AUTO_RECOVERY_ENABLED", false)
	set("LOG_LEVEL", "INFO")
	return Config{ServiceName: viper.GetString("SERVICE_NAME"), Env: viper.GetString("ENV"), HTTPPort: viper.GetString("HTTP_PORT"), NATSURL: viper.GetString("NATS_URL"), RedisAddr: viper.GetString("REDIS_ADDR"), OrderExecutorServiceURL: viper.GetString("ORDER_EXECUTOR_SERVICE_URL"), AccountDailyLossLimitPct: viper.GetFloat64("ACCOUNT_DAILY_LOSS_LIMIT_PCT"), StrategyDailyLossLimitPct: viper.GetFloat64("STRATEGY_DAILY_LOSS_LIMIT_PCT"), AccountMaxDrawdownPct: viper.GetFloat64("ACCOUNT_MAX_DRAWDOWN_PCT"), StrategyMaxDrawdownPct: viper.GetFloat64("STRATEGY_MAX_DRAWDOWN_PCT"), MaxConsecutiveLosses: viper.GetInt("MAX_CONSECUTIVE_LOSSES"), MaxOrderUnknownCountStrategy: viper.GetInt("MAX_ORDER_UNKNOWN_COUNT_STRATEGY"), MaxOrderUnknownCountAccount: viper.GetInt("MAX_ORDER_UNKNOWN_COUNT_ACCOUNT"), OrderFailureCountLimit: viper.GetInt("ORDER_FAILURE_COUNT_LIMIT"), MaxSlippagePct: viper.GetFloat64("MAX_SLIPPAGE_PCT"), MaxAbsFundingRate: viper.GetFloat64("MAX_ABS_FUNDING_RATE"), AutoCancelEnabled: viper.GetBool("AUTO_CANCEL_ENABLED"), AutoRecoveryEnabled: viper.GetBool("AUTO_RECOVERY_ENABLED"), LogLevel: viper.GetString("LOG_LEVEL")}
}
func set(k string, v any) { viper.SetDefault(k, v) }
