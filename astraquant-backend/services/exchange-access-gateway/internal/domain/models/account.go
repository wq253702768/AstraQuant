package models

type UnifiedAccount struct {
	Exchange  string `json:"exchange"`
	AccountID string `json:"account_id"`
	Equity    string `json:"equity"`
}
