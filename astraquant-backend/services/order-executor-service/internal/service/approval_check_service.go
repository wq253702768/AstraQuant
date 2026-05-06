package service

import "github.com/astraquant/order-executor-service/internal/domain/models"

type ApprovalCheckService struct{}

func (s ApprovalCheckService) Approved(ctx models.ExecutionContext) bool {
	return ctx.AdmissionResult.Decision == "ALLOW_SMALL_LIVE_APPLICATION" && ctx.AdmissionResult.ApprovalStatus == "APPROVED"
}
