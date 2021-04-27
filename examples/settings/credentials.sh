
# Cast bash configuration and credentials
# Contact: <Your-Email-Here>

# The engine defaults to a folder in /opt for its state.
# For HPC this is likely unavailable.
# Ideally, set this to a user-specific dir, such as "/tmp/<Your-User>"
export ENGINE_CACHE_DIR="/some-folder"
export ENGINE_TEMP_DIR="/some-folder"

# Flywheel SDK settings
export FLYWHEEL_SDK_SKIP_VERSION_CHECK="1"

# Flywheel site credentials
export SCITRAN_RUNTIME_HOST="<your-hostname>"
export SCITRAN_RUNTIME_PORT="443"
export SCITRAN_CORE_DRONE_SECRET="<your-credentials>"

# Disable metrics server
export ENGINE_METRICS_PORT=-1

# Enable signed URLs
export ENGINE_SIGNED_URLS=1

# HPC compatible compute
export ENGINE_MODULE=singularity

# Do NOT put other engine settings in this file.
