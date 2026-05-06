FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY services/live-risk-guard-service/go.mod services/live-risk-guard-service/go.sum ./
RUN go mod download
COPY services/live-risk-guard-service .
RUN go build -o live-risk-guard-service ./cmd/server
FROM alpine:3.20
WORKDIR /app
COPY --from=builder /app/live-risk-guard-service .
EXPOSE 8019
CMD ["./live-risk-guard-service"]
