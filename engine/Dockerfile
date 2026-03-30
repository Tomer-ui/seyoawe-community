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

# config.yaml paths are relative to CWD (/app):
#   directories.modules   = ./modules
#   directories.workflows = ./workflows
#   directories.logs      = ./logs
#   directories.lifetimes = ./lifetimes
COPY modules/ ./modules/
COPY configuration/config.yaml ./configuration/config.yaml
COPY workflows/ ./workflows/
RUN mkdir -p ./logs ./lifetimes

# Engine runs on port 8080 (defined in configuration/config.yaml)
EXPOSE 8080

ENTRYPOINT ["./seyoawe.linux"]
