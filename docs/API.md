# REST API Reference

## Base URL
`http://localhost:8000/api/v1`

## Endpoints

- `POST /repositories` - Register a repository
- `POST /repositories/{id}/scan` - Trigger scanning and parsing
- `POST /repositories/{id}/index` - Trigger vector embedding generation
- `GET /search?q=query&type=hybrid` - Perform code/doc search
- `GET /graph?repo_id={id}` - Retrieve graph data
- `GET /timeline?repo_id={id}` - Retrieve repository event timeline
- `GET /technical-debt?repo_id={id}` - Get tech debt analysis
- `POST /assistant/chat` - Interact with AI assistant
