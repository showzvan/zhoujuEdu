from django.db import models

# 友情链接
class Links(models.Model):
    link_title = models.CharField("友情链接名称", max_length=255, null=False)
    url = models.URLField("友情链接地址")
    is_status = models.BooleanField("状态", default=True)  # true 可用  false 不可用

    class Meta:
        verbose_name = "友情链接"
        verbose_name_plural = verbose_name
        db_table = "zhouju_links"




# 首页地区表
class Regions(models.Model):
    # IS_STATUS = (
    #     (0, '不可用'),
    #     (1, '可用'),
    # )
    # IS_HOT = (
    #     (0,'否'),
    #     (1,'是'),
    # )
    cityname = models.CharField("城市名称", null=False,max_length=255)
    initials = models.CharField("首字母", null=False, default='A',max_length=10)
    is_hot = models.BooleanField("是否热门", default=False)  # True 热门 False 非热门
    is_status = models.BooleanField("是否可用", default=True)  # True 可用  False 不可用

    class Meta:
        verbose_name = "首页地区表"
        verbose_name_plural = verbose_name
        db_table = "zhouju_regions"
