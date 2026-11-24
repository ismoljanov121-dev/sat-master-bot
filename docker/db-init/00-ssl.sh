#!/bin/sh
set -e

openssl req -new -x509 -days 3650 -nodes \
  -out "$PGDATA/server.crt" \
  -keyout "$PGDATA/server.key" \
  -subj "/CN=sat-master-local-pg"

chmod 600 "$PGDATA/server.key"
chown postgres:postgres "$PGDATA/server.key" "$PGDATA/server.crt"

printf "\nssl = on\nssl_cert_file = 'server.crt'\nssl_key_file = 'server.key'\n" >> "$PGDATA/postgresql.conf"
