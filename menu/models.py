from django.db import models

class Food(models.Model):
    name = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='foods/', blank=True, null=True)
    description = models.TextField(
        help_text="Short description (max 120 characters recommended)",
        blank=True
    )
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_available = models.BooleanField(default=True)
    
    def short_description(self):
        """Shortened version for displaying in cards"""
        return (self.description[:120] + '...') if len(self.description) > 120 else self.description
    
    def __str__(self):
        return self.name
