from django.db import models

# Create your models here.

class Supply(models.Model):
    product_name = models.CharField(max_length=500)  
    category_choices = (
        ('pot', '화분'),
        ('fertilizer', '비료'),
        ('nutrition', '영양제'),
        ('decoration', '데코레이션'),
        ('sprinkler', '물뿌리개'),
    )
    category = models.CharField(max_length=20, choices=category_choices) 
    like = models.PositiveIntegerField(default=0)  
    price = models.IntegerField()
    # tag_choices = (
    #     ('expensive', '비싸다'),
    #     ('affordable', '싸다'),
    #     ('bright', '밝다'),
    #     ('dark', '어둡다'),
    #     ('fast_shipping', '빠른배송'),
    #     ('slow_shipping', '느린배송'),
    # )
    # tags = models.CharField(max_length=100, choices=tag_choices) 

    def save(self, *args, **kwargs):
        self.tags = ','.join(self.tags)

        super().save(*args, **kwargs)

    def get_tags_list(self):
        return self.tags.split(',')