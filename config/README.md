# FinMkt configuration (your project)

Each installed package gets **its own INI file** under `config/application/<env>/`.
Every setting has a `;` comment above it describing what it does and how to use it.

| Path | Purpose |
|------|---------|
| `.env` | **Only** `FINMKT_ENV=dev` \| `qa` \| `prod` |
| `config/application/<env>/_core.ini` | Environment + config version |
| `config/application/<env>/<package>.ini` | That package's settings (safe in git) |
| `config/secrets/secrets.<env>.env` | API keys and PATs |

Legacy `*.yaml` / `config.<env>.ini` in this tree are still loaded if present.

```python
from finmkt.fastapi import create_app_from_settings, uvicorn_kwargs_from_settings
import uvicorn
app = create_app_from_settings()
uvicorn.run(app, **uvicorn_kwargs_from_settings())
```
