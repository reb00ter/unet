from autoslug import AutoSlugField
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models


# Create your models here.
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit


class StoreBrand(models.Model):
    title = models.CharField(verbose_name="название", max_length=100)
    slug = AutoSlugField(populate_from=title, blank=True, editable=True, verbose_name="адрес страницы", help_text="если оставить пустым - сгенерируется автоматически")
    logo = models.ImageField(verbose_name="логотип", upload_to="logos")
    logo_thumb = ImageSpecField(source='logo',
                                processors=[ResizeToFit(150, 150)],
                                format='PNG')
    website = models.URLField(verbose_name="адрес сайта", null=True, blank=True)
    description = RichTextField(verbose_name="описание", null=True, blank=True)

    def __str__(self):
        return self.title


class StoreLocation(models.Model):
    store_brand = models.ForeignKey(StoreBrand, verbose_name="название магазина")
    sub_title = models.CharField(verbose_name="название торговой точки", max_length=100, null=True, blank=True)
    address = models.TextField(verbose_name="адрес")
    longitude = models.FloatField(verbose_name="долгота", null=True, blank=True)
    latitude = models.FloatField(verbose_name="широта", null=True, blank=True)
    description = RichTextField(verbose_name="описание", null=True, blank=True)

    def __str__(self):
        if self.sub_title:
            return self.store_brand.title+", "+self.sub_title
        else:
            return self.store_brand.title+", "+self.address


class StoreAdmin(models.Model):
    store_brand = models.ForeignKey(StoreBrand, verbose_name="название магазина")
    user = models.ForeignKey(User, verbose_name="пользователь")

    def __str__(self):
        return self.store_brand.title+", "+self.user.username


class Category(models.Model):
    parent = models.ForeignKey("Category", null=True, blank=True)
    title = models.CharField(verbose_name="название", max_length=50)
    weight = models.PositiveSmallIntegerField(verbose_name="вес", default=0)

    def __str__(self):
        return self.title

    def children(self):
        return Category.objects.filter(parent=self).order_by("weight")

    class Meta:
        verbose_name = "категория товара"
        verbose_name_plural = "категории товаров"
        ordering = ["weight",]


class StoreCategory(models.Model):
    store_brand = models.ForeignKey(StoreBrand)
    store_category_id = models.PositiveIntegerField(verbose_name="id категории в системе магазина")
    store_category_title = models.PositiveIntegerField(verbose_name="название категории в системе магазина")
    our_category = models.ForeignKey(Category, verbose_name="категория на сайте", null=True)


class Image(models.Model):
    image = models.ImageField(verbose_name="изображение товара", upload_to="goods")
    image_thumb = ImageSpecField(source='image',
                                 processors=[ResizeToFit(200, 200)],
                                 format='PNG')


class Item(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(verbose_name="название", max_length=255)
    price = models.FloatField(verbose_name="цена", blank=True, null=True)
    store = models.ForeignKey(StoreBrand, verbose_name="магазин")
    images = models.ManyToManyField(Image, verbose_name="изображения товара")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"

