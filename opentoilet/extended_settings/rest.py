REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "opentoilet.utils.pagination.OpenToiletPagination",
    "DEFAULT_FILTER_BACKENDS": "django_filters.rest_framework.DjangoFilterBackend",
    "PAGE_SIZE": 20,
}
