package service

import "testing"

func TestFreshnessCalculate(t *testing.T) {
	service := FreshnessService{}
	f := service.Calculate(1000, 1050)
	if f.Level != "FRESH" {
		t.Fatal("expected fresh")
	}
	if service.Calculate(1000, 4000).Level != "STALE" {
		t.Fatal("expected stale")
	}
}
