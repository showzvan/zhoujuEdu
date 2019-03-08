from django.db import models

# 验证码表
class VerifyCode(models.Model):
    mobile = models.CharField("手机", max_length=11, null=True)
    code = models.CharField("验证码", max_length=4, null=True)


    class Meta:
        verbose_name = "验证码表"
        verbose_name_plural = verbose_name
        db_table = "zhouju_code"
