


def get_quality_of_life_for_NY():
    # PART 1: Calling the Teleport API (Quality of Life)

    # initial call to Teleport API about NYC quality of life
    base_url = "https://api.teleport.org/api/urban_areas/slug:new-york/scores/"
    r = requests.get(base_url)
    d = r.json()

    # creating cache dictionary for teleport
    dir_path = os.path.dirname(os.path.realpath(__file__))
    cache = dir_path + '/' + "nyc_cache.json"
    with open(cache, "w") as json_file:
        json.dump(d, json_file)
    json_file.close()

    # reading cache dictionary contents
    cache_file = open(cache, 'r')
    cache_contents = cache_file.read()
    cache_dict_teleport = json.loads(cache_contents)
    cache_file.close()

    # score of life in NYC
    nyc_score = cache_dict_teleport["teleport_city_score"]

    return nyc_score