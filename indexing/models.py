from django.db import models


class WIModel(models.Model):
  title       = models.CharField(max_length=250, blank=True, null=True)
  description = models.TextField(blank=True, null=True)

  link        = models.CharField(max_length=250)
  parse_links = models.TextField(blank=True, null=True)

  def __str__(self):
    return self.title[:30]
