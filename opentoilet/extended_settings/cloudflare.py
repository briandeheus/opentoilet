import os

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME", "opentoilet")
AWS_S3_ENDPOINT_URL = os.environ.get(
    "AWS_S3_ENDPOINT_URL",
    "https://0fa69ac4e65acedfe1787e8af58f1afd.r2.cloudflarestorage.com/opentoilet",
)
AWS_S3_CUSTOM_DOMAIN = os.environ.get(
    "AWS_S3_CUSTOM_DOMAIN", "cdn.opentoilet.xyz/opentoilet"
)
