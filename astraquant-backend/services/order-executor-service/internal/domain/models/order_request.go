package models

type UnifiedOrderRequest struct {
	AccountID  string `json:"account_id"`
	Exchange   string `json:"exchange"`
	InstID     string `json:"inst_id"`
	TdMode     string `json:"td_mode"`
	Side       string `json:"side"`
	PosSide    string `json:"pos_side"`
	OrdType    string `json:"ord_type"`
	Px         string `json:"px"`
	Sz         string `json:"sz"`
	ClOrdID    string `json:"cl_ord_id"`
	ReduceOnly bool   `json:"reduce_only"`
	Tag        string `json:"tag"`
}
