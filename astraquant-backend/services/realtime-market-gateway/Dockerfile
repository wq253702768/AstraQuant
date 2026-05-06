FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY services/realtime-market-gateway/go.mod services/realtime-market-gateway/go.sum ./
RUN go mod download
COPY services/realtime-market-gateway .
RUN go build -o realtime-market-gateway ./cmd/server

FROM alpine:3.20
WORKDIR /app
COPY --from=builder /app/realtime-market-gateway .
EXPOSE 8011
CMD ["./realtime-market-gateway"]
