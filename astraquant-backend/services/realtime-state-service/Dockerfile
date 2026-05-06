FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY services/realtime-state-service/go.mod services/realtime-state-service/go.sum ./
RUN go mod download
COPY services/realtime-state-service .
RUN go build -o realtime-state-service ./cmd/server
FROM alpine:3.20
WORKDIR /app
COPY --from=builder /app/realtime-state-service .
EXPOSE 8012
CMD ["./realtime-state-service"]
