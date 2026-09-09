from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):

    class AuthProvider(models.TextChoices):
        LOCAL = "LOCAL", "Local"
        THAID = "THAID", "ThaID"

    cid = models.CharField(
        "เลขประจำตัวประชาชน",
        max_length=13,
        unique=True,
        null=True,
        blank=True,
        db_index=True,
        validators=[
            RegexValidator(
                regex=r"^\d{13}$",
                message="เลขประจำตัวประชาชนต้องเป็นตัวเลข 13 หลัก",
            )
        ],
    )

    hosxp_loginname = models.CharField(
        "HOSxP Login",
        max_length=100,
        blank=True,
    )

    auth_provider = models.CharField(
        "Authentication Provider",
        max_length=10,
        choices=AuthProvider.choices,
        default=AuthProvider.LOCAL,
    )

    last_identity_verified_at = models.DateTimeField(
        "ยืนยันตัวตนล่าสุด",
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        "วันที่สร้าง",
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        "วันที่แก้ไข",
        auto_now=True,
    )

    def __str__(self):
        return self.username


class RoleMapping(models.Model):

    hosxp_groupname = models.CharField(
        "กลุ่มผู้ใช้ HOSxP",
        max_length=100,
        unique=True,
    )

    django_group = models.ForeignKey(
        "auth.Group",
        on_delete=models.PROTECT,
        related_name="dmremission_role_mappings",
        verbose_name="สิทธิ์ DM Remission",
    )

    is_active = models.BooleanField(
        "ใช้งาน",
        default=True,
    )

    created_at = models.DateTimeField(
        "วันที่สร้าง",
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        "วันที่แก้ไข",
        auto_now=True,
    )

    class Meta:
        verbose_name = "การจับคู่สิทธิ์ HOSxP"
        verbose_name_plural = "การจับคู่สิทธิ์ HOSxP"
        ordering = ["hosxp_groupname"]

    def __str__(self):
        return f"{self.hosxp_groupname} → {self.django_group.name}"

class UserRoleOverride(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="role_override",
        verbose_name="ผู้ใช้งาน",
    )

    django_group = models.ForeignKey(
        "auth.Group",
        on_delete=models.PROTECT,
        related_name="dmremission_user_overrides",
        verbose_name="สิทธิ์ที่กำหนด",
    )

    reason = models.CharField(
        "เหตุผลในการกำหนดสิทธิ์",
        max_length=255,
        blank=True,
    )

    is_active = models.BooleanField(
        "ใช้งาน",
        default=True,
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_role_overrides",
        verbose_name="สร้างโดย",
    )

    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="updated_role_overrides",
        verbose_name="แก้ไขล่าสุดโดย",
    )

    created_at = models.DateTimeField(
        "วันที่สร้าง",
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        "วันที่แก้ไข",
        auto_now=True,
    )

    class Meta:
        verbose_name = "กำหนดสิทธิ์รายบุคคล"
        verbose_name_plural = "กำหนดสิทธิ์รายบุคคล"
        ordering = ["user__username"]

    def __str__(self):
        return f"{self.user.username} → {self.django_group.name}"    