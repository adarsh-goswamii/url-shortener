class DBTables:
    URLS                    = "urls"
    CUSTOM_ALIAS            = "custom_alias"

class  DBConfig:
    SCHEMA_NAME = "url_shortener"
    BASE_ARGS   = { "schema": SCHEMA_NAME }

class RedisKeyCategory:
    URLS = "urls"
    RATE_LIMIT = "rate_limit"

class RedisKeyScope:
    SHORTEN_URL = "shorten_url"

class ApiRateLimit:
    SHORTEN_URL_ANONYMOUS = 10
    SHORTEN_URL_USER = 100