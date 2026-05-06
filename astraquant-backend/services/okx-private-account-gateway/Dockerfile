FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY services/okx-private-account-gateway/go.mod services/okx-private-account-gateway/go.sum ./
RUN go mod download
COPY services/okx-private-account-gateway .
RUN go build -o okx-private-account-gateway ./cmd/server
FROM alpine:3.20
WORKDIR /app
COPY --from=builder /app/okx-private-account-gateway .
EXPOSE 8017
CMD ["./okx-private-account-gateway"]
