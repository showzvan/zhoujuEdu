from django.db import models

from school.models import Schools
from major.models import Majors
from user.models import Users


class Orders(models.Model):
    STATUS_LIST = (
        ('wfk', "未付款"),
        ('yfk', "已付款"),
        ('ylq', "已录取"),
        ('ysx', "已失效"),
    )
    real_name = models.CharField("真实姓名", max_length=255, null=False)
    idcard = models.CharField("身份证号", max_length=18, null=False)
    phone = models.CharField("电话", max_length=255)
    create_time = models.DateTimeField("创建时间",null=True)
    # price = models.CharField("价格")
    majar_id = models.ForeignKey('major.Majors', verbose_name="专业id", on_delete=models.DO_NOTHING)
    school_id = models.ForeignKey('school.Schools',verbose_name='院校id', on_delete=models.DO_NOTHING)
    user_id = models.ForeignKey('user.Users',verbose_name="用户id", on_delete=models.DO_NOTHING)
    status = models.CharField("付款录取状态", max_length=3, choices=STATUS_LIST, default='wfk')
    is_status = models.BooleanField("状态", default=True)  # true 可用  false 不可用


    class Meta:
        verbose_name = "报名订单信息"
        verbose_name_plural = verbose_name
        db_table = "zhouju_orders"
