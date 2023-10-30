# Calypte API

## How to start

1. run dev compose file
```bash
cd <to the root dir of the repo>
./scripts/dev up -d
```
2. create a poetry venv
```bash
cd backend/apps/calypte_api
poetry shell
```
3. install all service dependencies
```bash
poetry install
```
4. run the service
```bash
python calypte_api/main.py
```

## JWT TOKEN (TEST PURPOSE ONLY)

Payload:
```json
{
  "user": {
     "id": "0a8f4b9b-8056-468c-b44b-2dc4005d6ab4",
     "role": "user"
  },
  "access_jti": "5dc47ef6-7802-4dda-9c6c-de6db85ce27d",
  "refresh_jti": "821ee6e1-1d3b-4e0f-bb3b-4e22d0581a0f",
  "exp": 9999999999,
  "iat": 1516239022
}
```

secret_key:
```
f8de30b1c16146bf9c6c583ad2215e15f1d20338c6f65b416c36dee81ef4101d
```

JWT Token
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7ImlkIjoiMGE4ZjRiOWItODA1Ni00NjhjLWI0NGItMmRjNDAwNWQ2YWI0Iiwicm9sZSI6InVzZXIifSwiYWNjZXNzX2p0aSI6IjVkYzQ3ZWY2LTc4MDItNGRkYS05YzZjLWRlNmRiODVjZTI3ZCIsInJlZnJlc2hfanRpIjoiODIxZWU2ZTEtMWQzYi00ZTBmLWJiM2ItNGUyMmQwNTgxYTBmIiwiZXhwIjo5OTk5OTk5OTk5LCJpYXQiOjE1MTYyMzkwMjJ9.bzdUhudpXWfJSWUjJk3i32XOenKM5O5-hL4E_XpON_0
```
