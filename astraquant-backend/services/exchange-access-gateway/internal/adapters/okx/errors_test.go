package okx

import (
	domainerrors "github.com/astraquant/exchange-access-gateway/internal/domain/errors"
	"testing"
)

func TestErrorMapper(t *testing.T) {
	if MapErrorCode("50011") != domainerrors.RateLimited {
		t.Fatal("expected RATE_LIMITED")
	}
	if MapErrorCode("50113") != domainerrors.AuthFailed {
		t.Fatal("expected AUTH_FAILED")
	}
	if MapErrorCode("51603") != domainerrors.OrderNotFound {
		t.Fatal("expected ORDER_NOT_FOUND")
	}
}
