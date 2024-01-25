#!/bin/bash
export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/postgres"
export TEST_DATABASE_URL="postgresql://postgres:postgres@localhost:5432/postgres_test"

export AUTH0_DOMAIN="dev-630svhk4fe35vgq3.us.auth0.com"
export ALGORITHMS="RS256"
export API_AUDIENCE="coffees"

echo "setup.sh script executed successfully!"