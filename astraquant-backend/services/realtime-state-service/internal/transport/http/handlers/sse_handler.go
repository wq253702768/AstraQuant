package handlers

import (
	"fmt"
	"io"
	"time"

	"github.com/gin-gonic/gin"
)

func SSE(c *gin.Context) {
	c.Header("Content-Type", "text/event-stream")
	c.Stream(func(w io.Writer) bool {
		fmt.Fprintf(w, "event: market\ndata: {\"fresh\":true,\"push_time\":%d}\n\n", time.Now().UnixMilli())
		return false
	})
}
