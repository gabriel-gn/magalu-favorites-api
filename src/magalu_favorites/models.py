from django.utils import timezone
from django.db import models


class DefaultModel(models.Model):
    # por padrão também tem um campo 'id', que pode ser referenciado como 'pk' que é a primary key
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        if not self.created:
            self.created = timezone.now()

        self.modified = timezone.now()
        return super(DefaultModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True
        ordering = ['-created']