package rules

import (
	"fmt"
	"github.com/astraquant/live-risk-guard-service/internal/config"
	"github.com/astraquant/live-risk-guard-service/internal/domain/models"
)

type GatewayDisconnectRule struct{ Cfg config.Config }

func (r GatewayDisconnectRule) Evaluate(input models.LiveRiskInput) RuleResult {
	if input.GatewayDisconnectedSeconds >= 15 {
		return RuleResult{Triggered: true, RuleCode: "GATEWAY_DISCONNECT_RULE", RuleName: "网关断连规则", Level: "WARNING", Action: "SET_REDUCE_ONLY", Reason: "私有网关断连", CurrentValue: fmt.Sprintf("%v", input), ThresholdValue: "configured"}
	}
	return pass("GATEWAY_DISCONNECT_RULE", "网关断连规则")
}
