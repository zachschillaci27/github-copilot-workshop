---
applyTo: "src/taskflow/routers/**/*.py"
description: FastAPI router conventions
---

# Router Conventions

- Mount routers under `/api/v1/` in `src/taskflow/main.py`.
- Handlers stay thin: validate with Pydantic, delegate to `database.py`,
  translate not-found into `HTTPException(status_code=404, detail=...)`.
- Return status codes explicitly via the `status_code=` kwarg on the route
  decorator — 201 for `POST`, 204 for `DELETE`, 200 otherwise.
- Filtering goes through query parameters, never a request body on `GET`.
- Every new route gets a docstring used by the FastAPI OpenAPI schema.
