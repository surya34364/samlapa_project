from finmkt.fastapi import app_config_from_settings

config = app_config_from_settings()
origin_regex = config.cors_allow_origin_regex
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:Surya27710@localhost/samlapa_db"