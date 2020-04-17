import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render
from .models import PokemonEntity, Pokemon
from django.core.exceptions import ObjectDoesNotExist

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = "https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832&fill=transparent"


def add_pokemon(folium_map, lat, lon, name, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        tooltip=name,
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    # with open("pokemon_entities/pokemons.json", encoding="utf-8") as database:
    #     pokemons = json.load(database)['pokemons']
    pokemons = Pokemon.objects.all()

    # print(type(pokemons.pokemonentity_set))
    # print(dir(pokemons.pokemonentity_set[0]))

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon in pokemons:
        print(PokemonEntity.objects.filter(pokemon=pokemon).first())
        for pokemon_entity in PokemonEntity.objects.filter(pokemon=pokemon):
            print(pokemon.title, pokemon.photo.url)
            add_pokemon(
                folium_map, pokemon_entity.lat, pokemon_entity.lon,
                pokemon.title, request.build_absolute_uri(pokemon.photo.url))

    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(pokemon.photo.url),
            'title_ru': pokemon.title,
        })

    return render(request, "mainpage.html", context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    with open("pokemon_entities/pokemons.json", encoding="utf-8") as database:
        pokemons = json.load(database)['pokemons']

    for pokemon in pokemons:
        if pokemon['pokemon_id'] == int(pokemon_id):
            requested_pokemon = pokemon
            break
    else:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    try:
        pokemon = Pokemon.objects.get(id=int(pokemon_id))
    except ObjectDoesNotExist:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    pokemon_entitys = PokemonEntity.objects.filter(pokemon=pokemon)

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entitys:
        add_pokemon(
            folium_map, pokemon_entity.lat, pokemon_entity.lon,
            pokemon.title, request.build_absolute_uri(pokemon.photo.url))

    return render(request, "pokemon.html", context={'map': folium_map._repr_html_(),
                                                    'pokemon': pokemon})
