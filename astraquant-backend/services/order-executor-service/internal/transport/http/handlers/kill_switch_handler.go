package handlers

import "github.com/gin-gonic/gin"

func TriggerKillSwitch(c *gin.Context) {
	c.JSON(200, gin.H{"kill_switch_id": "ks_mock", "enabled": true})
}
func ReleaseKillSwitch(c *gin.Context) {
	c.JSON(200, gin.H{"kill_switch_id": c.Param("id"), "enabled": false})
}
