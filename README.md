# Compound CLI
### Description

This is a CLI tool to fetch and display compound info
from open compound API provided by
EMBL's European Bioinformatics Institute.

### Usage
Fetching entries from remote API:
```shell
$ python -m compound sync ADP
```

Displaying fetched data:
```shell
$ python -m compound show
# or
$ python -m compound show ADP
```

### Deployment
```shell
# Start services
$ docker compose up -d
# Run a shell inside CLI service
$ docker exec -it compound_cli /bin/sh
# After that you may run the CLI inside the shell
$ ...
# Stop services
$ docker compose down
```
