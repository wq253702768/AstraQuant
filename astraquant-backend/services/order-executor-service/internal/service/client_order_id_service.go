package service

import (
	"math/rand"
	"time"
)

type ClientOrderIDService struct{ Prefix string }

func (s ClientOrderIDService) Generate(side string) string {
	suffix := "L"
	if side == "sell" || side == "SELL" {
		suffix = "S"
	}
	letters := []rune("ABCDEFGHJKLMNPQRSTUVWXYZ23456789")
	b := make([]rune, 6)
	for i := range b {
		b[i] = letters[rand.Intn(len(letters))]
	}
	return s.Prefix + time.Now().Format("0601021504") + string(b) + suffix
}
