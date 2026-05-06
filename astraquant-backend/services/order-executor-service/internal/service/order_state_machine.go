package service

var allowed = map[string][]string{"CREATED": {"DRY_RUN_PASSED", "GATED_REJECTED", "SUBMITTING"}, "SUBMITTING": {"SUBMITTED", "REJECTED", "FAILED", "UNKNOWN"}, "SUBMITTED": {"ACKNOWLEDGED", "UNKNOWN"}, "ACKNOWLEDGED": {"PARTIALLY_FILLED", "FILLED", "CANCEL_REQUESTED", "UNKNOWN"}, "PARTIALLY_FILLED": {"FILLED", "CANCEL_REQUESTED", "UNKNOWN"}, "CANCEL_REQUESTED": {"CANCELED", "UNKNOWN"}}

type OrderStateMachine struct{}

func (m OrderStateMachine) Can(from, to string) bool {
	if from == to {
		return true
	}
	for _, v := range allowed[from] {
		if v == to {
			return true
		}
	}
	return false
}
