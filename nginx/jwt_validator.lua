local jwt = require "resty.jwt"
local validators = require "resty.jwt-validators"

-- Read secret from environment or config
local jwt_secret = os.getenv("JWT_SECRET") or "dev_secret_key_123"

-- Get Authorization header
local auth_header = ngx.var.http_Authorization

if not auth_header then
    ngx.status = 401
    ngx.say("{\"error\": \"Missing Authorization header\"}")
    ngx.exit(ngx.HTTP_UNAUTHORIZED)
end

-- Extract token (Bearer <token>)
local _, _, token = string.find(auth_header, "Bearer%s+(.+)")

if not token then
    ngx.status = 401
    ngx.say("{\"error\": \"Invalid Authorization header format\"}")
    ngx.exit(ngx.HTTP_UNAUTHORIZED)
end

-- Verify token
local jwt_obj = jwt:verify(jwt_secret, token)

if not jwt_obj.verified then
    ngx.status = 401
    ngx.say("{\"error\": \"Invalid or expired token: " .. jwt_obj.reason .. "\"}")
    ngx.exit(ngx.HTTP_UNAUTHORIZED)
end

-- Token is valid, pass to upstream
-- Optionally set a header with user ID from claims
if jwt_obj.payload and jwt_obj.payload.sub then
    ngx.req.set_header("X-User-Id", jwt_obj.payload.sub)
end
