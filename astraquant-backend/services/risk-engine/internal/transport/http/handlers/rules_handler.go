package handlers

import "github.com/gin-gonic/gin"

func Rules(c *gin.Context) {
	c.JSON(200, gin.H{"items": []gin.H{{"rule_code": "MARKET_FRESHNESS_RULE", "rule_name": "行情新鲜度规则", "enabled": true, "severity": "HARD_BLOCK", "version": "v1.0"}, {"rule_code": "BBO_SPREAD_RULE", "rule_name": "盘口价差规则", "enabled": true, "severity": "HARD_BLOCK", "version": "v1.0"}}})
}
