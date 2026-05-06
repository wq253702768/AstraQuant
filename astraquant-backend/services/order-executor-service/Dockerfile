FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY services/order-executor-service/go.mod services/order-executor-service/go.sum ./
RUN go mod download
COPY services/order-executor-service .
RUN go build -o order-executor-service ./cmd/server
FROM alpine:3.20
WORKDIR /app
COPY --from=builder /app/order-executor-service .
EXPOSE 8018
CMD ["./order-executor-service"]
