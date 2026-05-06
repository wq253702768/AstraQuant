package models

type TriggeredRule struct {
	RuleCode     string `json:"rule_code"`
	RuleName     string `json:"rule_name"`
	Severity     string `json:"severity"`
	Result       string `json:"result"`
	Message      string `json:"message"`
	CurrentValue string `json:"current_value"`
	LimitValue   string `json:"limit_value"`
}
type RuleResult struct {
	RuleCode     string
	RuleName     string
	Passed       bool
	Decision     string
	Severity     string
	Message      string
	CurrentValue string
	LimitValue   string
}
type RiskRuleConfig struct {
	RuleCode string
	RuleName string
	Enabled  bool
	Severity string
	Config   map[string]any
	Version  string
}
