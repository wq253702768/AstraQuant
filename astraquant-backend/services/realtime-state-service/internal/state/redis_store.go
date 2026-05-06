package state

import (
	"context"
	"encoding/json"
	"github.com/redis/go-redis/v9"
	"time"
)

type RedisStore struct{ client *redis.Client }

func NewRedisStore(addr string, db int) *RedisStore {
	return &RedisStore{client: redis.NewClient(&redis.Options{Addr: addr, DB: db})}
}
func (s *RedisStore) Key(kind, exchange, symbol, stringer string) string {
	if stringer != "" {
		return "realtime:" + kind + ":" + exchange + ":" + symbol + ":" + stringer
	}
	return "realtime:" + kind + ":" + exchange + ":" + symbol
}
func (s *RedisStore) Set(ctx context.Context, key string, value any, ttl time.Duration) error {
	b, _ := json.Marshal(value)
	return s.client.Set(ctx, key, b, ttl).Err()
}
