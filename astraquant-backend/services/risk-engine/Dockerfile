FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY services/risk-engine/go.mod services/risk-engine/go.sum ./
RUN go mod download
COPY services/risk-engine .
RUN go build -o risk-engine ./cmd/server
FROM alpine:3.20
WORKDIR /app
COPY --from=builder /app/risk-engine .
EXPOSE 8013
CMD ["./risk-engine"]
