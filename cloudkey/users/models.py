from django.db import models


class InfoCard(models.Model):
    user_id = models.IntegerField("ID пользователя")
    icon = models.TextField("Иконка сайта")
    url = models.TextField("URL сайта")
    email = models.TextField("Email")
    password = models.CharField("Пароль", max_length=100)

    def __str__(self):
        return self.url

    class Meta:
        verbose_name = "Карточка с паролем"
        verbose_name_plural = "Карточки с паролем"
