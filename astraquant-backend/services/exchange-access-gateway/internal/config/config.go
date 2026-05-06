package config

import (
	"strings"
	"time"

	"github.com/spf13/viper"
)

type Config struct {
	ServiceName     string
	Env             string
	HTTPPort        string
	PostgresDSN     string
	RedisAddr       string
	NATSURL         string
	OKXRestBaseURL  string
	OKXTimeout      time.Duration
	OKXEnableDemo   bool
	LogLevel        string
	RateLimitEnable bool
	AuditEnable     bool
}

func Load() Config {
	viper.AutomaticEnv()
	viper.SetEnvKeyReplacer(strings.NewReplacer(".", "_"))
	setDefault("SERVICE_NAME", "exchange-access-gateway")
	setDefault("ENV", "dev")
	setDefault("HTTP_PORT", "8010")
	setDefault("POSTGRES_DSN", "postgres://astra:astra_password@localhost:5432/astraquant?sslmode=disable")
	setDefault("REDIS_ADDR", "localhost:6379")
	setDefault("NATS_URL", "nats://localhost:4222")
	setDefault("OKX_REST_BASE_URL", "https://www.okx.com")
	setDefault("OKX_TIMEOUT_MS", 5000)
	setDefault("OKX_ENABLE_DEMO", false)
	setDefault("LOG_LEVEL", "INFO")
	setDefault("RATE_LIMIT_ENABLED", true)
	setDefault("AUDIT_ENABLED", true)

	return Config{
		ServiceName:     viper.GetString("SERVICE_NAME"),
		Env:             viper.GetString("ENV"),
		HTTPPort:        viper.GetString("HTTP_PORT"),
		PostgresDSN:     viper.GetString("POSTGRES_DSN"),
		RedisAddr:       viper.GetString("REDIS_ADDR"),
		NATSURL:         viper.GetString("NATS_URL"),
		OKXRestBaseURL:  viper.GetString("OKX_REST_BASE_URL"),
		OKXTimeout:      time.Duration(viper.GetInt("OKX_TIMEOUT_MS")) * time.Millisecond,
		OKXEnableDemo:   viper.GetBool("OKX_ENABLE_DEMO"),
		LogLevel:        viper.GetString("LOG_LEVEL"),
		RateLimitEnable: viper.GetBool("RATE_LIMIT_ENABLED"),
		AuditEnable:     viper.GetBool("AUDIT_ENABLED"),
	}
}

func setDefault(key string, value any) { viper.SetDefault(key, value) }
