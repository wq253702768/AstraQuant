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

func Sign(in SignInput) string {
	pre := in.Timestamp + strings.ToUpper(in.Method) + in.RequestPath + in.Body
	mac := hmac.New(sha256.New, []byte(in.SecretKey))
	mac.Write([]byte(pre))
	return base64.StdEncoding.EncodeToString(mac.Sum(nil))
}
