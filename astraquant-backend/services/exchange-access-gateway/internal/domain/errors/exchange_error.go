package errors

import "fmt"

type Code string

const (
	RateLimited         Code = "RATE_LIMITED"
	AuthFailed          Code = "AUTH_FAILED"
	IPNotAllowed        Code = "IP_NOT_ALLOWED"
	InsufficientBalance Code = "INSUFFICIENT_BALANCE"
	OrderRejected       Code = "ORDER_REJECTED"
	OrderNotFound       Code = "ORDER_NOT_FOUND"
	PositionModeError   Code = "POSITION_MODE_ERROR"
	SymbolNotSupported  Code = "SYMBOL_NOT_SUPPORTED"
	ExchangeUnavailable Code = "EXCHANGE_UNAVAILABLE"
	NetworkError        Code = "NETWORK_ERROR"
	BadResponse         Code = "BAD_RESPONSE"
	NotImplemented      Code = "NOT_IMPLEMENTED"
	UnknownError        Code = "UNKNOWN_ERROR"
)

type ExchangeError struct {
	Code       Code
	Message    string
	StatusCode int
}

func (e *ExchangeError) Error() string {
	return fmt.Sprintf("%s: %s", e.Code, e.Message)
}

func New(code Code, message string, statusCode int) *ExchangeError {
	return &ExchangeError{Code: code, Message: message, StatusCode: statusCode}
}

var ErrNotImplemented = New(NotImplemented, "method not implemented", 501)
