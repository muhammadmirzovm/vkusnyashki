from django.db import models


class Monitor(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)
    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=200)
    bg_image = models.ImageField(upload_to="categories/", blank=True, null=True)
    monitor = models.ForeignKey(
        Monitor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='categories'   
    )
    order = models.PositiveSmallIntegerField(default=0, help_text="Display order")

    class Meta:
        ordering = ("order", "name")

    def __str__(self):
        return self.name


class Food(models.Model):
    name = models.CharField(max_length=200)
    photo = models.ImageField(upload_to="foods/", blank=True, null=True)
    description = models.TextField(
        help_text="Short description (max 120 characters recommended)", blank=True
    )
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='foods')

    def short_description(self):
        """Shortened version for displaying in cards"""
        return (
            (self.description[:120] + "...")
            if len(self.description) > 120
            else self.description
        )

    def __str__(self):
        return self.name
