from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='category', blank=True, null=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=50)
    intro = models.TextField()
    cover = models.ImageField(upload_to='article')
    published = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)
    read_time = models.PositiveIntegerField(help_text="O‘qish vaqti (daqiqa)")
    author = models.CharField(max_length=30)
    important = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True, blank=True, null=True)

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    tag = models.ManyToManyField(Tag,blank=True)


    def __str__(self):
        return self.title

    def save(self,*args, **kwargs):
        if self.important:
            Article.objects.exclude(pk=self.pk).update(important=False)
        super().save(*args, **kwargs)


class Context(models.Model):
    text = models.TextField()
    image = models.ImageField(upload_to='context', blank=True, null=True)

    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.article.title if self.article else "No article"


class Comment(models.Model):
    text = models.TextField()
    author = models.CharField(max_length=30)
    email = models.EmailField()
    published = models.BooleanField(default=False)

    created_at = models.DateField(auto_now_add=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    def __str__(self):
        return self.text[:20]


class Contact(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    seen = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Newsletter(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateField(auto_now_add=True)
