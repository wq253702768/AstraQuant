FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY services/exchange-access-gateway/go.mod services/exchange-access-gateway/go.sum ./
RUN go mod download
COPY services/exchange-access-gateway .
RUN go build -o exchange-access-gateway ./cmd/server

FROM alpine:3.20
WORKDIR /app
COPY --from=builder /app/exchange-access-gateway .
EXPOSE 8010
CMD ["./exchange-access-gateway"]
