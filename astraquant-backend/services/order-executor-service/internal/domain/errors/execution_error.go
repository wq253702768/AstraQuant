package errors

type ExecutionError struct {
	Code    string
	Message string
}

func (e ExecutionError) Error() string { return e.Code + ": " + e.Message }
