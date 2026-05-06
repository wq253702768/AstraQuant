package okx

import domainerrors "github.com/astraquant/exchange-access-gateway/internal/domain/errors"

func MapErrorCode(okxCode string) domainerrors.Code {
	switch okxCode {
	case "0", "":
		return ""
	case "50011", "50061":
		return domainerrors.RateLimited
	case "50113":
		return domainerrors.AuthFailed
	case "50110":
		return domainerrors.IPNotAllowed
	case "51008":
		return domainerrors.InsufficientBalance
	case "51000":
		return domainerrors.OrderRejected
	case "51603":
		return domainerrors.OrderNotFound
	default:
		return domainerrors.UnknownError
	}
}
