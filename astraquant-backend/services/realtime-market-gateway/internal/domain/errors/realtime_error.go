package errors

type RealtimeError struct {
	Code    string
	Message string
}

func (e RealtimeError) Error() string { return e.Code + ": " + e.Message }
