package okx_ws

import (
	"github.com/gorilla/websocket"
	"net/url"
)

type Client struct {
	URL  string
	Conn *websocket.Conn
}

func NewClient(rawURL string) *Client { return &Client{URL: rawURL} }
func (c *Client) Connect() error {
	u, err := url.Parse(c.URL)
	if err != nil {
		return err
	}
	conn, _, err := websocket.DefaultDialer.Dial(u.String(), nil)
	if err != nil {
		return err
	}
	c.Conn = conn
	return nil
}
func (c *Client) Close() error {
	if c.Conn != nil {
		return c.Conn.Close()
	}
	return nil
}
