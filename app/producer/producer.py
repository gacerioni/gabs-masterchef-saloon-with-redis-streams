import os
import sys

import redis
from random import choice, randint
from time import sleep
# This computes the absolute path to the root of the project
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.append(project_root)
from app.config.settings import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD
from app.config.settings import setup_logger

# Setup logger
logger = setup_logger()

# Establish Redis connection
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)


def publish_dish(stream_name, dish):
    """
    Publish a dish to a specified Redis stream.
    """
    dish_id = redis_client.xadd(stream_name, dish)
    logger.info(f"Published {dish['name']} to {stream_name} with ID {dish_id.decode('utf-8')}")


def chef_jacquin_menu():
    """
    Simulates Chef Jacquin preparing dishes and publishing them to different streams.
    """
    starters = [
        'Bruschetta', 'Caesar Salad', 'Garlic Bread', 'Caprese Salad',
        'Shrimp Cocktail', 'Stuffed Mushrooms', 'Deviled Eggs', 'Pulled Pork Sliders',
        'Soup of the Day', 'Spring Rolls'
    ]
    mains = [
        'Steak Frites', 'Trout Almondine', 'Coq au Vin', 'Ratatouille',
        'Chicken Parmesan', 'Seared Salmon', 'Vegetable Stir Fry', 'Lamb Shank',
        'Pork Belly', 'Duck Confit'
    ]
    desserts = [
        'Crème Brûlée', 'Tarte Tatin', 'Chocolate Mousse', 'Profiteroles',
        'Apple Pie', 'Cheesecake', 'Pavlova', 'Sorbet', 'Tiramisu', 'Panna Cotta'
    ]

    while True:  # Infinite loop to continuously produce dishes
        dish_type = choice(['starter', 'main', 'dessert'])
        if dish_type == 'starter':
            dish_name = choice(starters)
            stream = 'stream:starters'
        elif dish_type == 'main':
            dish_name = choice(mains)
            stream = 'stream:mains'
        else:
            dish_name = choice(desserts)
            stream = 'stream:desserts'

        dish_speed = randint(2, 4)  # Random preparation time
        dish = {
            'name': dish_name,  # Ensure the name is a string, not bytes
            'prep_time': str(dish_speed)
        }

        publish_dish(stream, dish)
        logger.debug(f"Next dish preparation in {dish_speed} seconds.")
        sleep(dish_speed)  # Simulate time taken to prepare the next dish


if __name__ == '__main__':
    try:
        chef_jacquin_menu()
    except KeyboardInterrupt:
        logger.info("Shutdown requested, exiting...")
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
