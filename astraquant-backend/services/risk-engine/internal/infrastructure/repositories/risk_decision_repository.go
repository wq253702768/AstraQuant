package repositories

import "github.com/astraquant/risk-engine/internal/domain/models"

type RiskDecisionRepository struct{ Memory []models.RiskDecision }

func (r *RiskDecisionRepository) Save(d models.RiskDecision)  { r.Memory = append(r.Memory, d) }
func (r *RiskDecisionRepository) List() []models.RiskDecision { return r.Memory }
func (r *RiskDecisionRepository) Get(id string) (models.RiskDecision, bool) {
	for _, d := range r.Memory {
		if d.ID == id {
			return d, true
		}
	}
	return models.RiskDecision{}, false
}
