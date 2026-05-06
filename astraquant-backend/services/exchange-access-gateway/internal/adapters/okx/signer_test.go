package okx

import "testing"

func TestOKXSigner(t *testing.T) {
	signature := Sign(SignInput{Timestamp: "2020-12-08T09:08:57.715Z", Method: "GET", RequestPath: "/api/v5/account/balance?ccy=BTC", Body: "", SecretKey: "22582BD0CFF14C41EDBF1AB98506286D"})
	if signature != "HiZhvSfMtWJA3uUIVXV3a/bSXNPCWvYFXoGCVS8V4zY=" {
		t.Fatalf("unexpected signature: %s", signature)
	}
}
