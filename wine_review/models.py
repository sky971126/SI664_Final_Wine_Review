# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.urls import reverse
from django.db.models import Q

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, on_delete=models.PROTECT)
    permission = models.ForeignKey('AuthPermission', on_delete=models.PROTECT)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', on_delete=models.PROTECT)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, on_delete=models.PROTECT)
    group = models.ForeignKey(AuthGroup, on_delete=models.PROTECT)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, on_delete=models.PROTECT)
    permission = models.ForeignKey(AuthPermission, on_delete=models.PROTECT)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Country(models.Model):
    country_id = models.AutoField(primary_key=True)
    country_name = models.CharField(unique=True, max_length=60)

    class Meta:
        managed = False
        db_table = 'country'
        ordering = ['country_name']
        verbose_name = 'country'
        verbose_name_plural = 'countries'

    def __str__(self):
        return self.country_name


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', on_delete=models.PROTECT, blank=True, null=True)
    user = models.ForeignKey(AuthUser, on_delete=models.PROTECT)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Province(models.Model):
    province_id = models.AutoField(primary_key=True)
    province_name = models.CharField(unique=True, max_length=60)
    country = models.ForeignKey(Country, on_delete=models.PROTECT)

    class Meta:
        managed = False
        db_table = 'province'
        ordering = ['province_name']
        verbose_name = 'province'
        verbose_name_plural = 'provinces'

    def __str__(self):
        return self.province_name


class Region(models.Model):
    region_id = models.AutoField(primary_key=True)
    region_name = models.CharField(unique=True, max_length=60)
    province = models.ForeignKey(Province, on_delete=models.PROTECT)

    class Meta:
        managed = False
        db_table = 'region'
        ordering = ['region_name']
        verbose_name = 'region'
        verbose_name_plural = 'regions'

    def __str__(self):
        return self.region_name


class Taster(models.Model):
    taster_id = models.AutoField(primary_key=True)
    taster_name = models.CharField(unique=True, max_length=60)
    taster_twitter = models.CharField(max_length=60, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'taster'
        ordering = ['taster_name']
        verbose_name = 'taster'
        verbose_name_plural = 'tasters'

    def __str__(self):
        return self.taster_name



class WineVariety(models.Model):
    wine_variety_id = models.AutoField(primary_key=True)
    wine_variety_name = models.CharField(unique=True, max_length=60)

    class Meta:
        managed = False
        db_table = 'wine_variety'
        ordering = ['wine_variety_name']
        verbose_name = 'variety'
        verbose_name_plural = 'varieties'

    def __str__(self):
        return self.wine_variety_name

class Winery(models.Model):
    winery_id = models.AutoField(primary_key=True)
    winery_name = models.CharField(unique=True, max_length=60)

    class Meta:
        managed = False
        db_table = 'winery'
        ordering = ['winery_name']
        verbose_name = 'winery'
        verbose_name_plural = 'wineries'

    def __str__(self):
        return self.winery_name


class WineReview(models.Model):
    taster_wine_id = models.AutoField(primary_key=True)
    taster = models.ForeignKey(Taster, on_delete=models.CASCADE, blank=True, null=True)
    wine = models.ForeignKey('Wine', on_delete=models.CASCADE)
    description = models.CharField(max_length=500)
    rating = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'taster_wine'
        ordering = ['wine','taster']
        verbose_name = 'wine review'
        verbose_name_plural = 'wine reviews'
    
    def __str__(self):
        return str(self.rating) + " " + self.description


class Wine(models.Model):
    wine_id = models.AutoField(primary_key=True)
    wine_title = models.CharField(unique=True, max_length=100)
    wine_variety = models.ForeignKey(WineVariety, on_delete=models.PROTECT)
    winery = models.ForeignKey(Winery, on_delete=models.PROTECT)
    region = models.ForeignKey(Region, on_delete=models.PROTECT, blank=True, null=True)
    province = models.ForeignKey(Province, on_delete=models.PROTECT, blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, blank=True, null=True)

    taster = models.ManyToManyField(Taster, through='WineReview')

    class Meta:
        managed = False
        db_table = 'wine'
        ordering = ['wine_title']
        verbose_name = 'wine title'
        verbose_name_plural = 'wine titles'
    
    def __str__(self):
        return self.wine_title

    def get_absolute_url(self):
        return reverse('wine_detail', kwargs={'pk': self.pk})
    
    def get_wine_review(self):
        return WineReview.objects.all().filter(Q(wine_id=self.wine_id))


