# JSON Parser CLI v0.3.2

## Features
- Pretty/Minify JSON
- Get/Set paths
- Find by key
- Query with JMESPath or JSONPath
- Docker + docker-compose support

## Usage
```bash
jsoncli pretty file.json
jsoncli query file.json --jmes "b[].x"
jsoncli query file.json --jsonpath "$.b[*].x"
```
