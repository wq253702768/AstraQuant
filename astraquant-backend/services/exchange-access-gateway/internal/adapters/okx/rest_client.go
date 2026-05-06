package okx

import (
	"context"
	"fmt"
	"net/http"
	"time"

	domainerrors "github.com/astraquant/exchange-access-gateway/internal/domain/errors"
	"github.com/go-resty/resty/v2"
)

type RestClient struct {
	client     *resty.Client
	baseURL    string
	enableDemo bool
}

func NewRestClient(baseURL string, timeout time.Duration, enableDemo bool) *RestClient {
	client := resty.New().SetBaseURL(baseURL).SetTimeout(timeout)
	return &RestClient{client: client, baseURL: baseURL, enableDemo: enableDemo}
}

func (c *RestClient) Get(ctx context.Context, endpoint string, query map[string]string) (*responseEnvelope, int, error) {
	var payload responseEnvelope
	req := c.client.R().SetContext(ctx).SetResult(&payload).SetQueryParams(query)
	if c.enableDemo {
		req.SetHeader("x-simulated-trading", "1")
	}
	resp, err := req.Get(endpoint)
	if err != nil {
		return nil, 0, domainerrors.New(domainerrors.NetworkError, err.Error(), http.StatusBadGateway)
	}
	if resp.IsError() {
		return nil, resp.StatusCode(), domainerrors.New(domainerrors.ExchangeUnavailable, fmt.Sprintf("okx http status %d", resp.StatusCode()), http.StatusBadGateway)
	}
	if payload.Code != "0" {
		mapped := MapErrorCode(payload.Code)
		return &payload, resp.StatusCode(), domainerrors.New(mapped, payload.Msg, http.StatusBadGateway)
	}
	return &payload, resp.StatusCode(), nil
}
