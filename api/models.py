from django.db import models


class Setting(models.Model):
    bot_link = models.CharField(max_length=250)
    api_id = models.CharField(max_length=250)
    api_hash = models.CharField(max_length=250)

    class Meta:
        verbose_name = "Настройки"
        verbose_name_plural = "Настройки"

    def __str__(self):
        return "Настройки"


class Account(models.Model):
    name = models.CharField(max_length=250)
    phone_code_hash = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Аккаунт"
        verbose_name_plural = "Аккаунты"

    def __str__(self):
        return self.name


class Result(models.Model):
    number = models.CharField(max_length=250, unique=True)
    text = models.TextField()
    file = models.FileField(blank=True, null=True, upload_to="media")

    class Meta:
        verbose_name = "Результат"
        verbose_name_plural = "Результаты"

    def __str__(self):
        return self.number
