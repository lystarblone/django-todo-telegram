from django.db import models, transaction
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

# Create your models here.
class IDSequence(models.Model):
    name = models.CharField(max_length=50, unique=True)
    last_id = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'id_sequences'

def get_next_id(sequence_name):
    with transaction.atomic():
        seq, created = IDSequence.objects.get_or_create(
            name=sequence_name,
            defaults={'last_id': 0}
        )
        seq.last_id += 1
        seq.save(update_fields=['last_id'])
        return seq.last_id

class BaseModel(models.Model):
    id = models.CharField(max_length=20, primary_key=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pk:
            counter = get_next_id(self._meta.model_name)
            self.id = f"{self._meta.model_name}_{str(counter).zfill(6)}"
        super().save(*args, **kwargs)

class CustomUser(AbstractUser, BaseModel):
    email = models.EmailField(unique=True)

    class Meta:
        db_table = 'auth_user'

class Category(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Task(BaseModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='tasks')
    categories = models.ManyToManyField(Category, blank=True)

    def __str__(self):
        return self.title