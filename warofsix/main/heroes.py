from django.shortcuts import get_object_or_404
from .models import Heroes, UserHeroes, Resources, Race
from django.utils import timezone


class HeroManagement():
    
    def __init__(self, user):
        self.user = user
    

    def hero_market_list(self):
        user_race = Race.objects.get(user=self.user).name
        heroes = Heroes.objects.filter(race = user_race).exclude(rings__gt=0).order_by('token')
        ring_hero = Heroes.objects.get(race=user_race, rings__gt=0)
        one_ring_hero_race = "Good" if user_race in ["Men", "Elves","Dwarves"] else "Evil"
        one_ring_hero = Heroes.objects.get(race= one_ring_hero_race, the_one_ring = True)
        return heroes, ring_hero, one_ring_hero
    
    def user_hero_list(self):
        user_heroes = UserHeroes.objects.filter(user = self.user).order_by('current_health')
        if user_heroes.exists():
            return user_heroes
        else:
            return []
    
    def buy_hero_check(self, hero_id):
        user_heroes = UserHeroes.objects.filter(user = self.user)
        hero = Heroes.objects.get(id = hero_id)
        # Hero number check, MAX 3 allowed
        if len(user_heroes) > 2:
            return False, "You may get maximum 3 heroes !", hero
        elif hero_id in [user_hero.hero.id for user_hero in user_heroes]:
            return False, "You already have this hero !", hero
        elif hero.token > Resources.objects.get(user = self.user).token:
            return False, "You do not enough Token for this hero !", hero
        elif hero not in [ hero for hero in self.hero_market_list()][0]:
            return False, "Do not try to get another race's hero pls...", hero
        else:
            return True, f"You got the {hero.name}", hero
    
    def get_hero(self, hero_id):
        check, message, hero = self.buy_hero_check(hero_id)
        if not check:
            return message
        else:
            UserHeroes.objects.create(
                user = self.user,
                hero = hero
            )
            user_resources = Resources.objects.get(user=self.user)
            user_resources.token -= hero.token
            user_resources.save()
            return message
    
    def get_ring_hero(self, hero_id):
        hero = Heroes.objects.get(id = hero_id)
        if hero.rings > Resources.objects.get(user=self.user).rings:
            return "You do not have enough rings. Try to get them by attacking the wild places."
        elif UserHeroes.objects.filter(hero=hero).exists():
            return "You already have this Ring Hero"
        elif hero not in self.hero_market_list():
            return "Every race have their own Ring Hero. Don't be greedy."
        else:
            UserHeroes.objects.create(
                user=self.user,
                hero=hero
            )
            return f"You have the {hero.name}"
    
    def get_one_ring_hero(self, hero_id):
        one_ring_hero = get_object_or_404(Heroes, id=hero_id)
        race_tree = {"Good": ["Men","Elves","Dwarves"], "Evil": ["Mordor", "Isengard", "Goblins"]}
        user_race = Race.objects.get(user=self.user).name
        
        user_resources = Resources.objects.get(user=self.user)
        if not user_resources.the_one_ring:
            return "Get the One Ring first!"
        elif one_ring_hero in [hero.hero for hero in self.user_hero_list()]:
            return "You already have it!"
        elif not user_race in race_tree[one_ring_hero.race]:
            return "You can not get the other side's hero. Don't be greedy"
        else:
            UserHeroes.objects.create(
                user=self.user,
                hero = one_ring_hero
            )
            return f"We have the {one_ring_hero}!!! HAHAHAHAHAHHAHAHA"
        



    def return_hero(self, user_hero_id):
        # check if you really have the hero
        if UserHeroes.objects.filter(user=self.user, id = user_hero_id).exists():
            user_hero = UserHeroes.objects.get(id = user_hero_id)
            if user_hero.hero.rings > 0:
                rings = user_hero.hero.rings
                user_resources = Resources.objects.get(user = self.user)
                user_resources.rings += round(rings / 2)
                user_resources.save()
                user_hero.delete()
                return "Ring Hero is returned for harf price."
            
            if user_hero.hero.the_one_ring:
                return "You can not return the ONE RING HERO"
            token = user_hero.hero.token
            user_resources = Resources.objects.get(user=self.user)
            user_resources.token += round(token / 2)
            message = f"{user_hero.hero} is returned for {token / 2} token."
            user_resources.save()
            user_hero.delete()
            return message
        else:
            return "Sorry, an Error accured !"
    
    def revival_hero(self, user_hero_id):
        if UserHeroes.objects.filter(user=self.user, id = user_hero_id).exists():
            user_hero = UserHeroes.objects.get(id = user_hero_id)
            if not user_hero.is_dead:
                return "He/she is not dead yet!"
            elif user_hero.hero.the_one_ring:
                user_resources = Resources.objects.get(user=self.user)
                if user_resources.the_one_ring:
                    user_hero.regenerate_time_left = user_hero.hero.regenerate_time
                    user_hero.save()
                    return "Hero revives"

                else:
                    return "Did you lost the Ring !?"
                    
            
            elif user_hero.hero.rings != 0:
                user_resources = Resources.objects.get(user=self.user)
                if all([user_resources.wood >= 10000, user_resources.stone >= 10000, user_resources.iron >= 10000, user_resources.grain >= 10000, user_resources.rings >= user_hero.hero.rings]):
                    user_hero.regenerate_time_left = user_hero.hero.regenerate_time
                    user_hero.save()
                    user_resources.wood -= 10000
                    user_resources.stone -= 10000
                    user_resources.iron -= 10000
                    user_resources.grain -= 10000
                    user_resources.save()
                    return f"{user_hero.hero} revives"
                else:
                    return "Not enough resources"

            else:
                user_resources = Resources.objects.get(user=self.user)
                if all([user_resources.wood >= 7500, user_resources.stone >= 7500, user_resources.iron >= 7500, user_resources.grain >= 7500]):
                    user_hero.regenerate_time_left = user_hero.hero.regenerate_time
                    user_hero.save()
                    user_resources.wood -= 7500
                    user_resources.stone -= 7500
                    user_resources.iron -= 7500
                    user_resources.grain -= 7500
                    user_resources.save()
                    return f"{user_hero.hero} revives"
                else:
                    return "Not enough resources!"
        else:
            return "Soryy, an Error accured"
        


    def refresh_heroes_health(self):
        user_heroes = UserHeroes.objects.filter(user=self.user)
        for user_hero in user_heroes:
            if user_hero.is_dead:
                time_difference = (timezone.now() - user_hero.last_checkout).total_seconds()
                if user_hero.regenerate_time_left != 0 and time_difference > user_hero.regenerate_time_left:
                    user_hero.is_dead = False
                    user_hero.last_checkout = timezone.now()
                    user_hero.regenerate_time_left = 0
                    user_hero.save()
                elif user_hero.regenerate_time_left != 0:
                    user_hero.regenerate_time_left -= time_difference
                    user_hero.last_checkout = timezone.now()
                    user_hero.save()
                else:
                    pass
                
            elif user_hero.current_health == user_hero.hero.health:
                pass
            else:
                time_difference = (timezone.now() - user_hero.last_checkout).total_seconds()
                if user_hero.current_health + time_difference > user_hero.hero.health:
                    user_hero.current_health = user_hero.hero.health
                    user_hero.last_checkout = timezone.now()
                    user_hero.save()
                else:
                    user_hero.current_health += time_difference
                    user_hero.last_checkout = timezone.now()
                    user_hero.save()
        




