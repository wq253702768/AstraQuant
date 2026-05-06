package errors

type StateError struct {
	Code    string
	Message string
}

func (e StateError) Error() string { return e.Code + ": " + e.Message }
