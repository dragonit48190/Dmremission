from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .models import RoleMapping, User, UserRoleOverride


DM_GROUPS = [
    "SYSTEM_ADMIN",
    "NCD_ADMIN",
    "NCD_STAFF",
    "DOCTOR",
    "VIEWER",
]


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (
            "DM Remission",
            {
                "fields": (
                    "cid",
                    "hosxp_loginname",
                    "auth_provider",
                    "last_identity_verified_at",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    readonly_fields = (
        "created_at",
        "updated_at",
        "last_identity_verified_at",
    )

    list_display = (
        "username",
        "cid",
        "hosxp_loginname",
        "auth_provider",
        "is_active",
        "is_staff",
        "last_login",
    )

    list_filter = (
        "auth_provider",
        "is_active",
        "is_staff",
        "is_superuser",
    )

    search_fields = (
        "username",
        "cid",
        "hosxp_loginname",
        "first_name",
        "last_name",
        "email",
    )


@admin.register(RoleMapping)
class RoleMappingAdmin(admin.ModelAdmin):
    list_display = (
        "hosxp_groupname",
        "django_group",
        "is_active",
        "updated_at",
    )

    list_filter = (
        "is_active",
        "django_group",
    )

    search_fields = (
        "hosxp_groupname",
        "django_group__name",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "django_group":
            kwargs["queryset"] = Group.objects.filter(
                name__in=DM_GROUPS
            ).order_by("name")

        return super().formfield_for_foreignkey(
            db_field,
            request,
            **kwargs
        )


@admin.register(UserRoleOverride)
class UserRoleOverrideAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "django_group",
        "is_active",
        "created_by",
        "updated_by",
        "updated_at",
    )

    list_filter = (
        "is_active",
        "django_group",
    )

    search_fields = (
        "user__username",
        "user__cid",
        "user__hosxp_loginname",
        "django_group__name",
        "reason",
    )

    readonly_fields = (
        "created_by",
        "updated_by",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "การกำหนดสิทธิ์",
            {
                "fields": (
                    "user",
                    "django_group",
                    "reason",
                    "is_active",
                )
            },
        ),
        (
            "Audit",
            {
                "fields": (
                    "created_by",
                    "updated_by",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):

        if db_field.name == "django_group":
            kwargs["queryset"] = Group.objects.filter(
                name__in=DM_GROUPS
            ).order_by("name")

        if db_field.name == "user":
            kwargs["queryset"] = User.objects.filter(
                auth_provider=User.AuthProvider.THAID,
                is_superuser=False,
            ).order_by("username")

        return super().formfield_for_foreignkey(
            db_field,
            request,
            **kwargs
        )

    def save_model(self, request, obj, form, change):

        if not obj.pk:
            obj.created_by = request.user

        obj.updated_by = request.user

        super().save_model(
            request,
            obj,
            form,
            change
        )