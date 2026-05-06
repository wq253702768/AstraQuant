package okx

import (
	"crypto/hmac"
	"crypto/sha256"
	"encoding/base64"
	"strings"
)

type SignInput struct {
	Timestamp   string
	Method      string
	RequestPath string
	Body        string
	SecretKey   string
}

func Sign(input SignInput) string {
	preHash := input.Timestamp + strings.ToUpper(input.Method) + input.RequestPath + input.Body
	mac := hmac.New(sha256.New, []byte(input.SecretKey))
	_, _ = mac.Write([]byte(preHash))
	return base64.StdEncoding.EncodeToString(mac.Sum(nil))
}
