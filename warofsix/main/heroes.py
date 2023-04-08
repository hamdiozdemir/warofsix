from .models import Heroes, UserHeroes, Resources, Race
from django.utils import timezone


class HeroManagement():
    
    def __init__(self, user):
        self.user = user
    

    def hero_market_list(self):
        user_race = Race.objects.get(user=self.user).name
        heroes = Heroes.objects.filter(race = user_race).order_by('token')
        return heroes
    
    def user_hero_list(self):
        user_heroes = UserHeroes.objects.filter(user = self.user).order_by('current_health')
        if user_heroes.exists():
            return user_heroes
        else:
            return None
    
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

    def return_hero(self, user_hero_id):
        # check if you really have the hero
        if UserHeroes.objects.filter(user=self.user, id = user_hero_id).exists:
            user_hero = UserHeroes.objects.get(id = user_hero_id)
            token = user_hero.hero.token
            user_resources = Resources.objects.get(user=self.user)
            user_resources.token += token / 2
            message = f"{user_hero.hero} is returned for {token / 2} token."
            user_resources.save()
            user_hero.delete()
            return message
        else:
            return "Sorry, an Error accured !"
    
    def revival_hero(self, user_hero_id):
        if UserHeroes.objects.filter(user=self.user, id = user_hero_id).exists:
            user_hero = UserHeroes.objects.get(id = user_hero_id)
            if not user_hero.is_dead:
                return "He/she is not dead yet!"
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
                if time_difference > user_hero.regenerate_time_left:
                    user_hero.is_dead = False
                    user_hero.last_checkout = timezone.now()
                    user_hero.regenerate_time_left = 0
                    user_hero.save()
                else:
                    user_hero.regenerate_time_left -= time_difference
                    user_hero.last_checkout = timezone.now()
                    user_hero.save()
                
            if user_hero.current_health == user_hero.hero.health:
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
        




