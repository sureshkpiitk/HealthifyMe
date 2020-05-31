from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import models

# Create your models here.


class Food(models.Model):
    name = models.CharField(max_length=32)


class Meal(models.Model):
    name = models.CharField(max_length=32)
    foods = models.ManyToManyField(Food, related_name='meal', db_index=True)


class Cuisines(models.Model):
    name = models.CharField(max_length=32)
    foods = models.ManyToManyField(Food, related_name='cuisines', db_index=True)


class Medical(models.Model):
    name = models.CharField(max_length=32)
    food = models.ManyToManyField(Food, related_name='medical', db_index=True, through='MedicalFood')


class MedicalFood(models.Model):
    medical_id = models.ForeignKey(Medical, db_index=True, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, db_index=True, on_delete=models.CASCADE, related_name='medical')
    is_good = models.NullBooleanField(default=None, help_text='True=> good, False=> bed, None=> no preference')


class Allergy(models.Model):
    name = models.CharField(max_length=32)
    foods = models.ManyToManyField(Food, related_name='good_allergy', db_index=True, through='AllergyFood')


class AllergyFood(models.Model):
    allergy_id = models.ForeignKey(Allergy, db_index=True, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, db_index=True, on_delete=models.CASCADE, related_name='allergy')
    is_good = models.NullBooleanField(default=None, help_text='True=> good, False=> bed, None=> no preference')


class UserFood(models.Model):
    user = models.ForeignKey(User, db_index=True, on_delete=models.CASCADE, related_name='like')
    food = models.ForeignKey(Food, db_index=True, on_delete=models.CASCADE, related_name='like')
    is_like = models.NullBooleanField(default=None, help_text='True=> like, False=> dislike, None=> no preference')


def get_cuisines_foods(cuisines):
    key = cuisines
    foods = cache.get(key, None)
    if foods:
        return foods
    else:
        foods = set(Food.objects.filter(cuisines__id=cuisines).values_list('id', flat=True))  # get foods list data for a particular cuisines from sheet
        cache.set(key, foods)
        return foods


def get_good_food_for_medical(medical):
    key = medical
    foods = cache.get(key, None)
    if foods:
        return foods
    else:
        foods = set(Food.objects.filter(medical__medical_id=medical, medical__is_good=True).values_list('id', flat=True))  # get good foods list data for a particular medical from sheet
        cache.set(key, foods)
        return foods


def get_bed_food_for_medical(medical):
    key = medical
    foods = cache.get(key, None)
    if foods:
        return foods
    else:
        foods = set(Food.objects.filter(medical__medical_id=medical, medical__is_good=False).values_list('id', flat=True))  # get bed foods list data for a particular medical from sheet
        cache.set(key, foods)
        return foods


def get_good_food_for_allergy(allergy):
    key = allergy
    foods = cache.get(key, None)
    if foods:
        return foods
    else:
        foods = set(Food.objects.filter(allergy__allergy_id=allergy, allergy__is_good=True).values_list('id', flat=True))  # get good foods list data for a particular allergy from sheet
        cache.set(key, foods)
        return foods


def get_bed_food_for_allergy(allergy):
    key = allergy
    foods = cache.get(key, None)
    if foods:
        return foods
    else:
        foods = set(Food.objects.filter(allergy__allergy_id=allergy, allergy__is_good=False).values_list('id', flat=True))  # get bed foods list data for a particular allergy from sheet
        cache.set(key, foods)
        return foods


def get_user_like_food(user_id):
    key = user_id
    foods = cache.get(key, None)
    if foods:
        return foods
    else:
        foods = set(Food.objects.filter(like__user_id=user_id, like__is_like=True).values_list('id', flat=True))
        cache.set(key, foods)
        return foods


def get_user_dislike_food(user_id):
    key = user_id
    foods = cache.get(key, None)
    if foods:
        return foods
    else:
        foods = set(Food.objects.filter(like__user_id=user_id, like__is_like=False).values_list('id', flat=True))
        cache.set(key, foods)
        return foods
