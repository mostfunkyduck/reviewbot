#!/bin/sh

# this has to be scripted because initialization of the container errors
# out if you place it beforehand
cat > /var/lib/postgresql/data/postgresql.conf << CONFIG
listen_addresses = '*'
#log_min_messages = debug1
#log_min_error_statement = debug1
#log_min_duration_statement = 0
debug_pretty_print = on
#log_error_verbosity = verbose
#log_statement = 'all'
#client_min_messages = debug1
CONFIG
