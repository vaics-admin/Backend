"""Flask configuration."""

import os

SECRET_KEY = os.urandom(24)
SQLALCHEMY_DATABASE_URI = "postgresql://avnadmin:AVNS_LxntLC6YcMGA7CYaR5o@pg-2ac3c26a-hrms-b7f6.h.aivencloud.com:19580/defaultdb"

