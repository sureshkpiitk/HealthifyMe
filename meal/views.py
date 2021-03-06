from django.db.models import Count
from django.shortcuts import render

# Create your views here.
from meal.models import get_cuisines_foods, get_good_food_for_medical, get_bed_food_for_medical, get_good_food_for_allergy, get_bed_food_for_allergy, \
    Meal, get_user_like_food, get_user_dislike_food


def get_meal(user_id, cuisines, medical, allergies):
    final_food_like = set()
    cuisines_food = set()
    for c in cuisines:
        cuisines_food += get_cuisines_foods(c)
    medical_good = set()
    medical_bed = set()

    for m in medical:
        medical_good += get_good_food_for_medical(m)
        medical_bed += get_bed_food_for_medical(m)
    allergies_good = set()
    allergies_bed = set()

    for a in allergies:
        allergies_good += get_good_food_for_allergy(a)
        allergies_bed += get_bed_food_for_allergy(a)

    user_like_food = get_user_like_food(user_id=user_id)
    user_dislike_food = get_user_dislike_food(user_id=user_id)

    final_food_like = final_food_like.union(allergies_good).union(cuisines_food).union(medical_good).union(user_like_food)
    final_list = final_food_like.difference(medical_bed).difference(allergies_bed).difference(user_dislike_food)
    meals = Meal.objects.filter(foods__id__in=final_list).annotate(total=Count('id')).order_by('-total')

    return meals[:10]
