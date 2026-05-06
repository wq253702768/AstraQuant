package publisher

import "github.com/astraquant/order-executor-service/internal/domain/models"

type NATSPublisher struct{}

func (p NATSPublisher) Publish(topic string, order models.LiveOrder) error { return nil }
