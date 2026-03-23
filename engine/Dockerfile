FROM ubuntu:22.04

# Prevent interactive prompts during package install
ENV DEBIAN_FRONTEND=noninteractive

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    ca-certificates \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy the engine binary and make it executable
COPY seyoawe.linux ./seyoawe.linux
RUN chmod +x ./seyoawe.linux

# config.yaml expects paths relative to CWD (/app):
#   directories.modules   = ./seyoawe-community/modules
#   directories.workflows = ./seyoawe-community/workflows
#   directories.logs      = ./seyoawe-community/logs
#   directories.lifetimes = ./seyoawe-community/lifetimes
# Copy into that layout and pre-create the writable directories.
COPY modules/ ./seyoawe-community/modules/
COPY configuration/config.yaml ./configuration/config.yaml
COPY workflows/ ./seyoawe-community/workflows/
RUN mkdir -p ./seyoawe-community/logs ./seyoawe-community/lifetimes

# Engine runs on port 8080 (defined in configuration/config.yaml)
EXPOSE 8080

ENTRYPOINT ["./seyoawe.linux"]
