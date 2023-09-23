from django_filters import rest_framework as filters


class IsUserFilterBackend(filters.BaseInFilter):
    """
    Filter that only allows users to get their own objects
    """
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(user_id=request.user)
