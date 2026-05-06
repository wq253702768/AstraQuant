package okx

import "encoding/json"

type responseEnvelope struct {
	Code string          `json:"code"`
	Msg  string          `json:"msg"`
	Data json.RawMessage `json:"data"`
}

func (r responseEnvelope) DataObjects() ([]map[string]any, error) {
	var items []map[string]any
	if len(r.Data) == 0 {
		return items, nil
	}
	err := json.Unmarshal(r.Data, &items)
	return items, err
}

func (r responseEnvelope) DataArrays() ([][]any, error) {
	var items [][]any
	if len(r.Data) == 0 {
		return items, nil
	}
	err := json.Unmarshal(r.Data, &items)
	return items, err
}
