package errors

type LiveRiskError struct {
	Code    string
	Message string
}

func (e LiveRiskError) Error() string { return e.Code + ": " + e.Message }
