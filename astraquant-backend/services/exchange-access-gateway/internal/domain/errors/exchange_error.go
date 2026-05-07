package errors

import "fmt"

type Code string

const (
	RateLimited           Code = "RATE_LIMITED"
	AuthFailed            Code = "AUTH_FAILED"
	IPNotAllowed          Code = "IP_NOT_ALLOWED"
	InsufficientBalance   Code = "INSUFFICIENT_BALANCE"
	OrderRejected         Code = "ORDER_REJECTED"
	OrderNotFound         Code = "ORDER_NOT_FOUND"
	PositionModeError     Code = "POSITION_MODE_ERROR"
	SymbolNotSupported    Code = "SYMBOL_NOT_SUPPORTED"
	TimeframeNotSupported Code = "TIMEFRAME_NOT_SUPPORTED"
	ExchangeUnavailable   Code = "EXCHANGE_UNAVAILABLE"
	NetworkError          Code = "NETWORK_ERROR"
	BadResponse           Code = "BAD_RESPONSE"
	NotImplemented        Code = "NOT_IMPLEMENTED"
	UnknownError          Code = "UNKNOWN_ERROR"
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

func PublicCode(code Code) string {
	switch code {
	case RateLimited:
		return "EXCHANGE_RATE_LIMITED"
	case SymbolNotSupported:
		return "EXCHANGE_SYMBOL_NOT_SUPPORTED"
	case TimeframeNotSupported:
		return "EXCHANGE_TIMEFRAME_NOT_SUPPORTED"
	case BadResponse:
		return "EXCHANGE_RESPONSE_INVALID"
	case NetworkError:
		return "EXCHANGE_REQUEST_FAILED"
	case ExchangeUnavailable:
		return "EXCHANGE_UNAVAILABLE"
	case UnknownError:
		return "EXCHANGE_REQUEST_FAILED"
	default:
		if code == "" {
			return "EXCHANGE_REQUEST_FAILED"
		}
		return "EXCHANGE_" + string(code)
	}
}

func PublicMessage(code Code, message string) string {
	if message != "" {
		return message
	}
	return PublicCode(code)
}

var ErrNotImplemented = New(NotImplemented, "method not implemented", 501)
