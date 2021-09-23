#!/bin/sh

# Copy Docker container environment
# to ensure is passed into the cron sub-processes
env >> /etc/environment

# Start cron
cron -l 2

# execute CMD
echo "$@"
exec "$@"
