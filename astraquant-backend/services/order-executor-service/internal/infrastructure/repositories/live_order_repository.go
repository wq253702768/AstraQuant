package repositories

import "github.com/astraquant/order-executor-service/internal/domain/models"

type LiveOrderRepository struct{ Memory []models.LiveOrder }

func (r *LiveOrderRepository) Save(o models.LiveOrder)  { r.Memory = append(r.Memory, o) }
func (r *LiveOrderRepository) List() []models.LiveOrder { return r.Memory }
func (r *LiveOrderRepository) Get(id string) (models.LiveOrder, bool) {
	for _, o := range r.Memory {
		if o.ID == id {
			return o, true
		}
	}
	return models.LiveOrder{}, false
}
