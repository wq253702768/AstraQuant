package handlers

import "github.com/gin-gonic/gin"

func Rules(c *gin.Context) {
	c.JSON(200, gin.H{"items": []gin.H{{"rule_code": "ORDER_UNKNOWN_RULE", "rule_name": "订单未知状态熔断规则", "enabled": true, "level": "CRITICAL", "action": "BLOCK_TRADING", "version": "v1.0"}}})
}
