from pathlib import Path

from app.clients import redis_client

lua_path=Path(__file__).parent.parent / "scripts" / "rate_limit.lua"
with open(lua_path, "r") as f:
    rate_limit_lua = f.read()

rate_limiter = redis_client.register_script(rate_limit_lua)