package errors

type RiskError struct {
	Code    string
	Message string
}

func (e RiskError) Error() string { return e.Code + ": " + e.Message }
