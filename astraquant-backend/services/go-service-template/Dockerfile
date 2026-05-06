FROM golang:1.22-alpine AS build
WORKDIR /src
COPY services/go-service-template .
RUN go build -o /out/server ./cmd/server

FROM alpine:3.20
COPY --from=build /out/server /server
CMD ["/server"]
