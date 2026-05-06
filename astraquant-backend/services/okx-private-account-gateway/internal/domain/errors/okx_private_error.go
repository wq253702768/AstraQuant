package errors

type OKXPrivateError struct {
	Code    string
	Message string
}

func (e OKXPrivateError) Error() string { return e.Code + ": " + e.Message }
