FROM rust:latest
COPY src/ .
COPY static/ .
COPY Cargo.toml .
