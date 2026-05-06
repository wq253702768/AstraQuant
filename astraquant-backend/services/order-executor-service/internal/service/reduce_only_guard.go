package service

type ReduceOnlyGuard struct{}

func (g ReduceOnlyGuard) Valid(action string, reduceOnly bool) bool {
	return !reduceOnly || action != "OPEN"
}
