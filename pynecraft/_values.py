# This internal file contains the data that is imported automatically from the minecraft jar file and reports.
# They are all imported into info.py, and you should import them from there.

from collections import namedtuple
from typing import Tuple

from pynecraft.base import _in_group, de_arg, is_arg, StrOrArg


def _value(v, dups: dict):
    if is_arg(v):
        return de_arg(v)
    try:
        return dups[v]
    except KeyError:
        return v


def _as_things(group: list, dups: dict, *values: StrOrArg) -> str | Tuple[str, ...]:
    if len(values) == 1:
        return _in_group(group, _value(values[0], dups))
    return tuple((_in_group(group, _value(v, dups)) for v in values))



# Generated values:

# Generated from Minecraft 26.2-snapshot-5 jar data, 2026-05-04T14:23:00-07:00

wolves = ('ashen', 'black', 'chestnut', 'pale', 'rusty', 'snowy', 'spotted', 'striped', 'woods')
trim_materials = ('amethyst', 'copper', 'diamond', 'emerald', 'gold', 'iron', 'lapis', 'netherite', 'quartz', 'redstone', 'resin')
trim_patterns = ('bolt', 'coast', 'dune', 'eye', 'flow', 'host', 'raiser', 'rib', 'sentry', 'shaper', 'silence', 'snout', 'spire', 'tide', 'vex', 'ward', 'wayfinder', 'wild')


# TeamOptions
__teamoption_dups = {}
COLLISION_RULE = "collisionRule"
COLOR = "color"
DEATH_MESSAGE_VISIBILITY = "deathMessageVisibility"
__teamoption_dups["displayname"] = "displayName"
FRIENDLY_FIRE = "friendlyFire"
NAMETAG_VISIBILITY = "nametagVisibility"
PREFIX = "prefix"
SEE_FRIENDLY_INVISIBLES = "seeFriendlyInvisibles"
SUFFIX = "suffix"
TEAM_OPTION_GROUP = [
    COLLISION_RULE, COLOR, DEATH_MESSAGE_VISIBILITY, "displayName", FRIENDLY_FIRE, NAMETAG_VISIBILITY, PREFIX, SEE_FRIENDLY_INVISIBLES, SUFFIX
]

TeamOptionInfo = namedtuple("TeamOption", ['name', 'value', 'desc', 'type'])
team_options = {
    "COLLISION_RULE": TeamOptionInfo("""collision Rule""", "collisionRule", None, ['always', 'never', 'pushOtherTeams', 'pushOwnTeam']),
    "COLOR": TeamOptionInfo("""color""", "color", None, 'Nbt'),
    "DEATH_MESSAGE_VISIBILITY": TeamOptionInfo("""death Message Visibility""", "deathMessageVisibility", None, ['always', 'hideForOtherTeams', 'hideForOwnTeam', 'never']),
    "DISPLAY_NAME": TeamOptionInfo("""display Name""", "displayName", None, 'Nbt'),
    "FRIENDLY_FIRE": TeamOptionInfo("""friendly Fire""", "friendlyFire", None, bool),
    "NAMETAG_VISIBILITY": TeamOptionInfo("""nametag Visibility""", "nametagVisibility", None, ['always', 'hideForOtherTeams', 'hideForOwnTeam', 'never']),
    "PREFIX": TeamOptionInfo("""prefix""", "prefix", None, 'Nbt'),
    "SEE_FRIENDLY_INVISIBLES": TeamOptionInfo("""see Friendly Invisibles""", "seeFriendlyInvisibles", None, bool),
    "SUFFIX": TeamOptionInfo("""suffix""", "suffix", None, 'Nbt'),
}

for __k in tuple(team_options.keys()):
    v = team_options[__k]
    team_options[v.name] = v
    team_options[v.value] = v


def as_teamoption(*values: StrOrArg) -> str | Tuple[str, ...]:
    return _as_things(TEAM_OPTION_GROUP, __teamoption_dups, *values)



# Patterns
__pattern_dups = {}
BASE = "base"
BORDER = "border"
BRICKS = "bricks"
CIRCLE = "circle"
CREEPER = "creeper"
CROSS = "cross"
CURLY_BORDER = "curly_border"
DIAGONAL_LEFT = "diagonal_left"
DIAGONAL_RIGHT = "diagonal_right"
DIAGONAL_UP_LEFT = "diagonal_up_left"
DIAGONAL_UP_RIGHT = "diagonal_up_right"
FLOW = "flow"
FLOWER = "flower"
GLOBE = "globe"
GRADIENT = "gradient"
GRADIENT_UP = "gradient_up"
GUSTER = "guster"
HALF_HORIZONTAL = "half_horizontal"
HALF_HORIZONTAL_BOTTOM = "half_horizontal_bottom"
HALF_VERTICAL = "half_vertical"
HALF_VERTICAL_RIGHT = "half_vertical_right"
MOJANG = "mojang"
PIGLIN = "piglin"
RHOMBUS = "rhombus"
SKULL = "skull"
SMALL_STRIPES = "small_stripes"
SQUARE_BOTTOM_LEFT = "square_bottom_left"
SQUARE_BOTTOM_RIGHT = "square_bottom_right"
SQUARE_TOP_LEFT = "square_top_left"
SQUARE_TOP_RIGHT = "square_top_right"
STRAIGHT_CROSS = "straight_cross"
STRIPE_BOTTOM = "stripe_bottom"
STRIPE_CENTER = "stripe_center"
STRIPE_DOWNLEFT = "stripe_downleft"
STRIPE_DOWNRIGHT = "stripe_downright"
STRIPE_LEFT = "stripe_left"
STRIPE_MIDDLE = "stripe_middle"
STRIPE_RIGHT = "stripe_right"
STRIPE_TOP = "stripe_top"
TRIANGLES_BOTTOM = "triangles_bottom"
TRIANGLES_TOP = "triangles_top"
TRIANGLE_BOTTOM = "triangle_bottom"
TRIANGLE_TOP = "triangle_top"
PATTERN_GROUP = [
    BASE, BORDER, BRICKS, CIRCLE, CREEPER, CROSS, CURLY_BORDER, DIAGONAL_LEFT, DIAGONAL_RIGHT, DIAGONAL_UP_LEFT, DIAGONAL_UP_RIGHT, FLOW, FLOWER, GLOBE, GRADIENT, GRADIENT_UP, GUSTER, HALF_HORIZONTAL, HALF_HORIZONTAL_BOTTOM, HALF_VERTICAL, HALF_VERTICAL_RIGHT, MOJANG, PIGLIN, RHOMBUS, SKULL, SMALL_STRIPES, SQUARE_BOTTOM_LEFT, SQUARE_BOTTOM_RIGHT, SQUARE_TOP_LEFT, SQUARE_TOP_RIGHT, STRAIGHT_CROSS, STRIPE_BOTTOM, STRIPE_CENTER, STRIPE_DOWNLEFT, STRIPE_DOWNRIGHT, STRIPE_LEFT, STRIPE_MIDDLE, STRIPE_RIGHT, STRIPE_TOP, TRIANGLES_BOTTOM, TRIANGLES_TOP, TRIANGLE_BOTTOM, TRIANGLE_TOP
]

PatternInfo = namedtuple("Pattern", ['name', 'value', 'desc'])
patterns = {
    "BASE": PatternInfo("""Base""", "base", """Base"""),
    "BORDER": PatternInfo("""Border""", "border", """Border"""),
    "BRICKS": PatternInfo("""Bricks""", "bricks", """Bricks"""),
    "CIRCLE": PatternInfo("""Circle""", "circle", """Circle"""),
    "CREEPER": PatternInfo("""Creeper""", "creeper", """Creeper"""),
    "CROSS": PatternInfo("""Cross""", "cross", """Cross"""),
    "CURLY_BORDER": PatternInfo("""Curly Border""", "curly_border", """Curly Border"""),
    "DIAGONAL_LEFT": PatternInfo("""Diagonal Left""", "diagonal_left", """Diagonal Left"""),
    "DIAGONAL_RIGHT": PatternInfo("""Diagonal Right""", "diagonal_right", """Diagonal Right"""),
    "DIAGONAL_UP_LEFT": PatternInfo("""Diagonal Up Left""", "diagonal_up_left", """Diagonal Up Left"""),
    "DIAGONAL_UP_RIGHT": PatternInfo("""Diagonal Up Right""", "diagonal_up_right", """Diagonal Up Right"""),
    "FLOW": PatternInfo("""Flow""", "flow", """Flow"""),
    "FLOWER": PatternInfo("""Flower""", "flower", """Flower"""),
    "GLOBE": PatternInfo("""Globe""", "globe", """Globe"""),
    "GRADIENT": PatternInfo("""Gradient""", "gradient", """Gradient"""),
    "GRADIENT_UP": PatternInfo("""Gradient Up""", "gradient_up", """Gradient Up"""),
    "GUSTER": PatternInfo("""Guster""", "guster", """Guster"""),
    "HALF_HORIZONTAL": PatternInfo("""Half Horizontal""", "half_horizontal", """Half Horizontal"""),
    "HALF_HORIZONTAL_BOTTOM": PatternInfo("""Half Horizontal Bottom""", "half_horizontal_bottom", """Half Horizontal Bottom"""),
    "HALF_VERTICAL": PatternInfo("""Half Vertical""", "half_vertical", """Half Vertical"""),
    "HALF_VERTICAL_RIGHT": PatternInfo("""Half Vertical Right""", "half_vertical_right", """Half Vertical Right"""),
    "MOJANG": PatternInfo("""Mojang""", "mojang", """Mojang"""),
    "PIGLIN": PatternInfo("""Piglin""", "piglin", """Piglin"""),
    "RHOMBUS": PatternInfo("""Rhombus""", "rhombus", """Rhombus"""),
    "SKULL": PatternInfo("""Skull""", "skull", """Skull"""),
    "SMALL_STRIPES": PatternInfo("""Small Stripes""", "small_stripes", """Small Stripes"""),
    "SQUARE_BOTTOM_LEFT": PatternInfo("""Square Bottom Left""", "square_bottom_left", """Square Bottom Left"""),
    "SQUARE_BOTTOM_RIGHT": PatternInfo("""Square Bottom Right""", "square_bottom_right", """Square Bottom Right"""),
    "SQUARE_TOP_LEFT": PatternInfo("""Square Top Left""", "square_top_left", """Square Top Left"""),
    "SQUARE_TOP_RIGHT": PatternInfo("""Square Top Right""", "square_top_right", """Square Top Right"""),
    "STRAIGHT_CROSS": PatternInfo("""Straight Cross""", "straight_cross", """Straight Cross"""),
    "STRIPE_BOTTOM": PatternInfo("""Stripe Bottom""", "stripe_bottom", """Stripe Bottom"""),
    "STRIPE_CENTER": PatternInfo("""Stripe Center""", "stripe_center", """Stripe Center"""),
    "STRIPE_DOWNLEFT": PatternInfo("""Stripe Downleft""", "stripe_downleft", """Stripe Downleft"""),
    "STRIPE_DOWNRIGHT": PatternInfo("""Stripe Downright""", "stripe_downright", """Stripe Downright"""),
    "STRIPE_LEFT": PatternInfo("""Stripe Left""", "stripe_left", """Stripe Left"""),
    "STRIPE_MIDDLE": PatternInfo("""Stripe Middle""", "stripe_middle", """Stripe Middle"""),
    "STRIPE_RIGHT": PatternInfo("""Stripe Right""", "stripe_right", """Stripe Right"""),
    "STRIPE_TOP": PatternInfo("""Stripe Top""", "stripe_top", """Stripe Top"""),
    "TRIANGLES_BOTTOM": PatternInfo("""Triangles Bottom""", "triangles_bottom", """Triangles Bottom"""),
    "TRIANGLES_TOP": PatternInfo("""Triangles Top""", "triangles_top", """Triangles Top"""),
    "TRIANGLE_BOTTOM": PatternInfo("""Triangle Bottom""", "triangle_bottom", """Triangle Bottom"""),
    "TRIANGLE_TOP": PatternInfo("""Triangle Top""", "triangle_top", """Triangle Top"""),
}

for __k in tuple(patterns.keys()):
    v = patterns[__k]
    patterns[v.name] = v
    patterns[v.value] = v


def as_pattern(*values: StrOrArg) -> str | Tuple[str, ...]:
    return _as_things(PATTERN_GROUP, __pattern_dups, *values)



# Advancements
__advancement_dups = {}
ACQUIRE_HARDWARE = "story/smelt_iron"
__advancement_dups["adventure"] = "adventure/root"
ADVENTURING_TIME = "adventure/adventuring_time"
ARBALISTIC = "adventure/arbalistic"
A_BALANCED_DIET = "husbandry/balanced_diet"
A_COMPLETE_CATALOGUE = "husbandry/complete_catalogue"
A_FURIOUS_COCKTAIL = "nether/all_potions"
A_SEEDY_PLACE = "husbandry/plant_seed"
A_TERRIBLE_FORTRESS = "nether/find_fortress"
A_THROWAWAY_JOKE = "adventure/throw_trident"
BEACONATOR = "nether/create_full_beacon"
BEE_OUR_GUEST = "husbandry/safely_harvest_honey"
BEST_FRIENDS_FOREVER = "husbandry/tame_an_animal"
BIRTHDAY_SONG = "husbandry/allay_deliver_cake_to_note_block"
BLOWBACK = "adventure/blowback"
BRING_HOME_THE_BEACON = "nether/create_beacon"
BUKKIT_BUKKIT = "husbandry/tadpole_in_a_bucket"
BULLSEYE = "adventure/bullseye"
CAREFUL_RESTORATION = "adventure/craft_decorated_pot_using_only_sherds"
CAVES__CLIFFS = "adventure/fall_from_world_height"
COUNTRY_LODE_TAKE_ME_HOME = "adventure/use_lodestone"
COVER_ME_IN_DEBRIS = "nether/netherite_armor"
COVER_ME_WITH_DIAMONDS = "story/shiny_gear"
CRAFTERS_CRAFTING_CRAFTERS = "adventure/crafters_crafting_crafters"
CRAFTING_A_NEW_LOOK = "adventure/trim_with_any_armor_pattern"
DIAMONDS = "story/mine_diamond"
ENCHANTER = "story/enchant_item"
EYE_SPY = "story/follow_ender_eye"
FEELS_LIKE_HOME = "nether/ride_strider_in_overworld_lava"
FISHY_BUSINESS = "husbandry/fishy_business"
FREE_THE_END = "end/kill_dragon"
GETTING_AN_UPGRADE = "story/upgrade_tools"
GLOW_AND_BEHOLD = "husbandry/make_a_sign_glow"
GOOD_AS_NEW = "husbandry/repair_wolf_armor"
GREAT_VIEW_FROM_UP_HERE = "end/levitate"
HEART_TRANSPLANTER = "adventure/heart_transplanter"
HERO_OF_THE_VILLAGE = "adventure/hero_of_the_village"
HIDDEN_IN_THE_DEPTHS = "nether/obtain_ancient_debris"
HIRED_HELP = "adventure/summon_iron_golem"
HOT_STUFF = "story/lava_bucket"
HOT_TOURIST_DESTINATIONS = "nether/explore_nether"
HOW_DID_WE_GET_HERE = "nether/all_effects"
__advancement_dups["husbandry"] = "husbandry/root"
ICE_BUCKET_CHALLENGE = "story/form_obsidian"
INTO_FIRE = "nether/obtain_blaze_rod"
ISNT_IT_IRON_PICK = "story/iron_tools"
ISNT_IT_SCUTE = "adventure/brush_armadillo"
IS_IT_A_BALLOON = "adventure/spyglass_at_ghast"
IS_IT_A_BIRD = "adventure/spyglass_at_parrot"
IS_IT_A_PLANE = "adventure/spyglass_at_dragon"
IT_SPREADS = "adventure/kill_mob_near_sculk_catalyst"
LIGHTEN_UP = "adventure/lighten_up"
LIGHT_AS_A_RABBIT = "adventure/walk_on_powder_snow_with_leather_boots"
LITTLE_SNIFFS = "husbandry/feed_snifflet"
LOCAL_BREWERY = "nether/brew_potion"
MINECRAFT = "story/root"
MINECRAFT_TRIALS_EDITION = "adventure/minecraft_trials_edition"
MOB_KABOB = "adventure/spear_many_mobs"
MONSTERS_HUNTED = "adventure/kill_all_mobs"
MONSTER_HUNTER = "adventure/kill_a_mob"
__advancement_dups["nether"] = "nether/root"
NOT_QUITE_NINE_LIVES = "nether/charge_respawn_anchor"
NOT_TODAY_THANK_YOU = "story/deflect_arrow"
OH_SHINY = "nether/distract_piglin"
OL_BETSY = "adventure/ol_betsy"
OVEROVERKILL = "adventure/overoverkill"
PLANTING_THE_PAST = "husbandry/plant_any_sniffer_seed"
POSTMORTAL = "adventure/totem_of_undying"
REMOTE_GETAWAY = "end/enter_end_gateway"
RESPECTING_THE_REMNANTS = "adventure/salvage_sherd"
RETURN_TO_SENDER = "nether/return_to_sender"
REVAULTING = "adventure/revaulting"
SERIOUS_DEDICATION = "husbandry/obtain_netherite_hoe"
SHEAR_BRILLIANCE = "husbandry/remove_wolf_armor"
SKYS_THE_LIMIT = "end/elytra"
SMELLS_INTERESTING = "husbandry/obtain_sniffer_egg"
SMITHING_WITH_STYLE = "adventure/trim_with_all_exclusive_armor_patterns"
SNEAK_100 = "adventure/avoid_vibration"
SNIPER_DUEL = "adventure/sniper_duel"
SOUND_OF_MUSIC = "adventure/play_jukebox_in_meadows"
SPOOKY_SCARY_SKELETON = "nether/get_wither_skull"
STAR_TRADER = "adventure/trade_at_world_height"
STAY_HYDRATED = "husbandry/place_dried_ghast_in_water"
STICKY_SITUATION = "adventure/honey_block_slide"
STONE_AGE = "story/mine_stone"
SUBSPACE_BUBBLE = "nether/fast_travel"
SUIT_UP = "story/obtain_armor"
SURGE_PROTECTOR = "adventure/lightning_rod_with_villager_no_fire"
SWEET_DREAMS = "adventure/sleep_in_bed"
TACTICAL_FISHING = "husbandry/tactical_fishing"
TAKE_AIM = "adventure/shoot_arrow"
THE_CITY_AT_THE_END_OF_THE_GAME = "end/find_end_city"
THE_CUTEST_PREDATOR = "husbandry/axolotl_in_a_bucket"
__advancement_dups["the_end"] = "end/root"
THE_END_AGAIN = "end/respawn_dragon"
THE_END_STORY = "story/enter_the_end"
THE_HEALING_POWER_OF_FRIENDSHIP = "husbandry/kill_axolotl_target"
THE_NEXT_GENERATION = "end/dragon_egg"
THE_PARROTS_AND_THE_BATS = "husbandry/breed_an_animal"
THE_POWER_OF_BOOKS = "adventure/read_power_of_chiseled_bookshelf"
THE_WHOLE_PACK = "husbandry/whole_pack"
THIS_BOAT_HAS_LEGS = "nether/ride_strider"
THOSE_WERE_THE_DAYS = "nether/find_bastion"
TOTAL_BEELOCATION = "husbandry/silk_touch_nest"
TWO_BIRDS_ONE_ARROW = "adventure/two_birds_one_arrow"
TWO_BY_TWO = "husbandry/bred_all_animals"
UNDER_LOCK_AND_KEY = "adventure/under_lock_and_key"
UNEASY_ALLIANCE = "nether/uneasy_alliance"
VERY_VERY_FRIGHTENING = "adventure/very_very_frightening"
VOLUNTARY_EXILE = "adventure/voluntary_exile"
WAR_PIGS = "nether/loot_bastion"
WAX_OFF = "husbandry/wax_off"
WAX_ON = "husbandry/wax_on"
WE_NEED_TO_GO_DEEPER = "story/enter_the_nether"
WHATEVER_FLOATS_YOUR_GOAT = "husbandry/ride_a_boat_with_a_goat"
WHAT_A_DEAL = "adventure/trade"
WHEN_THE_SQUAD_HOPS_INTO_TOWN = "husbandry/leash_all_frog_variants"
WHOS_THE_PILLAGER_NOW = "adventure/whos_the_pillager_now"
WHO_IS_CUTTING_ONIONS = "nether/obtain_crying_obsidian"
WHO_NEEDS_ROCKETS = "adventure/who_needs_rockets"
WITHERING_HEIGHTS = "nether/summon_wither"
WITH_OUR_POWERS_COMBINED = "husbandry/froglights"
YOUVE_GOT_A_FRIEND_IN_ME = "husbandry/allay_deliver_item_to_player"
YOU_NEED_A_MINT = "end/dragon_breath"
ZOMBIE_DOCTOR = "story/cure_zombie_villager"
ADVANCEMENT_GROUP = [
    ACQUIRE_HARDWARE, "adventure/root", ADVENTURING_TIME, ARBALISTIC, A_BALANCED_DIET, A_COMPLETE_CATALOGUE, A_FURIOUS_COCKTAIL, A_SEEDY_PLACE, A_TERRIBLE_FORTRESS, A_THROWAWAY_JOKE, BEACONATOR, BEE_OUR_GUEST, BEST_FRIENDS_FOREVER, BIRTHDAY_SONG, BLOWBACK, BRING_HOME_THE_BEACON, BUKKIT_BUKKIT, BULLSEYE, CAREFUL_RESTORATION, CAVES__CLIFFS, COUNTRY_LODE_TAKE_ME_HOME, COVER_ME_IN_DEBRIS, COVER_ME_WITH_DIAMONDS, CRAFTERS_CRAFTING_CRAFTERS, CRAFTING_A_NEW_LOOK, DIAMONDS, ENCHANTER, EYE_SPY, FEELS_LIKE_HOME, FISHY_BUSINESS, FREE_THE_END, GETTING_AN_UPGRADE, GLOW_AND_BEHOLD, GOOD_AS_NEW, GREAT_VIEW_FROM_UP_HERE, HEART_TRANSPLANTER, HERO_OF_THE_VILLAGE, HIDDEN_IN_THE_DEPTHS, HIRED_HELP, HOT_STUFF, HOT_TOURIST_DESTINATIONS, HOW_DID_WE_GET_HERE, "husbandry/root", ICE_BUCKET_CHALLENGE, INTO_FIRE, ISNT_IT_IRON_PICK, ISNT_IT_SCUTE, IS_IT_A_BALLOON, IS_IT_A_BIRD, IS_IT_A_PLANE, IT_SPREADS, LIGHTEN_UP, LIGHT_AS_A_RABBIT, LITTLE_SNIFFS, LOCAL_BREWERY, MINECRAFT, MINECRAFT_TRIALS_EDITION, MOB_KABOB, MONSTERS_HUNTED, MONSTER_HUNTER, "nether/root", NOT_QUITE_NINE_LIVES, NOT_TODAY_THANK_YOU, OH_SHINY, OL_BETSY, OVEROVERKILL, PLANTING_THE_PAST, POSTMORTAL, REMOTE_GETAWAY, RESPECTING_THE_REMNANTS, RETURN_TO_SENDER, REVAULTING, SERIOUS_DEDICATION, SHEAR_BRILLIANCE, SKYS_THE_LIMIT, SMELLS_INTERESTING, SMITHING_WITH_STYLE, SNEAK_100, SNIPER_DUEL, SOUND_OF_MUSIC, SPOOKY_SCARY_SKELETON, STAR_TRADER, STAY_HYDRATED, STICKY_SITUATION, STONE_AGE, SUBSPACE_BUBBLE, SUIT_UP, SURGE_PROTECTOR, SWEET_DREAMS, TACTICAL_FISHING, TAKE_AIM, THE_CITY_AT_THE_END_OF_THE_GAME, THE_CUTEST_PREDATOR, "end/root", THE_END_AGAIN, THE_END_STORY, THE_HEALING_POWER_OF_FRIENDSHIP, THE_NEXT_GENERATION, THE_PARROTS_AND_THE_BATS, THE_POWER_OF_BOOKS, THE_WHOLE_PACK, THIS_BOAT_HAS_LEGS, THOSE_WERE_THE_DAYS, TOTAL_BEELOCATION, TWO_BIRDS_ONE_ARROW, TWO_BY_TWO, UNDER_LOCK_AND_KEY, UNEASY_ALLIANCE, VERY_VERY_FRIGHTENING, VOLUNTARY_EXILE, WAR_PIGS, WAX_OFF, WAX_ON, WE_NEED_TO_GO_DEEPER, WHATEVER_FLOATS_YOUR_GOAT, WHAT_A_DEAL, WHEN_THE_SQUAD_HOPS_INTO_TOWN, WHOS_THE_PILLAGER_NOW, WHO_IS_CUTTING_ONIONS, WHO_NEEDS_ROCKETS, WITHERING_HEIGHTS, WITH_OUR_POWERS_COMBINED, YOUVE_GOT_A_FRIEND_IN_ME, YOU_NEED_A_MINT, ZOMBIE_DOCTOR
]

AdvancementInfo = namedtuple("Advancement", ['name', 'value', 'desc'])
advancements = {
    "ACQUIRE_HARDWARE": AdvancementInfo("""Acquire Hardware""", "story/smelt_iron", """Smelt an Iron Ingot"""),
    "ADVENTURE": AdvancementInfo("""Adventure""", "adventure/root", """Adventure, exploration and combat"""),
    "ADVENTURING_TIME": AdvancementInfo("""Adventuring Time""", "adventure/adventuring_time", """Discover every biome"""),
    "ARBALISTIC": AdvancementInfo("""Arbalistic""", "adventure/arbalistic", """Kill five unique mobs with one crossbow shot"""),
    "A_BALANCED_DIET": AdvancementInfo("""A Balanced Diet""", "husbandry/balanced_diet", """Eat everything that is edible, even if it's not good for you"""),
    "A_COMPLETE_CATALOGUE": AdvancementInfo("""A Complete Catalogue""", "husbandry/complete_catalogue", """Tame all Cat variants!"""),
    "A_FURIOUS_COCKTAIL": AdvancementInfo("""A Furious Cocktail""", "nether/all_potions", """Have every potion effect applied at the same time"""),
    "A_SEEDY_PLACE": AdvancementInfo("""A Seedy Place""", "husbandry/plant_seed", """Plant a seed and watch it grow"""),
    "A_TERRIBLE_FORTRESS": AdvancementInfo("""A Terrible Fortress""", "nether/find_fortress", """Break your way into a Nether Fortress"""),
    "A_THROWAWAY_JOKE": AdvancementInfo("""A Throwaway Joke""", "adventure/throw_trident", """Throw a Trident at something.
Note: Throwing away your only weapon is not a good idea."""),
    "BEACONATOR": AdvancementInfo("""Beaconator""", "nether/create_full_beacon", """Bring a Beacon to full power"""),
    "BEE_OUR_GUEST": AdvancementInfo("""Bee Our Guest""", "husbandry/safely_harvest_honey", """Use a Campfire to collect Honey from a Beehive using a Glass Bottle without aggravating the Bees"""),
    "BEST_FRIENDS_FOREVER": AdvancementInfo("""Best Friends Forever""", "husbandry/tame_an_animal", """Tame an animal"""),
    "BIRTHDAY_SONG": AdvancementInfo("""Birthday Song""", "husbandry/allay_deliver_cake_to_note_block", """Have an Allay drop a Cake at a Note Block"""),
    "BLOWBACK": AdvancementInfo("""Blowback""", "adventure/blowback", """Kill a Breeze with a deflected Breeze-shot Wind Charge"""),
    "BRING_HOME_THE_BEACON": AdvancementInfo("""Bring Home the Beacon""", "nether/create_beacon", """Construct and place a Beacon"""),
    "BUKKIT_BUKKIT": AdvancementInfo("""Bukkit Bukkit""", "husbandry/tadpole_in_a_bucket", """Catch a Tadpole in a Bucket"""),
    "BULLSEYE": AdvancementInfo("""Bullseye""", "adventure/bullseye", """Hit the bullseye of a Target block from at least 30 meters away"""),
    "CAREFUL_RESTORATION": AdvancementInfo("""Careful Restoration""", "adventure/craft_decorated_pot_using_only_sherds", """Make a Decorated Pot out of 4 Pottery Sherds"""),
    "CAVES__CLIFFS": AdvancementInfo("""Caves & Cliffs""", "adventure/fall_from_world_height", """Free fall from the top of the world (build limit) to the bottom of the world and survive"""),
    "COUNTRY_LODE_TAKE_ME_HOME": AdvancementInfo("""Country Lode, Take Me Home""", "adventure/use_lodestone", """Use a Compass on a Lodestone"""),
    "COVER_ME_IN_DEBRIS": AdvancementInfo("""Cover Me in Debris""", "nether/netherite_armor", """Get a full suit of Netherite armor"""),
    "COVER_ME_WITH_DIAMONDS": AdvancementInfo("""Cover Me with Diamonds""", "story/shiny_gear", """Diamond armor saves lives"""),
    "CRAFTERS_CRAFTING_CRAFTERS": AdvancementInfo("""Crafters Crafting Crafters""", "adventure/crafters_crafting_crafters", """Be near a Crafter when it crafts a Crafter"""),
    "CRAFTING_A_NEW_LOOK": AdvancementInfo("""Crafting a New Look""", "adventure/trim_with_any_armor_pattern", """Craft trimmed armor at a Smithing Table"""),
    "DIAMONDS": AdvancementInfo("""Diamonds!""", "story/mine_diamond", """Acquire diamonds"""),
    "ENCHANTER": AdvancementInfo("""Enchanter""", "story/enchant_item", """Enchant an item at an Enchanting Table"""),
    "EYE_SPY": AdvancementInfo("""Eye Spy""", "story/follow_ender_eye", """Follow an Eye of Ender"""),
    "FEELS_LIKE_HOME": AdvancementInfo("""Feels Like Home""", "nether/ride_strider_in_overworld_lava", """Take a Strider for a loooong ride on a lava lake in the Overworld"""),
    "FISHY_BUSINESS": AdvancementInfo("""Fishy Business""", "husbandry/fishy_business", """Catch a fish"""),
    "FREE_THE_END": AdvancementInfo("""Free the End""", "end/kill_dragon", """Good luck"""),
    "GETTING_AN_UPGRADE": AdvancementInfo("""Getting an Upgrade""", "story/upgrade_tools", """Construct a better Pickaxe"""),
    "GLOW_AND_BEHOLD": AdvancementInfo("""Glow and Behold!""", "husbandry/make_a_sign_glow", """Make the text of any kind of sign glow"""),
    "GOOD_AS_NEW": AdvancementInfo("""Good as New""", "husbandry/repair_wolf_armor", """Fully repair damaged Wolf Armor using Armadillo Scutes"""),
    "GREAT_VIEW_FROM_UP_HERE": AdvancementInfo("""Great View From Up Here""", "end/levitate", """Levitate up 50 blocks from the attacks of a Shulker"""),
    "HEART_TRANSPLANTER": AdvancementInfo("""Heart Transplanter""", "adventure/heart_transplanter", """Place a Creaking Heart with the correct alignment between two Pale Oak Log blocks"""),
    "HERO_OF_THE_VILLAGE": AdvancementInfo("""Hero of the Village""", "adventure/hero_of_the_village", """Successfully defend a village from a raid"""),
    "HIDDEN_IN_THE_DEPTHS": AdvancementInfo("""Hidden in the Depths""", "nether/obtain_ancient_debris", """Obtain Ancient Debris"""),
    "HIRED_HELP": AdvancementInfo("""Hired Help""", "adventure/summon_iron_golem", """Summon an Iron Golem to help defend a village"""),
    "HOT_STUFF": AdvancementInfo("""Hot Stuff""", "story/lava_bucket", """Fill a Bucket with lava"""),
    "HOT_TOURIST_DESTINATIONS": AdvancementInfo("""Hot Tourist Destinations""", "nether/explore_nether", """Explore all Nether biomes"""),
    "HOW_DID_WE_GET_HERE": AdvancementInfo("""How Did We Get Here?""", "nether/all_effects", """Have every effect applied at the same time"""),
    "HUSBANDRY": AdvancementInfo("""Husbandry""", "husbandry/root", """The world is full of friends and food"""),
    "ICE_BUCKET_CHALLENGE": AdvancementInfo("""Ice Bucket Challenge""", "story/form_obsidian", """Obtain a block of Obsidian"""),
    "INTO_FIRE": AdvancementInfo("""Into Fire""", "nether/obtain_blaze_rod", """Relieve a Blaze of its rod"""),
    "ISNT_IT_IRON_PICK": AdvancementInfo("""Isn't It Iron Pick""", "story/iron_tools", """Upgrade your Pickaxe"""),
    "ISNT_IT_SCUTE": AdvancementInfo("""Isn't It Scute?""", "adventure/brush_armadillo", """Get Armadillo Scutes from an Armadillo using a Brush"""),
    "IS_IT_A_BALLOON": AdvancementInfo("""Is It a Balloon?""", "adventure/spyglass_at_ghast", """Look at a Ghast through a Spyglass"""),
    "IS_IT_A_BIRD": AdvancementInfo("""Is It a Bird?""", "adventure/spyglass_at_parrot", """Look at a Parrot through a Spyglass"""),
    "IS_IT_A_PLANE": AdvancementInfo("""Is It a Plane?""", "adventure/spyglass_at_dragon", """Look at the Ender Dragon through a Spyglass"""),
    "IT_SPREADS": AdvancementInfo("""It Spreads""", "adventure/kill_mob_near_sculk_catalyst", """Kill a mob near a Sculk Catalyst"""),
    "LIGHTEN_UP": AdvancementInfo("""Lighten Up""", "adventure/lighten_up", """Scrape a Copper Bulb with an Axe to make it brighter"""),
    "LIGHT_AS_A_RABBIT": AdvancementInfo("""Light as a Rabbit""", "adventure/walk_on_powder_snow_with_leather_boots", """Walk on Powder Snow... without sinking in it"""),
    "LITTLE_SNIFFS": AdvancementInfo("""Little Sniffs""", "husbandry/feed_snifflet", """Feed a Snifflet"""),
    "LOCAL_BREWERY": AdvancementInfo("""Local Brewery""", "nether/brew_potion", """Brew a Potion"""),
    "MINECRAFT": AdvancementInfo("""Minecraft""", "story/root", """The heart and story of the game"""),
    "MINECRAFT_TRIALS_EDITION": AdvancementInfo("""Minecraft: Trial(s) Edition""", "adventure/minecraft_trials_edition", """Step foot in a Trial Chamber"""),
    "MOB_KABOB": AdvancementInfo("""Mob Kabob""", "adventure/spear_many_mobs", """Hit five mobs in the same Charge attack using the Spear"""),
    "MONSTERS_HUNTED": AdvancementInfo("""Monsters Hunted""", "adventure/kill_all_mobs", """Kill one of every hostile monster"""),
    "MONSTER_HUNTER": AdvancementInfo("""Monster Hunter""", "adventure/kill_a_mob", """Kill any hostile monster"""),
    "NETHER": AdvancementInfo("""Nether""", "nether/root", """Bring summer clothes"""),
    "NOT_QUITE_NINE_LIVES": AdvancementInfo("""Not Quite "Nine" Lives""", "nether/charge_respawn_anchor", """Charge a Respawn Anchor to the maximum"""),
    "NOT_TODAY_THANK_YOU": AdvancementInfo("""Not Today, Thank You""", "story/deflect_arrow", """Deflect a projectile with a Shield"""),
    "OH_SHINY": AdvancementInfo("""Oh Shiny""", "nether/distract_piglin", """Distract Piglins with gold"""),
    "OL_BETSY": AdvancementInfo("""Ol' Betsy""", "adventure/ol_betsy", """Shoot a Crossbow"""),
    "OVEROVERKILL": AdvancementInfo("""Over-Overkill""", "adventure/overoverkill", """Deal 50 hearts of damage in a single hit using the Mace"""),
    "PLANTING_THE_PAST": AdvancementInfo("""Planting the Past""", "husbandry/plant_any_sniffer_seed", """Plant any Sniffer seed"""),
    "POSTMORTAL": AdvancementInfo("""Postmortal""", "adventure/totem_of_undying", """Use a Totem of Undying to cheat death"""),
    "REMOTE_GETAWAY": AdvancementInfo("""Remote Getaway""", "end/enter_end_gateway", """Escape the island"""),
    "RESPECTING_THE_REMNANTS": AdvancementInfo("""Respecting the Remnants""", "adventure/salvage_sherd", """Brush a Suspicious block to obtain a Pottery Sherd"""),
    "RETURN_TO_SENDER": AdvancementInfo("""Return to Sender""", "nether/return_to_sender", """Destroy a Ghast with a fireball"""),
    "REVAULTING": AdvancementInfo("""Revaulting""", "adventure/revaulting", """Unlock an Ominous Vault with an Ominous Trial Key"""),
    "SERIOUS_DEDICATION": AdvancementInfo("""Serious Dedication""", "husbandry/obtain_netherite_hoe", """Use a Netherite Ingot to upgrade a Hoe, and then reevaluate your life choices"""),
    "SHEAR_BRILLIANCE": AdvancementInfo("""Shear Brilliance""", "husbandry/remove_wolf_armor", """Remove Wolf Armor from a Wolf using Shears"""),
    "SKYS_THE_LIMIT": AdvancementInfo("""Sky's the Limit""", "end/elytra", """Find Elytra"""),
    "SMELLS_INTERESTING": AdvancementInfo("""Smells Interesting""", "husbandry/obtain_sniffer_egg", """Obtain a Sniffer Egg"""),
    "SMITHING_WITH_STYLE": AdvancementInfo("""Smithing with Style""", "adventure/trim_with_all_exclusive_armor_patterns", """Apply these smithing templates at least once: Spire, Snout, Rib, Ward, Silence, Vex, Tide, Wayfinder"""),
    "SNEAK_100": AdvancementInfo("""Sneak 100""", "adventure/avoid_vibration", """Sneak near a Sculk Sensor or Warden to prevent it from detecting you"""),
    "SNIPER_DUEL": AdvancementInfo("""Sniper Duel""", "adventure/sniper_duel", """Kill a Skeleton from at least 50 meters away"""),
    "SOUND_OF_MUSIC": AdvancementInfo("""Sound of Music""", "adventure/play_jukebox_in_meadows", """Make the Meadows come alive with the sound of music from a Jukebox"""),
    "SPOOKY_SCARY_SKELETON": AdvancementInfo("""Spooky Scary Skeleton""", "nether/get_wither_skull", """Obtain a Wither Skeleton's skull"""),
    "STAR_TRADER": AdvancementInfo("""Star Trader""", "adventure/trade_at_world_height", """Trade with a Villager at the build height limit"""),
    "STAY_HYDRATED": AdvancementInfo("""Stay Hydrated!""", "husbandry/place_dried_ghast_in_water", """Place a Dried Ghast block into water"""),
    "STICKY_SITUATION": AdvancementInfo("""Sticky Situation""", "adventure/honey_block_slide", """Jump into a Honey Block to break your fall"""),
    "STONE_AGE": AdvancementInfo("""Stone Age""", "story/mine_stone", """Mine Stone with your new Pickaxe"""),
    "SUBSPACE_BUBBLE": AdvancementInfo("""Subspace Bubble""", "nether/fast_travel", """Use the Nether to travel 7 km in the Overworld"""),
    "SUIT_UP": AdvancementInfo("""Suit Up""", "story/obtain_armor", """Protect yourself with a piece of iron armor"""),
    "SURGE_PROTECTOR": AdvancementInfo("""Surge Protector""", "adventure/lightning_rod_with_villager_no_fire", """Protect a Villager from an undesired shock without starting a fire"""),
    "SWEET_DREAMS": AdvancementInfo("""Sweet Dreams""", "adventure/sleep_in_bed", """Sleep in a Bed to change your respawn point"""),
    "TACTICAL_FISHING": AdvancementInfo("""Tactical Fishing""", "husbandry/tactical_fishing", """Catch a Fish... without a Fishing Rod!"""),
    "TAKE_AIM": AdvancementInfo("""Take Aim""", "adventure/shoot_arrow", """Shoot something with an Arrow"""),
    "THE_CITY_AT_THE_END_OF_THE_GAME": AdvancementInfo("""The City at the End of the Game""", "end/find_end_city", """Go on in, what could happen?"""),
    "THE_CUTEST_PREDATOR": AdvancementInfo("""The Cutest Predator""", "husbandry/axolotl_in_a_bucket", """Catch an Axolotl in a Bucket"""),
    "THE_END": AdvancementInfo("""The End""", "end/root", """Or the beginning?"""),
    "THE_END_AGAIN": AdvancementInfo("""The End... Again...""", "end/respawn_dragon", """Respawn the Ender Dragon"""),
    "THE_END_STORY": AdvancementInfo("""The End?""", "story/enter_the_end", """Enter the End Portal"""),
    "THE_HEALING_POWER_OF_FRIENDSHIP": AdvancementInfo("""The Healing Power of Friendship!""", "husbandry/kill_axolotl_target", """Team up with an Axolotl and win a fight"""),
    "THE_NEXT_GENERATION": AdvancementInfo("""The Next Generation""", "end/dragon_egg", """Hold the Dragon Egg"""),
    "THE_PARROTS_AND_THE_BATS": AdvancementInfo("""The Parrots and the Bats""", "husbandry/breed_an_animal", """Breed two animals together"""),
    "THE_POWER_OF_BOOKS": AdvancementInfo("""The Power of Books""", "adventure/read_power_of_chiseled_bookshelf", """Read the power signal of a Chiseled Bookshelf using a Comparator"""),
    "THE_WHOLE_PACK": AdvancementInfo("""The Whole Pack""", "husbandry/whole_pack", """Tame one of each Wolf variant"""),
    "THIS_BOAT_HAS_LEGS": AdvancementInfo("""This Boat Has Legs""", "nether/ride_strider", """Ride a Strider with a Warped Fungus on a Stick"""),
    "THOSE_WERE_THE_DAYS": AdvancementInfo("""Those Were the Days""", "nether/find_bastion", """Enter a Bastion Remnant"""),
    "TOTAL_BEELOCATION": AdvancementInfo("""Total Beelocation""", "husbandry/silk_touch_nest", """Move a Bee Nest or Beehive, with 3 Bees inside, using Silk Touch"""),
    "TWO_BIRDS_ONE_ARROW": AdvancementInfo("""Two Birds, One Arrow""", "adventure/two_birds_one_arrow", """Kill two Phantoms with a piercing Arrow"""),
    "TWO_BY_TWO": AdvancementInfo("""Two by Two""", "husbandry/bred_all_animals", """Breed all the animals!"""),
    "UNDER_LOCK_AND_KEY": AdvancementInfo("""Under Lock and Key""", "adventure/under_lock_and_key", """Unlock a Vault with a Trial Key"""),
    "UNEASY_ALLIANCE": AdvancementInfo("""Uneasy Alliance""", "nether/uneasy_alliance", """Rescue a Ghast from the Nether, bring it safely home to the Overworld... and then kill it"""),
    "VERY_VERY_FRIGHTENING": AdvancementInfo("""Very Very Frightening""", "adventure/very_very_frightening", """Strike a Villager with lightning"""),
    "VOLUNTARY_EXILE": AdvancementInfo("""Voluntary Exile""", "adventure/voluntary_exile", """Kill a raid captain.
Maybe consider staying away from villages for the time being..."""),
    "WAR_PIGS": AdvancementInfo("""War Pigs""", "nether/loot_bastion", """Loot a Chest in a Bastion Remnant"""),
    "WAX_OFF": AdvancementInfo("""Wax Off""", "husbandry/wax_off", """Scrape Wax off of a Copper block!"""),
    "WAX_ON": AdvancementInfo("""Wax On""", "husbandry/wax_on", """Apply Honeycomb to a Copper block!"""),
    "WE_NEED_TO_GO_DEEPER": AdvancementInfo("""We Need to Go Deeper""", "story/enter_the_nether", """Build, light, and enter a Nether Portal"""),
    "WHATEVER_FLOATS_YOUR_GOAT": AdvancementInfo("""Whatever Floats Your Goat!""", "husbandry/ride_a_boat_with_a_goat", """Get in a Boat and float with a Goat"""),
    "WHAT_A_DEAL": AdvancementInfo("""What a Deal!""", "adventure/trade", """Successfully trade with a Villager"""),
    "WHEN_THE_SQUAD_HOPS_INTO_TOWN": AdvancementInfo("""When the Squad Hops into Town""", "husbandry/leash_all_frog_variants", """Get each Frog variant on a Lead"""),
    "WHOS_THE_PILLAGER_NOW": AdvancementInfo("""Who's the Pillager Now?""", "adventure/whos_the_pillager_now", """Give a Pillager a taste of their own medicine"""),
    "WHO_IS_CUTTING_ONIONS": AdvancementInfo("""Who is Cutting Onions?""", "nether/obtain_crying_obsidian", """Obtain Crying Obsidian"""),
    "WHO_NEEDS_ROCKETS": AdvancementInfo("""Who Needs Rockets?""", "adventure/who_needs_rockets", """Use a Wind Charge to launch yourself upward 8 blocks"""),
    "WITHERING_HEIGHTS": AdvancementInfo("""Withering Heights""", "nether/summon_wither", """Summon the Wither"""),
    "WITH_OUR_POWERS_COMBINED": AdvancementInfo("""With Our Powers Combined!""", "husbandry/froglights", """Have all Froglights in your inventory"""),
    "YOUVE_GOT_A_FRIEND_IN_ME": AdvancementInfo("""You've Got a Friend in Me""", "husbandry/allay_deliver_item_to_player", """Have an Allay deliver items to you"""),
    "YOU_NEED_A_MINT": AdvancementInfo("""You Need a Mint""", "end/dragon_breath", """Collect Dragon's Breath in a Glass Bottle"""),
    "ZOMBIE_DOCTOR": AdvancementInfo("""Zombie Doctor""", "story/cure_zombie_villager", """Weaken and then cure a Zombie Villager"""),
}

for __k in tuple(advancements.keys()):
    v = advancements[__k]
    advancements[v.name] = v
    advancements[v.value] = v


def as_advancement(*values: StrOrArg) -> str | Tuple[str, ...]:
    return _as_things(ADVANCEMENT_GROUP, __advancement_dups, *values)



# Biomes
__biome_dups = {}
BADLANDS = "badlands"
BAMBOO_JUNGLE = "bamboo_jungle"
BASALT_DELTAS = "basalt_deltas"
BEACH = "beach"
BIRCH_FOREST = "birch_forest"
CHERRY_GROVE = "cherry_grove"
COLD_OCEAN = "cold_ocean"
CRIMSON_FOREST = "crimson_forest"
DARK_FOREST = "dark_forest"
DEEP_COLD_OCEAN = "deep_cold_ocean"
DEEP_DARK = "deep_dark"
DEEP_FROZEN_OCEAN = "deep_frozen_ocean"
DEEP_LUKEWARM_OCEAN = "deep_lukewarm_ocean"
DEEP_OCEAN = "deep_ocean"
DRIPSTONE_CAVES = "dripstone_caves"
END_BARRENS = "end_barrens"
END_HIGHLANDS = "end_highlands"
END_MIDLANDS = "end_midlands"
ERODED_BADLANDS = "eroded_badlands"
FLOWER_FOREST = "flower_forest"
FOREST = "forest"
FROZEN_OCEAN = "frozen_ocean"
FROZEN_PEAKS = "frozen_peaks"
FROZEN_RIVER = "frozen_river"
GROVE = "grove"
ICE_SPIKES = "ice_spikes"
JAGGED_PEAKS = "jagged_peaks"
LUKEWARM_OCEAN = "lukewarm_ocean"
LUSH_CAVES = "lush_caves"
MANGROVE_SWAMP = "mangrove_swamp"
MEADOW = "meadow"
MUSHROOM_FIELDS = "mushroom_fields"
NETHER_WASTES = "nether_wastes"
OCEAN = "ocean"
OLD_GROWTH_BIRCH_FOREST = "old_growth_birch_forest"
OLD_GROWTH_PINE_TAIGA = "old_growth_pine_taiga"
OLD_GROWTH_SPRUCE_TAIGA = "old_growth_spruce_taiga"
PALE_GARDEN = "pale_garden"
RIVER = "river"
SAVANNA_PLATEAU = "savanna_plateau"
SMALL_END_ISLANDS = "small_end_islands"
SNOWY_BEACH = "snowy_beach"
SNOWY_PLAINS = "snowy_plains"
SNOWY_SLOPES = "snowy_slopes"
SNOWY_TAIGA = "snowy_taiga"
SOUL_SAND_VALLEY = "soul_sand_valley"
SPARSE_JUNGLE = "sparse_jungle"
STONY_PEAKS = "stony_peaks"
STONY_SHORE = "stony_shore"
SULFUR_CAVES = "sulfur_caves"
SUNFLOWER_PLAINS = "sunflower_plains"
THE_VOID = "the_void"
WARM_OCEAN = "warm_ocean"
WARPED_FOREST = "warped_forest"
WINDSWEPT_FOREST = "windswept_forest"
WINDSWEPT_GRAVELLY_HILLS = "windswept_gravelly_hills"
WINDSWEPT_HILLS = "windswept_hills"
WINDSWEPT_SAVANNA = "windswept_savanna"
WOODED_BADLANDS = "wooded_badlands"
BIOME_GROUP = [
    BADLANDS, BAMBOO_JUNGLE, BASALT_DELTAS, BEACH, BIRCH_FOREST, CHERRY_GROVE, COLD_OCEAN, CRIMSON_FOREST, DARK_FOREST, DEEP_COLD_OCEAN, DEEP_DARK, DEEP_FROZEN_OCEAN, DEEP_LUKEWARM_OCEAN, DEEP_OCEAN, "desert", DRIPSTONE_CAVES, END_BARRENS, END_HIGHLANDS, END_MIDLANDS, ERODED_BADLANDS, FLOWER_FOREST, FOREST, FROZEN_OCEAN, FROZEN_PEAKS, FROZEN_RIVER, GROVE, ICE_SPIKES, JAGGED_PEAKS, "jungle", LUKEWARM_OCEAN, LUSH_CAVES, MANGROVE_SWAMP, MEADOW, MUSHROOM_FIELDS, NETHER_WASTES, OCEAN, OLD_GROWTH_BIRCH_FOREST, OLD_GROWTH_PINE_TAIGA, OLD_GROWTH_SPRUCE_TAIGA, PALE_GARDEN, "plains", RIVER, "savanna", SAVANNA_PLATEAU, SMALL_END_ISLANDS, SNOWY_BEACH, SNOWY_PLAINS, SNOWY_SLOPES, SNOWY_TAIGA, SOUL_SAND_VALLEY, SPARSE_JUNGLE, STONY_PEAKS, STONY_SHORE, SULFUR_CAVES, SUNFLOWER_PLAINS, "swamp", "taiga", "the_end", THE_VOID, WARM_OCEAN, WARPED_FOREST, WINDSWEPT_FOREST, WINDSWEPT_GRAVELLY_HILLS, WINDSWEPT_HILLS, WINDSWEPT_SAVANNA, WOODED_BADLANDS
]

BiomeInfo = namedtuple("Biome", ['name', 'value', 'desc'])
biomes = {
    "BADLANDS": BiomeInfo("""Badlands""", "badlands", """Badlands"""),
    "BAMBOO_JUNGLE": BiomeInfo("""Bamboo Jungle""", "bamboo_jungle", """Bamboo Jungle"""),
    "BASALT_DELTAS": BiomeInfo("""Basalt Deltas""", "basalt_deltas", """Basalt Deltas"""),
    "BEACH": BiomeInfo("""Beach""", "beach", """Beach"""),
    "BIRCH_FOREST": BiomeInfo("""Birch Forest""", "birch_forest", """Birch Forest"""),
    "CHERRY_GROVE": BiomeInfo("""Cherry Grove""", "cherry_grove", """Cherry Grove"""),
    "COLD_OCEAN": BiomeInfo("""Cold Ocean""", "cold_ocean", """Cold Ocean"""),
    "CRIMSON_FOREST": BiomeInfo("""Crimson Forest""", "crimson_forest", """Crimson Forest"""),
    "DARK_FOREST": BiomeInfo("""Dark Forest""", "dark_forest", """Dark Forest"""),
    "DEEP_COLD_OCEAN": BiomeInfo("""Deep Cold Ocean""", "deep_cold_ocean", """Deep Cold Ocean"""),
    "DEEP_DARK": BiomeInfo("""Deep Dark""", "deep_dark", """Deep Dark"""),
    "DEEP_FROZEN_OCEAN": BiomeInfo("""Deep Frozen Ocean""", "deep_frozen_ocean", """Deep Frozen Ocean"""),
    "DEEP_LUKEWARM_OCEAN": BiomeInfo("""Deep Lukewarm Ocean""", "deep_lukewarm_ocean", """Deep Lukewarm Ocean"""),
    "DEEP_OCEAN": BiomeInfo("""Deep Ocean""", "deep_ocean", """Deep Ocean"""),
    "DESERT": BiomeInfo("""Desert""", "desert", """Desert"""),
    "DRIPSTONE_CAVES": BiomeInfo("""Dripstone Caves""", "dripstone_caves", """Dripstone Caves"""),
    "END_BARRENS": BiomeInfo("""End Barrens""", "end_barrens", """End Barrens"""),
    "END_HIGHLANDS": BiomeInfo("""End Highlands""", "end_highlands", """End Highlands"""),
    "END_MIDLANDS": BiomeInfo("""End Midlands""", "end_midlands", """End Midlands"""),
    "ERODED_BADLANDS": BiomeInfo("""Eroded Badlands""", "eroded_badlands", """Eroded Badlands"""),
    "FLOWER_FOREST": BiomeInfo("""Flower Forest""", "flower_forest", """Flower Forest"""),
    "FOREST": BiomeInfo("""Forest""", "forest", """Forest"""),
    "FROZEN_OCEAN": BiomeInfo("""Frozen Ocean""", "frozen_ocean", """Frozen Ocean"""),
    "FROZEN_PEAKS": BiomeInfo("""Frozen Peaks""", "frozen_peaks", """Frozen Peaks"""),
    "FROZEN_RIVER": BiomeInfo("""Frozen River""", "frozen_river", """Frozen River"""),
    "GROVE": BiomeInfo("""Grove""", "grove", """Grove"""),
    "ICE_SPIKES": BiomeInfo("""Ice Spikes""", "ice_spikes", """Ice Spikes"""),
    "JAGGED_PEAKS": BiomeInfo("""Jagged Peaks""", "jagged_peaks", """Jagged Peaks"""),
    "JUNGLE": BiomeInfo("""Jungle""", "jungle", """Jungle"""),
    "LUKEWARM_OCEAN": BiomeInfo("""Lukewarm Ocean""", "lukewarm_ocean", """Lukewarm Ocean"""),
    "LUSH_CAVES": BiomeInfo("""Lush Caves""", "lush_caves", """Lush Caves"""),
    "MANGROVE_SWAMP": BiomeInfo("""Mangrove Swamp""", "mangrove_swamp", """Mangrove Swamp"""),
    "MEADOW": BiomeInfo("""Meadow""", "meadow", """Meadow"""),
    "MUSHROOM_FIELDS": BiomeInfo("""Mushroom Fields""", "mushroom_fields", """Mushroom Fields"""),
    "NETHER_WASTES": BiomeInfo("""Nether Wastes""", "nether_wastes", """Nether Wastes"""),
    "OCEAN": BiomeInfo("""Ocean""", "ocean", """Ocean"""),
    "OLD_GROWTH_BIRCH_FOREST": BiomeInfo("""Old Growth Birch Forest""", "old_growth_birch_forest", """Old Growth Birch Forest"""),
    "OLD_GROWTH_PINE_TAIGA": BiomeInfo("""Old Growth Pine Taiga""", "old_growth_pine_taiga", """Old Growth Pine Taiga"""),
    "OLD_GROWTH_SPRUCE_TAIGA": BiomeInfo("""Old Growth Spruce Taiga""", "old_growth_spruce_taiga", """Old Growth Spruce Taiga"""),
    "PALE_GARDEN": BiomeInfo("""Pale Garden""", "pale_garden", """Pale Garden"""),
    "PLAINS": BiomeInfo("""Plains""", "plains", """Plains"""),
    "RIVER": BiomeInfo("""River""", "river", """River"""),
    "SAVANNA": BiomeInfo("""Savanna""", "savanna", """Savanna"""),
    "SAVANNA_PLATEAU": BiomeInfo("""Savanna Plateau""", "savanna_plateau", """Savanna Plateau"""),
    "SMALL_END_ISLANDS": BiomeInfo("""Small End Islands""", "small_end_islands", """Small End Islands"""),
    "SNOWY_BEACH": BiomeInfo("""Snowy Beach""", "snowy_beach", """Snowy Beach"""),
    "SNOWY_PLAINS": BiomeInfo("""Snowy Plains""", "snowy_plains", """Snowy Plains"""),
    "SNOWY_SLOPES": BiomeInfo("""Snowy Slopes""", "snowy_slopes", """Snowy Slopes"""),
    "SNOWY_TAIGA": BiomeInfo("""Snowy Taiga""", "snowy_taiga", """Snowy Taiga"""),
    "SOUL_SAND_VALLEY": BiomeInfo("""Soul Sand Valley""", "soul_sand_valley", """Soul Sand Valley"""),
    "SPARSE_JUNGLE": BiomeInfo("""Sparse Jungle""", "sparse_jungle", """Sparse Jungle"""),
    "STONY_PEAKS": BiomeInfo("""Stony Peaks""", "stony_peaks", """Stony Peaks"""),
    "STONY_SHORE": BiomeInfo("""Stony Shore""", "stony_shore", """Stony Shore"""),
    "SULFUR_CAVES": BiomeInfo("""Sulfur Caves""", "sulfur_caves", """Sulfur Caves"""),
    "SUNFLOWER_PLAINS": BiomeInfo("""Sunflower Plains""", "sunflower_plains", """Sunflower Plains"""),
    "SWAMP": BiomeInfo("""Swamp""", "swamp", """Swamp"""),
    "TAIGA": BiomeInfo("""Taiga""", "taiga", """Taiga"""),
    "THE_END": BiomeInfo("""The End""", "the_end", """The End"""),
    "THE_VOID": BiomeInfo("""The Void""", "the_void", """The Void"""),
    "WARM_OCEAN": BiomeInfo("""Warm Ocean""", "warm_ocean", """Warm Ocean"""),
    "WARPED_FOREST": BiomeInfo("""Warped Forest""", "warped_forest", """Warped Forest"""),
    "WINDSWEPT_FOREST": BiomeInfo("""Windswept Forest""", "windswept_forest", """Windswept Forest"""),
    "WINDSWEPT_GRAVELLY_HILLS": BiomeInfo("""Windswept Gravelly Hills""", "windswept_gravelly_hills", """Windswept Gravelly Hills"""),
    "WINDSWEPT_HILLS": BiomeInfo("""Windswept Hills""", "windswept_hills", """Windswept Hills"""),
    "WINDSWEPT_SAVANNA": BiomeInfo("""Windswept Savanna""", "windswept_savanna", """Windswept Savanna"""),
    "WOODED_BADLANDS": BiomeInfo("""Wooded Badlands""", "wooded_badlands", """Wooded Badlands"""),
}

for __k in tuple(biomes.keys()):
    v = biomes[__k]
    biomes[v.name] = v
    biomes[v.value] = v


def as_biome(*values: StrOrArg) -> str | Tuple[str, ...]:
    return _as_things(BIOME_GROUP, __biome_dups, *values)



# Effects
__effect_dups = {}
ABSORPTION = "absorption"
BAD_LUCK = "unluck"
BAD_OMEN = "bad_omen"
BLINDNESS = "blindness"
BREATH_OF_THE_NAUTILUS = "breath_of_the_nautilus"
CONDUIT_POWER = "conduit_power"
DARKNESS = "darkness"
DOLPHINS_GRACE = "dolphins_grace"
FIRE_RESISTANCE = "fire_resistance"
GLOWING = "glowing"
HASTE = "haste"
HEALTH_BOOST = "health_boost"
__effect_dups["adventure/hero_of_the_village"] = "hero_of_the_village"
HUNGER = "hunger"
INFESTED = "infested"
INSTANT_DAMAGE = "instant_damage"
INSTANT_HEALTH = "instant_health"
INVISIBILITY = "invisibility"
JUMP_BOOST = "jump_boost"
LEVITATION = "levitation"
LUCK = "luck"
MINING_FATIGUE = "mining_fatigue"
NAUSEA = "nausea"
NIGHT_VISION = "night_vision"
OOZING = "oozing"
POISON = "poison"
RAID_OMEN = "raid_omen"
REGENERATION = "regeneration"
RESISTANCE = "resistance"
SATURATION = "saturation"
SLOWNESS = "slowness"
SLOW_FALLING = "slow_falling"
SPEED = "speed"
STRENGTH = "strength"
TRIAL_OMEN = "trial_omen"
WATER_BREATHING = "water_breathing"
WEAKNESS = "weakness"
WEAVING = "weaving"
WIND_CHARGED = "wind_charged"
WITHER = "wither"
EFFECT_GROUP = [
    ABSORPTION, BAD_LUCK, BAD_OMEN, BLINDNESS, BREATH_OF_THE_NAUTILUS, CONDUIT_POWER, DARKNESS, DOLPHINS_GRACE, FIRE_RESISTANCE, GLOWING, HASTE, HEALTH_BOOST, "hero_of_the_village", HUNGER, INFESTED, INSTANT_DAMAGE, INSTANT_HEALTH, INVISIBILITY, JUMP_BOOST, LEVITATION, LUCK, MINING_FATIGUE, NAUSEA, NIGHT_VISION, OOZING, POISON, RAID_OMEN, REGENERATION, RESISTANCE, SATURATION, SLOWNESS, SLOW_FALLING, SPEED, STRENGTH, TRIAL_OMEN, WATER_BREATHING, WEAKNESS, WEAVING, WIND_CHARGED, WITHER
]

EffectInfo = namedtuple("Effect", ['name', 'value', 'desc'])
effects = {
    "ABSORPTION": EffectInfo("""Absorption""", "absorption", None),
    "BAD_LUCK": EffectInfo("""Bad Luck""", "unluck", None),
    "BAD_OMEN": EffectInfo("""Bad Omen""", "bad_omen", None),
    "BLINDNESS": EffectInfo("""Blindness""", "blindness", None),
    "BREATH_OF_THE_NAUTILUS": EffectInfo("""Breath of the Nautilus""", "breath_of_the_nautilus", None),
    "CONDUIT_POWER": EffectInfo("""Conduit Power""", "conduit_power", None),
    "DARKNESS": EffectInfo("""Darkness""", "darkness", None),
    "DOLPHINS_GRACE": EffectInfo("""Dolphin's Grace""", "dolphins_grace", None),
    "FIRE_RESISTANCE": EffectInfo("""Fire Resistance""", "fire_resistance", None),
    "GLOWING": EffectInfo("""Glowing""", "glowing", None),
    "HASTE": EffectInfo("""Haste""", "haste", None),
    "HEALTH_BOOST": EffectInfo("""Health Boost""", "health_boost", None),
    "HERO_OF_THE_VILLAGE": EffectInfo("""Hero of the Village""", "hero_of_the_village", None),
    "HUNGER": EffectInfo("""Hunger""", "hunger", None),
    "INFESTED": EffectInfo("""Infested""", "infested", None),
    "INSTANT_DAMAGE": EffectInfo("""Instant Damage""", "instant_damage", None),
    "INSTANT_HEALTH": EffectInfo("""Instant Health""", "instant_health", None),
    "INVISIBILITY": EffectInfo("""Invisibility""", "invisibility", None),
    "JUMP_BOOST": EffectInfo("""Jump Boost""", "jump_boost", None),
    "LEVITATION": EffectInfo("""Levitation""", "levitation", None),
    "LUCK": EffectInfo("""Luck""", "luck", None),
    "MINING_FATIGUE": EffectInfo("""Mining Fatigue""", "mining_fatigue", None),
    "NAUSEA": EffectInfo("""Nausea""", "nausea", None),
    "NIGHT_VISION": EffectInfo("""Night Vision""", "night_vision", None),
    "OOZING": EffectInfo("""Oozing""", "oozing", None),
    "POISON": EffectInfo("""Poison""", "poison", None),
    "RAID_OMEN": EffectInfo("""Raid Omen""", "raid_omen", None),
    "REGENERATION": EffectInfo("""Regeneration""", "regeneration", None),
    "RESISTANCE": EffectInfo("""Resistance""", "resistance", None),
    "SATURATION": EffectInfo("""Saturation""", "saturation", None),
    "SLOWNESS": EffectInfo("""Slowness""", "slowness", None),
    "SLOW_FALLING": EffectInfo("""Slow Falling""", "slow_falling", None),
    "SPEED": EffectInfo("""Speed""", "speed", None),
    "STRENGTH": EffectInfo("""Strength""", "strength", None),
    "TRIAL_OMEN": EffectInfo("""Trial Omen""", "trial_omen", None),
    "WATER_BREATHING": EffectInfo("""Water Breathing""", "water_breathing", None),
    "WEAKNESS": EffectInfo("""Weakness""", "weakness", None),
    "WEAVING": EffectInfo("""Weaving""", "weaving", None),
    "WIND_CHARGED": EffectInfo("""Wind Charged""", "wind_charged", None),
    "WITHER": EffectInfo("""Wither""", "wither", None),
}

for __k in tuple(effects.keys()):
    v = effects[__k]
    effects[v.name] = v
    effects[v.value] = v


def as_effect(*values: StrOrArg) -> str | Tuple[str, ...]:
    return _as_things(EFFECT_GROUP, __effect_dups, *values)



# Enchantments
__enchantment_dups = {}
AQUA_AFFINITY = "aqua_affinity"
BANE_OF_ARTHROPODS = "bane_of_arthropods"
BLAST_PROTECTION = "blast_protection"
BREACH = "breach"
CHANNELING = "channeling"
CURSE_OF_BINDING = "binding_curse"
CURSE_OF_VANISHING = "vanishing_curse"
DENSITY = "density"
DEPTH_STRIDER = "depth_strider"
EFFICIENCY = "efficiency"
FEATHER_FALLING = "feather_falling"
FIRE_ASPECT = "fire_aspect"
FIRE_PROTECTION = "fire_protection"
FLAME = "flame"
FORTUNE = "fortune"
FROST_WALKER = "frost_walker"
IMPALING = "impaling"
INFINITY = "infinity"
KNOCKBACK = "knockback"
LOOTING = "looting"
LOYALTY = "loyalty"
LUCK_OF_THE_SEA = "luck_of_the_sea"
LUNGE = "lunge"
LURE = "lure"
MENDING = "mending"
MULTISHOT = "multishot"
PIERCING = "piercing"
POWER = "power"
PROJECTILE_PROTECTION = "projectile_protection"
PROTECTION = "protection"
PUNCH = "punch"
QUICK_CHARGE = "quick_charge"
RESPIRATION = "respiration"
RIPTIDE = "riptide"
SHARPNESS = "sharpness"
SILK_TOUCH = "silk_touch"
SMITE = "smite"
SOUL_SPEED = "soul_speed"
SWEEPING_EDGE = "sweeping_edge"
SWIFT_SNEAK = "swift_sneak"
THORNS = "thorns"
UNBREAKING = "unbreaking"
WIND_BURST = "wind_burst"
ENCHANTMENT_GROUP = [
    AQUA_AFFINITY, BANE_OF_ARTHROPODS, BLAST_PROTECTION, BREACH, CHANNELING, CURSE_OF_BINDING, CURSE_OF_VANISHING, DENSITY, DEPTH_STRIDER, EFFICIENCY, FEATHER_FALLING, FIRE_ASPECT, FIRE_PROTECTION, FLAME, FORTUNE, FROST_WALKER, IMPALING, INFINITY, KNOCKBACK, LOOTING, LOYALTY, LUCK_OF_THE_SEA, LUNGE, LURE, MENDING, MULTISHOT, PIERCING, POWER, PROJECTILE_PROTECTION, PROTECTION, PUNCH, QUICK_CHARGE, RESPIRATION, RIPTIDE, SHARPNESS, SILK_TOUCH, SMITE, SOUL_SPEED, SWEEPING_EDGE, SWIFT_SNEAK, THORNS, UNBREAKING, WIND_BURST
]

EnchantmentInfo = namedtuple("Enchantment", ['name', 'value', 'desc', 'max_level'])
enchantments = {
    "AQUA_AFFINITY": EnchantmentInfo("""Aqua Affinity""", "aqua_affinity", None, 1),
    "BANE_OF_ARTHROPODS": EnchantmentInfo("""Bane of Arthropods""", "bane_of_arthropods", None, 5),
    "BLAST_PROTECTION": EnchantmentInfo("""Blast Protection""", "blast_protection", None, 4),
    "BREACH": EnchantmentInfo("""Breach""", "breach", None, 4),
    "CHANNELING": EnchantmentInfo("""Channeling""", "channeling", None, 1),
    "CURSE_OF_BINDING": EnchantmentInfo("""Curse of Binding""", "binding_curse", None, 1),
    "CURSE_OF_VANISHING": EnchantmentInfo("""Curse of Vanishing""", "vanishing_curse", None, 1),
    "DENSITY": EnchantmentInfo("""Density""", "density", None, 5),
    "DEPTH_STRIDER": EnchantmentInfo("""Depth Strider""", "depth_strider", None, 3),
    "EFFICIENCY": EnchantmentInfo("""Efficiency""", "efficiency", None, 5),
    "FEATHER_FALLING": EnchantmentInfo("""Feather Falling""", "feather_falling", None, 4),
    "FIRE_ASPECT": EnchantmentInfo("""Fire Aspect""", "fire_aspect", None, 2),
    "FIRE_PROTECTION": EnchantmentInfo("""Fire Protection""", "fire_protection", None, 4),
    "FLAME": EnchantmentInfo("""Flame""", "flame", None, 1),
    "FORTUNE": EnchantmentInfo("""Fortune""", "fortune", None, 3),
    "FROST_WALKER": EnchantmentInfo("""Frost Walker""", "frost_walker", None, 2),
    "IMPALING": EnchantmentInfo("""Impaling""", "impaling", None, 5),
    "INFINITY": EnchantmentInfo("""Infinity""", "infinity", None, 1),
    "KNOCKBACK": EnchantmentInfo("""Knockback""", "knockback", None, 2),
    "LOOTING": EnchantmentInfo("""Looting""", "looting", None, 3),
    "LOYALTY": EnchantmentInfo("""Loyalty""", "loyalty", None, 3),
    "LUCK_OF_THE_SEA": EnchantmentInfo("""Luck of the Sea""", "luck_of_the_sea", None, 3),
    "LUNGE": EnchantmentInfo("""Lunge""", "lunge", None, 3),
    "LURE": EnchantmentInfo("""Lure""", "lure", None, 3),
    "MENDING": EnchantmentInfo("""Mending""", "mending", None, 1),
    "MULTISHOT": EnchantmentInfo("""Multishot""", "multishot", None, 1),
    "PIERCING": EnchantmentInfo("""Piercing""", "piercing", None, 4),
    "POWER": EnchantmentInfo("""Power""", "power", None, 5),
    "PROJECTILE_PROTECTION": EnchantmentInfo("""Projectile Protection""", "projectile_protection", None, 4),
    "PROTECTION": EnchantmentInfo("""Protection""", "protection", None, 4),
    "PUNCH": EnchantmentInfo("""Punch""", "punch", None, 2),
    "QUICK_CHARGE": EnchantmentInfo("""Quick Charge""", "quick_charge", None, 3),
    "RESPIRATION": EnchantmentInfo("""Respiration""", "respiration", None, 3),
    "RIPTIDE": EnchantmentInfo("""Riptide""", "riptide", None, 3),
    "SHARPNESS": EnchantmentInfo("""Sharpness""", "sharpness", None, 5),
    "SILK_TOUCH": EnchantmentInfo("""Silk Touch""", "silk_touch", None, 1),
    "SMITE": EnchantmentInfo("""Smite""", "smite", None, 5),
    "SOUL_SPEED": EnchantmentInfo("""Soul Speed""", "soul_speed", None, 3),
    "SWEEPING_EDGE": EnchantmentInfo("""Sweeping Edge""", "sweeping_edge", None, 3),
    "SWIFT_SNEAK": EnchantmentInfo("""Swift Sneak""", "swift_sneak", None, 3),
    "THORNS": EnchantmentInfo("""Thorns""", "thorns", None, 3),
    "UNBREAKING": EnchantmentInfo("""Unbreaking""", "unbreaking", None, 3),
    "WIND_BURST": EnchantmentInfo("""Wind Burst""", "wind_burst", None, 3),
}

for __k in tuple(enchantments.keys()):
    v = enchantments[__k]
    enchantments[v.name] = v
    enchantments[v.value] = v


def as_enchantment(*values: StrOrArg) -> str | Tuple[str, ...]:
    return _as_things(ENCHANTMENT_GROUP, __enchantment_dups, *values)



# GameRules
__gamerule_dups = {}
ADVANCE_TIME = "advance_time"
ADVANCE_WEATHER = "advance_weather"
ALLOW_ENTERING_NETHER_USING_PORTALS = "allow_entering_nether_using_portals"
BLOCK_DROPS = "block_drops"
BLOCK_EXPLOSION_DROP_DECAY = "block_explosion_drop_decay"
COMMAND_BLOCKS_WORK = "command_blocks_work"
COMMAND_BLOCK_OUTPUT = "command_block_output"
DROWNING_DAMAGE = "drowning_damage"
ELYTRA_MOVEMENT_CHECK = "elytra_movement_check"
ENDER_PEARLS_VANISH_ON_DEATH = "ender_pearls_vanish_on_death"
ENTITY_DROPS = "entity_drops"
FALL_DAMAGE = "fall_damage"
FIRE_DAMAGE = "fire_damage"
FIRE_SPREAD_RADIUS_AROUND_PLAYER = "fire_spread_radius_around_player"
FORGIVE_DEAD_PLAYERS = "forgive_dead_players"
FREEZE_DAMAGE = "freeze_damage"
GLOBAL_SOUND_EVENTS = "global_sound_events"
IMMEDIATE_RESPAWN = "immediate_respawn"
KEEP_INVENTORY = "keep_inventory"
LAVA_SOURCE_CONVERSION = "lava_source_conversion"
LIMITED_CRAFTING = "limited_crafting"
LOCATOR_BAR = "locator_bar"
LOG_ADMIN_COMMANDS = "log_admin_commands"
MAX_BLOCK_MODIFICATIONS = "max_block_modifications"
MAX_COMMAND_FORKS = "max_command_forks"
MAX_COMMAND_SEQUENCE_LENGTH = "max_command_sequence_length"
MAX_ENTITY_CRAMMING = "max_entity_cramming"
MAX_MINECART_SPEED = "max_minecart_speed"
MAX_SNOW_ACCUMULATION_HEIGHT = "max_snow_accumulation_height"
MOB_DROPS = "mob_drops"
MOB_EXPLOSION_DROP_DECAY = "mob_explosion_drop_decay"
MOB_GRIEFING = "mob_griefing"
NATURAL_HEALTH_REGENERATION = "natural_health_regeneration"
PLAYERS_NETHER_PORTAL_CREATIVE_DELAY = "players_nether_portal_creative_delay"
PLAYERS_NETHER_PORTAL_DEFAULT_DELAY = "players_nether_portal_default_delay"
PLAYERS_SLEEPING_PERCENTAGE = "players_sleeping_percentage"
PLAYER_MOVEMENT_CHECK = "player_movement_check"
PROJECTILES_CAN_BREAK_BLOCKS = "projectiles_can_break_blocks"
PVP = "pvp"
RAIDS = "raids"
RANDOM_TICK_SPEED = "random_tick_speed"
REDUCED_DEBUG_INFO = "reduced_debug_info"
RESPAWN_RADIUS = "respawn_radius"
SEND_COMMAND_FEEDBACK = "send_command_feedback"
SHOW_ADVANCEMENT_MESSAGES = "show_advancement_messages"
SHOW_DEATH_MESSAGES = "show_death_messages"
SPAWNER_BLOCKS_WORK = "spawner_blocks_work"
SPAWN_MOBS = "spawn_mobs"
SPAWN_MONSTERS = "spawn_monsters"
SPAWN_PATROLS = "spawn_patrols"
SPAWN_PHANTOMS = "spawn_phantoms"
SPAWN_WANDERING_TRADERS = "spawn_wandering_traders"
SPAWN_WARDENS = "spawn_wardens"
SPECTATORS_GENERATE_CHUNKS = "spectators_generate_chunks"
SPREAD_VINES = "spread_vines"
TNT_EXPLODES = "tnt_explodes"
TNT_EXPLOSION_DROP_DECAY = "tnt_explosion_drop_decay"
UNIVERSAL_ANGER = "universal_anger"
WATER_SOURCE_CONVERSION = "water_source_conversion"
GAME_RULE_GROUP = [
    ADVANCE_TIME, ADVANCE_WEATHER, ALLOW_ENTERING_NETHER_USING_PORTALS, BLOCK_DROPS, BLOCK_EXPLOSION_DROP_DECAY, COMMAND_BLOCKS_WORK, COMMAND_BLOCK_OUTPUT, DROWNING_DAMAGE, ELYTRA_MOVEMENT_CHECK, ENDER_PEARLS_VANISH_ON_DEATH, ENTITY_DROPS, FALL_DAMAGE, FIRE_DAMAGE, FIRE_SPREAD_RADIUS_AROUND_PLAYER, FORGIVE_DEAD_PLAYERS, FREEZE_DAMAGE, GLOBAL_SOUND_EVENTS, IMMEDIATE_RESPAWN, KEEP_INVENTORY, LAVA_SOURCE_CONVERSION, LIMITED_CRAFTING, LOCATOR_BAR, LOG_ADMIN_COMMANDS, MAX_BLOCK_MODIFICATIONS, MAX_COMMAND_FORKS, MAX_COMMAND_SEQUENCE_LENGTH, MAX_ENTITY_CRAMMING, MAX_MINECART_SPEED, MAX_SNOW_ACCUMULATION_HEIGHT, MOB_DROPS, MOB_EXPLOSION_DROP_DECAY, MOB_GRIEFING, NATURAL_HEALTH_REGENERATION, PLAYERS_NETHER_PORTAL_CREATIVE_DELAY, PLAYERS_NETHER_PORTAL_DEFAULT_DELAY, PLAYERS_SLEEPING_PERCENTAGE, PLAYER_MOVEMENT_CHECK, PROJECTILES_CAN_BREAK_BLOCKS, PVP, RAIDS, RANDOM_TICK_SPEED, REDUCED_DEBUG_INFO, RESPAWN_RADIUS, SEND_COMMAND_FEEDBACK, SHOW_ADVANCEMENT_MESSAGES, SHOW_DEATH_MESSAGES, SPAWNER_BLOCKS_WORK, SPAWN_MOBS, SPAWN_MONSTERS, SPAWN_PATROLS, SPAWN_PHANTOMS, SPAWN_WANDERING_TRADERS, SPAWN_WARDENS, SPECTATORS_GENERATE_CHUNKS, SPREAD_VINES, TNT_EXPLODES, TNT_EXPLOSION_DROP_DECAY, UNIVERSAL_ANGER, WATER_SOURCE_CONVERSION
]

GameRuleInfo = namedtuple("GameRule", ['name', 'value', 'desc', 'rule_type'])
game_rules = {
    "ADVANCE_TIME": GameRuleInfo("""advance Time""", "advance_time", None, bool),
    "ADVANCE_WEATHER": GameRuleInfo("""advance Weather""", "advance_weather", None, bool),
    "ALLOW_ENTERING_NETHER_USING_PORTALS": GameRuleInfo("""allow Entering Nether Using Portals""", "allow_entering_nether_using_portals", """Controls whether players are allowed to enter the Nether.""", bool),
    "BLOCK_DROPS": GameRuleInfo("""block Drops""", "block_drops", None, bool),
    "BLOCK_EXPLOSION_DROP_DECAY": GameRuleInfo("""block Explosion Drop Decay""", "block_explosion_drop_decay", """Some of the drops from blocks destroyed by explosions caused by block interactions are lost in the explosion.""", bool),
    "COMMAND_BLOCKS_WORK": GameRuleInfo("""command Blocks Work""", "command_blocks_work", None, bool),
    "COMMAND_BLOCK_OUTPUT": GameRuleInfo("""command Block Output""", "command_block_output", """Broadcast command block output""", bool),
    "DROWNING_DAMAGE": GameRuleInfo("""drowning Damage""", "drowning_damage", """Deal drowning damage""", bool),
    "ELYTRA_MOVEMENT_CHECK": GameRuleInfo("""elytra Movement Check""", "elytra_movement_check", None, bool),
    "ENDER_PEARLS_VANISH_ON_DEATH": GameRuleInfo("""ender Pearls Vanish On Death""", "ender_pearls_vanish_on_death", """Whether Ender Pearls thrown by a player vanish when that player dies.""", bool),
    "ENTITY_DROPS": GameRuleInfo("""entity Drops""", "entity_drops", None, bool),
    "FALL_DAMAGE": GameRuleInfo("""fall Damage""", "fall_damage", """Deal fall damage""", bool),
    "FIRE_DAMAGE": GameRuleInfo("""fire Damage""", "fire_damage", """Deal fire damage""", bool),
    "FIRE_SPREAD_RADIUS_AROUND_PLAYER": GameRuleInfo("""fire Spread Radius Around Player""", "fire_spread_radius_around_player", None, int),
    "FORGIVE_DEAD_PLAYERS": GameRuleInfo("""forgive Dead Players""", "forgive_dead_players", """Angered neutral mobs stop being angry when the targeted player dies nearby.""", bool),
    "FREEZE_DAMAGE": GameRuleInfo("""freeze Damage""", "freeze_damage", """Deal freeze damage""", bool),
    "GLOBAL_SOUND_EVENTS": GameRuleInfo("""global Sound Events""", "global_sound_events", """When certain game events happen, like a boss spawning, the sound is heard everywhere.""", bool),
    "IMMEDIATE_RESPAWN": GameRuleInfo("""immediate Respawn""", "immediate_respawn", None, bool),
    "KEEP_INVENTORY": GameRuleInfo("""keep Inventory""", "keep_inventory", """Keep inventory after death""", bool),
    "LAVA_SOURCE_CONVERSION": GameRuleInfo("""lava Source Conversion""", "lava_source_conversion", """When flowing lava is surrounded on two sides by lava sources, it converts into a source.""", bool),
    "LIMITED_CRAFTING": GameRuleInfo("""limited Crafting""", "limited_crafting", None, bool),
    "LOCATOR_BAR": GameRuleInfo("""locator Bar""", "locator_bar", """When enabled, a bar is shown on the screen to indicate the direction of players.""", bool),
    "LOG_ADMIN_COMMANDS": GameRuleInfo("""log Admin Commands""", "log_admin_commands", """Broadcast admin commands""", bool),
    "MAX_BLOCK_MODIFICATIONS": GameRuleInfo("""max Block Modifications""", "max_block_modifications", None, int),
    "MAX_COMMAND_FORKS": GameRuleInfo("""max Command Forks""", "max_command_forks", None, int),
    "MAX_COMMAND_SEQUENCE_LENGTH": GameRuleInfo("""max Command Sequence Length""", "max_command_sequence_length", None, int),
    "MAX_ENTITY_CRAMMING": GameRuleInfo("""max Entity Cramming""", "max_entity_cramming", """Entity cramming threshold""", int),
    "MAX_MINECART_SPEED": GameRuleInfo("""max Minecart Speed""", "max_minecart_speed", None, int),
    "MAX_SNOW_ACCUMULATION_HEIGHT": GameRuleInfo("""max Snow Accumulation Height""", "max_snow_accumulation_height", None, int),
    "MOB_DROPS": GameRuleInfo("""mob Drops""", "mob_drops", None, bool),
    "MOB_EXPLOSION_DROP_DECAY": GameRuleInfo("""mob Explosion Drop Decay""", "mob_explosion_drop_decay", """Some of the drops from blocks destroyed by explosions caused by mobs are lost in the explosion.""", bool),
    "MOB_GRIEFING": GameRuleInfo("""mob Griefing""", "mob_griefing", """Allow destructive mob actions""", bool),
    "NATURAL_HEALTH_REGENERATION": GameRuleInfo("""natural Health Regeneration""", "natural_health_regeneration", None, bool),
    "PLAYERS_NETHER_PORTAL_CREATIVE_DELAY": GameRuleInfo("""players Nether Portal Creative Delay""", "players_nether_portal_creative_delay", """Time (in ticks) that a creative mode player needs to stand in a Nether Portal before changing dimensions.""", int),
    "PLAYERS_NETHER_PORTAL_DEFAULT_DELAY": GameRuleInfo("""players Nether Portal Default Delay""", "players_nether_portal_default_delay", """Time (in ticks) that a non-creative mode player needs to stand in a Nether Portal before changing dimensions.""", int),
    "PLAYERS_SLEEPING_PERCENTAGE": GameRuleInfo("""players Sleeping Percentage""", "players_sleeping_percentage", """The percentage of players who must be sleeping to skip the night.""", int),
    "PLAYER_MOVEMENT_CHECK": GameRuleInfo("""player Movement Check""", "player_movement_check", None, bool),
    "PROJECTILES_CAN_BREAK_BLOCKS": GameRuleInfo("""projectiles Can Break Blocks""", "projectiles_can_break_blocks", """Controls whether impact projectiles will destroy blocks that are destructible by them.""", bool),
    "PVP": GameRuleInfo("""pvp""", "pvp", """Controls whether players are allowed to damage other players.""", bool),
    "RAIDS": GameRuleInfo("""raids""", "raids", None, bool),
    "RANDOM_TICK_SPEED": GameRuleInfo("""random Tick Speed""", "random_tick_speed", """Random tick speed rate""", int),
    "REDUCED_DEBUG_INFO": GameRuleInfo("""reduced Debug Info""", "reduced_debug_info", """Limits contents of debug screen.""", bool),
    "RESPAWN_RADIUS": GameRuleInfo("""respawn Radius""", "respawn_radius", None, int),
    "SEND_COMMAND_FEEDBACK": GameRuleInfo("""send Command Feedback""", "send_command_feedback", """Send command feedback""", bool),
    "SHOW_ADVANCEMENT_MESSAGES": GameRuleInfo("""show Advancement Messages""", "show_advancement_messages", None, bool),
    "SHOW_DEATH_MESSAGES": GameRuleInfo("""show Death Messages""", "show_death_messages", """Show death messages""", bool),
    "SPAWNER_BLOCKS_WORK": GameRuleInfo("""spawner Blocks Work""", "spawner_blocks_work", None, bool),
    "SPAWN_MOBS": GameRuleInfo("""spawn Mobs""", "spawn_mobs", None, bool),
    "SPAWN_MONSTERS": GameRuleInfo("""spawn Monsters""", "spawn_monsters", """Controls whether monsters naturally spawn.""", bool),
    "SPAWN_PATROLS": GameRuleInfo("""spawn Patrols""", "spawn_patrols", None, bool),
    "SPAWN_PHANTOMS": GameRuleInfo("""spawn Phantoms""", "spawn_phantoms", None, bool),
    "SPAWN_WANDERING_TRADERS": GameRuleInfo("""spawn Wandering Traders""", "spawn_wandering_traders", None, bool),
    "SPAWN_WARDENS": GameRuleInfo("""spawn Wardens""", "spawn_wardens", None, bool),
    "SPECTATORS_GENERATE_CHUNKS": GameRuleInfo("""spectators Generate Chunks""", "spectators_generate_chunks", """Allow spectators to generate terrain""", bool),
    "SPREAD_VINES": GameRuleInfo("""spread Vines""", "spread_vines", None, bool),
    "TNT_EXPLODES": GameRuleInfo("""tnt Explodes""", "tnt_explodes", """Allow TNT to be activated and to explode""", bool),
    "TNT_EXPLOSION_DROP_DECAY": GameRuleInfo("""tnt Explosion Drop Decay""", "tnt_explosion_drop_decay", """Some of the drops from blocks destroyed by explosions caused by TNT are lost in the explosion.""", bool),
    "UNIVERSAL_ANGER": GameRuleInfo("""universal Anger""", "universal_anger", """Angered neutral mobs attack any nearby player, not just the player that angered them. Works best if forgiveDeadPlayers is disabled.""", bool),
    "WATER_SOURCE_CONVERSION": GameRuleInfo("""water Source Conversion""", "water_source_conversion", """When flowing water is surrounded on two sides by water sources, it converts into a source.""", bool),
}

for __k in tuple(game_rules.keys()):
    v = game_rules[__k]
    game_rules[v.name] = v
    game_rules[v.value] = v


def as_gamerule(*values: StrOrArg) -> str | Tuple[str, ...]:
    return _as_things(GAME_RULE_GROUP, __gamerule_dups, *values)



# Particles
__particle_dups = {}
ANGRY_VILLAGER = "angry_villager"
ASH = "ash"
BLOCK_CRUMBLE = "block_crumble"
BUBBLE = "bubble"
BUBBLE_COLUMN_UP = "bubble_column_up"
BUBBLE_POP = "bubble_pop"
CAMPFIRE_COSY_SMOKE = "campfire_cosy_smoke"
CAMPFIRE_SIGNAL_SMOKE = "campfire_signal_smoke"
CHERRY_LEAVES = "cherry_leaves"
CLOUD = "cloud"
COMPOSTER = "composter"
COPPER_FIRE_FLAME = "copper_fire_flame"
CRIMSON_SPORE = "crimson_spore"
CRIT = "crit"
CURRENT_DOWN = "current_down"
DAMAGE_INDICATOR = "damage_indicator"
DOLPHIN = "dolphin"
DRAGON_BREATH = "dragon_breath"
DRIPPING_DRIPSTONE_LAVA = "dripping_dripstone_lava"
DRIPPING_DRIPSTONE_WATER = "dripping_dripstone_water"
DRIPPING_HONEY = "dripping_honey"
DRIPPING_LAVA = "dripping_lava"
DRIPPING_OBSIDIAN_TEAR = "dripping_obsidian_tear"
DRIPPING_WATER = "dripping_water"
DUST = "dust"
DUST_COLOR_TRANSITION = "dust_color_transition"
DUST_PLUME = "dust_plume"
EFFECT = "effect"
EGG_CRACK = "egg_crack"
ELDER_GUARDIAN = "elder_guardian"
ELECTRIC_SPARK = "electric_spark"
ENCHANT = "enchant"
ENCHANTED_HIT = "enchanted_hit"
END_ROD = "end_rod"
ENTITY_EFFECT = "entity_effect"
EXPLOSION = "explosion"
EXPLOSION_EMITTER = "explosion_emitter"
FALLING_DRIPSTONE_LAVA = "falling_dripstone_lava"
FALLING_DRIPSTONE_WATER = "falling_dripstone_water"
FALLING_HONEY = "falling_honey"
FALLING_LAVA = "falling_lava"
FALLING_NECTAR = "falling_nectar"
FALLING_OBSIDIAN_TEAR = "falling_obsidian_tear"
FALLING_SPORE_BLOSSOM = "falling_spore_blossom"
FALLING_WATER = "falling_water"
FIREFLY = "firefly"
FIREWORK = "firework"
FISHING = "fishing"
FLASH = "flash"
GEYSER = "geyser"
GEYSER_BASE = "geyser_base"
GEYSER_PLUME = "geyser_plume"
GEYSER_POOF = "geyser_poof"
GLOW = "glow"
GLOW_SQUID_INK = "glow_squid_ink"
GUST = "gust"
GUST_EMITTER_LARGE = "gust_emitter_large"
GUST_EMITTER_SMALL = "gust_emitter_small"
HAPPY_VILLAGER = "happy_villager"
HEART = "heart"
INSTANT_EFFECT = "instant_effect"
ITEM_COBWEB = "item_cobweb"
ITEM_SLIME = "item_slime"
ITEM_SNOWBALL = "item_snowball"
LANDING_HONEY = "landing_honey"
LANDING_LAVA = "landing_lava"
LANDING_OBSIDIAN_TEAR = "landing_obsidian_tear"
LARGE_SMOKE = "large_smoke"
LAVA = "lava"
MYCELIUM = "mycelium"
NAUTILUS = "nautilus"
NOTE = "note"
NOXIOUS_GAS = "noxious_gas"
NOXIOUS_GAS_CLOUD = "noxious_gas_cloud"
OMINOUS_SPAWNING = "ominous_spawning"
PALE_OAK_LEAVES = "pale_oak_leaves"
PAUSE_MOB_GROWTH = "pause_mob_growth"
POOF = "poof"
PORTAL = "portal"
RESET_MOB_GROWTH = "reset_mob_growth"
REVERSE_PORTAL = "reverse_portal"
SCRAPE = "scrape"
SCULK_CHARGE = "sculk_charge"
SCULK_CHARGE_POP = "sculk_charge_pop"
SCULK_SOUL = "sculk_soul"
SHRIEK = "shriek"
SMALL_FLAME = "small_flame"
SMALL_GUST = "small_gust"
SMOKE = "smoke"
SNEEZE = "sneeze"
SNOWFLAKE = "snowflake"
SONIC_BOOM = "sonic_boom"
SOUL = "soul"
SOUL_FIRE_FLAME = "soul_fire_flame"
SPIT = "spit"
SPLASH = "splash"
SPORE_BLOSSOM_AIR = "spore_blossom_air"
SQUID_INK = "squid_ink"
SULFUR_BUBBLES = "sulfur_bubbles"
SULFUR_CUBE_GOO = "sulfur_cube_goo"
SWEEP_ATTACK = "sweep_attack"
TINTED_LEAVES = "tinted_leaves"
TOTEM_OF_UNDYING = "totem_of_undying"
TRAIL = "trail"
TRIAL_SPAWNER_DETECTION = "trial_spawner_detection"
TRIAL_SPAWNER_DETECTION_OMINOUS = "trial_spawner_detection_ominous"
UNDERWATER = "underwater"
VAULT_CONNECTION = "vault_connection"
VIBRATION = "vibration"
WARPED_SPORE = "warped_spore"
__particle_dups["husbandry/wax_off"] = "wax_off"
__particle_dups["husbandry/wax_on"] = "wax_on"
WHITE_ASH = "white_ash"
WHITE_SMOKE = "white_smoke"
WITCH = "witch"
PARTICLE_GROUP = [
    ANGRY_VILLAGER, ASH, "block", BLOCK_CRUMBLE, "block_marker", BUBBLE, BUBBLE_COLUMN_UP, BUBBLE_POP, CAMPFIRE_COSY_SMOKE, CAMPFIRE_SIGNAL_SMOKE, CHERRY_LEAVES, CLOUD, COMPOSTER, COPPER_FIRE_FLAME, CRIMSON_SPORE, CRIT, CURRENT_DOWN, DAMAGE_INDICATOR, DOLPHIN, DRAGON_BREATH, DRIPPING_DRIPSTONE_LAVA, DRIPPING_DRIPSTONE_WATER, DRIPPING_HONEY, DRIPPING_LAVA, DRIPPING_OBSIDIAN_TEAR, DRIPPING_WATER, DUST, DUST_COLOR_TRANSITION, "dust_pillar", DUST_PLUME, EFFECT, EGG_CRACK, ELDER_GUARDIAN, ELECTRIC_SPARK, ENCHANT, ENCHANTED_HIT, END_ROD, ENTITY_EFFECT, EXPLOSION, EXPLOSION_EMITTER, FALLING_DRIPSTONE_LAVA, FALLING_DRIPSTONE_WATER, "falling_dust", FALLING_HONEY, FALLING_LAVA, FALLING_NECTAR, FALLING_OBSIDIAN_TEAR, FALLING_SPORE_BLOSSOM, FALLING_WATER, FIREFLY, FIREWORK, FISHING, "flame", FLASH, GEYSER, GEYSER_BASE, GEYSER_PLUME, GEYSER_POOF, GLOW, GLOW_SQUID_INK, GUST, GUST_EMITTER_LARGE, GUST_EMITTER_SMALL, HAPPY_VILLAGER, HEART, "infested", INSTANT_EFFECT, "item", ITEM_COBWEB, ITEM_SLIME, ITEM_SNOWBALL, LANDING_HONEY, LANDING_LAVA, LANDING_OBSIDIAN_TEAR, LARGE_SMOKE, LAVA, MYCELIUM, NAUTILUS, NOTE, NOXIOUS_GAS, NOXIOUS_GAS_CLOUD, OMINOUS_SPAWNING, PALE_OAK_LEAVES, PAUSE_MOB_GROWTH, POOF, PORTAL, "raid_omen", "rain", RESET_MOB_GROWTH, REVERSE_PORTAL, SCRAPE, SCULK_CHARGE, SCULK_CHARGE_POP, SCULK_SOUL, SHRIEK, SMALL_FLAME, SMALL_GUST, SMOKE, SNEEZE, SNOWFLAKE, SONIC_BOOM, SOUL, SOUL_FIRE_FLAME, SPIT, SPLASH, SPORE_BLOSSOM_AIR, SQUID_INK, SULFUR_BUBBLES, SULFUR_CUBE_GOO, SWEEP_ATTACK, TINTED_LEAVES, TOTEM_OF_UNDYING, TRAIL, "trial_omen", TRIAL_SPAWNER_DETECTION, TRIAL_SPAWNER_DETECTION_OMINOUS, UNDERWATER, VAULT_CONNECTION, VIBRATION, WARPED_SPORE, "wax_off", "wax_on", WHITE_ASH, WHITE_SMOKE, WITCH
]

ParticleInfo = namedtuple("Particle", ['name', 'value', 'desc'])
particles = {
    "ANGRY_VILLAGER": ParticleInfo("""Angry Villager""", "angry_villager", None),
    "ASH": ParticleInfo("""Ash""", "ash", None),
    "BLOCK": ParticleInfo("""Block""", "block", None),
    "BLOCK_CRUMBLE": ParticleInfo("""Block Crumble""", "block_crumble", None),
    "BLOCK_MARKER": ParticleInfo("""Block Marker""", "block_marker", None),
    "BUBBLE": ParticleInfo("""Bubble""", "bubble", None),
    "BUBBLE_COLUMN_UP": ParticleInfo("""Bubble Column Up""", "bubble_column_up", None),
    "BUBBLE_POP": ParticleInfo("""Bubble Pop""", "bubble_pop", None),
    "CAMPFIRE_COSY_SMOKE": ParticleInfo("""Campfire Cosy Smoke""", "campfire_cosy_smoke", None),
    "CAMPFIRE_SIGNAL_SMOKE": ParticleInfo("""Campfire Signal Smoke""", "campfire_signal_smoke", None),
    "CHERRY_LEAVES": ParticleInfo("""Cherry Leaves""", "cherry_leaves", None),
    "CLOUD": ParticleInfo("""Cloud""", "cloud", None),
    "COMPOSTER": ParticleInfo("""Composter""", "composter", None),
    "COPPER_FIRE_FLAME": ParticleInfo("""Copper Fire Flame""", "copper_fire_flame", None),
    "CRIMSON_SPORE": ParticleInfo("""Crimson Spore""", "crimson_spore", None),
    "CRIT": ParticleInfo("""Crit""", "crit", None),
    "CURRENT_DOWN": ParticleInfo("""Current Down""", "current_down", None),
    "DAMAGE_INDICATOR": ParticleInfo("""Damage Indicator""", "damage_indicator", None),
    "DOLPHIN": ParticleInfo("""Dolphin""", "dolphin", None),
    "DRAGON_BREATH": ParticleInfo("""Dragon Breath""", "dragon_breath", None),
    "DRIPPING_DRIPSTONE_LAVA": ParticleInfo("""Dripping Dripstone Lava""", "dripping_dripstone_lava", None),
    "DRIPPING_DRIPSTONE_WATER": ParticleInfo("""Dripping Dripstone Water""", "dripping_dripstone_water", None),
    "DRIPPING_HONEY": ParticleInfo("""Dripping Honey""", "dripping_honey", None),
    "DRIPPING_LAVA": ParticleInfo("""Dripping Lava""", "dripping_lava", None),
    "DRIPPING_OBSIDIAN_TEAR": ParticleInfo("""Dripping Obsidian Tear""", "dripping_obsidian_tear", None),
    "DRIPPING_WATER": ParticleInfo("""Dripping Water""", "dripping_water", None),
    "DUST": ParticleInfo("""Dust""", "dust", None),
    "DUST_COLOR_TRANSITION": ParticleInfo("""Dust Color Transition""", "dust_color_transition", None),
    "DUST_PILLAR": ParticleInfo("""Dust Pillar""", "dust_pillar", None),
    "DUST_PLUME": ParticleInfo("""Dust Plume""", "dust_plume", None),
    "EFFECT": ParticleInfo("""Effect""", "effect", None),
    "EGG_CRACK": ParticleInfo("""Egg Crack""", "egg_crack", None),
    "ELDER_GUARDIAN": ParticleInfo("""Elder Guardian""", "elder_guardian", None),
    "ELECTRIC_SPARK": ParticleInfo("""Electric Spark""", "electric_spark", None),
    "ENCHANT": ParticleInfo("""Enchant""", "enchant", None),
    "ENCHANTED_HIT": ParticleInfo("""Enchanted Hit""", "enchanted_hit", None),
    "END_ROD": ParticleInfo("""End Rod""", "end_rod", None),
    "ENTITY_EFFECT": ParticleInfo("""Entity Effect""", "entity_effect", None),
    "EXPLOSION": ParticleInfo("""Explosion""", "explosion", None),
    "EXPLOSION_EMITTER": ParticleInfo("""Explosion Emitter""", "explosion_emitter", None),
    "FALLING_DRIPSTONE_LAVA": ParticleInfo("""Falling Dripstone Lava""", "falling_dripstone_lava", None),
    "FALLING_DRIPSTONE_WATER": ParticleInfo("""Falling Dripstone Water""", "falling_dripstone_water", None),
    "FALLING_DUST": ParticleInfo("""Falling Dust""", "falling_dust", None),
    "FALLING_HONEY": ParticleInfo("""Falling Honey""", "falling_honey", None),
    "FALLING_LAVA": ParticleInfo("""Falling Lava""", "falling_lava", None),
    "FALLING_NECTAR": ParticleInfo("""Falling Nectar""", "falling_nectar", None),
    "FALLING_OBSIDIAN_TEAR": ParticleInfo("""Falling Obsidian Tear""", "falling_obsidian_tear", None),
    "FALLING_SPORE_BLOSSOM": ParticleInfo("""Falling Spore Blossom""", "falling_spore_blossom", None),
    "FALLING_WATER": ParticleInfo("""Falling Water""", "falling_water", None),
    "FIREFLY": ParticleInfo("""Firefly""", "firefly", None),
    "FIREWORK": ParticleInfo("""Firework""", "firework", None),
    "FISHING": ParticleInfo("""Fishing""", "fishing", None),
    "FLAME": ParticleInfo("""Flame""", "flame", None),
    "FLASH": ParticleInfo("""Flash""", "flash", None),
    "GEYSER": ParticleInfo("""Geyser""", "geyser", None),
    "GEYSER_BASE": ParticleInfo("""Geyser Base""", "geyser_base", None),
    "GEYSER_PLUME": ParticleInfo("""Geyser Plume""", "geyser_plume", None),
    "GEYSER_POOF": ParticleInfo("""Geyser Poof""", "geyser_poof", None),
    "GLOW": ParticleInfo("""Glow""", "glow", None),
    "GLOW_SQUID_INK": ParticleInfo("""Glow Squid Ink""", "glow_squid_ink", None),
    "GUST": ParticleInfo("""Gust""", "gust", None),
    "GUST_EMITTER_LARGE": ParticleInfo("""Gust Emitter Large""", "gust_emitter_large", None),
    "GUST_EMITTER_SMALL": ParticleInfo("""Gust Emitter Small""", "gust_emitter_small", None),
    "HAPPY_VILLAGER": ParticleInfo("""Happy Villager""", "happy_villager", None),
    "HEART": ParticleInfo("""Heart""", "heart", None),
    "INFESTED": ParticleInfo("""Infested""", "infested", None),
    "INSTANT_EFFECT": ParticleInfo("""Instant Effect""", "instant_effect", None),
    "ITEM": ParticleInfo("""Item""", "item", None),
    "ITEM_COBWEB": ParticleInfo("""Item Cobweb""", "item_cobweb", None),
    "ITEM_SLIME": ParticleInfo("""Item Slime""", "item_slime", None),
    "ITEM_SNOWBALL": ParticleInfo("""Item Snowball""", "item_snowball", None),
    "LANDING_HONEY": ParticleInfo("""Landing Honey""", "landing_honey", None),
    "LANDING_LAVA": ParticleInfo("""Landing Lava""", "landing_lava", None),
    "LANDING_OBSIDIAN_TEAR": ParticleInfo("""Landing Obsidian Tear""", "landing_obsidian_tear", None),
    "LARGE_SMOKE": ParticleInfo("""Large Smoke""", "large_smoke", None),
    "LAVA": ParticleInfo("""Lava""", "lava", None),
    "MYCELIUM": ParticleInfo("""Mycelium""", "mycelium", None),
    "NAUTILUS": ParticleInfo("""Nautilus""", "nautilus", None),
    "NOTE": ParticleInfo("""Note""", "note", None),
    "NOXIOUS_GAS": ParticleInfo("""Noxious Gas""", "noxious_gas", None),
    "NOXIOUS_GAS_CLOUD": ParticleInfo("""Noxious Gas Cloud""", "noxious_gas_cloud", None),
    "OMINOUS_SPAWNING": ParticleInfo("""Ominous Spawning""", "ominous_spawning", None),
    "PALE_OAK_LEAVES": ParticleInfo("""Pale Oak Leaves""", "pale_oak_leaves", None),
    "PAUSE_MOB_GROWTH": ParticleInfo("""Pause Mob Growth""", "pause_mob_growth", None),
    "POOF": ParticleInfo("""Poof""", "poof", None),
    "PORTAL": ParticleInfo("""Portal""", "portal", None),
    "RAID_OMEN": ParticleInfo("""Raid Omen""", "raid_omen", None),
    "RAIN": ParticleInfo("""Rain""", "rain", None),
    "RESET_MOB_GROWTH": ParticleInfo("""Reset Mob Growth""", "reset_mob_growth", None),
    "REVERSE_PORTAL": ParticleInfo("""Reverse Portal""", "reverse_portal", None),
    "SCRAPE": ParticleInfo("""Scrape""", "scrape", None),
    "SCULK_CHARGE": ParticleInfo("""Sculk Charge""", "sculk_charge", None),
    "SCULK_CHARGE_POP": ParticleInfo("""Sculk Charge Pop""", "sculk_charge_pop", None),
    "SCULK_SOUL": ParticleInfo("""Sculk Soul""", "sculk_soul", None),
    "SHRIEK": ParticleInfo("""Shriek""", "shriek", None),
    "SMALL_FLAME": ParticleInfo("""Small Flame""", "small_flame", None),
    "SMALL_GUST": ParticleInfo("""Small Gust""", "small_gust", None),
    "SMOKE": ParticleInfo("""Smoke""", "smoke", None),
    "SNEEZE": ParticleInfo("""Sneeze""", "sneeze", None),
    "SNOWFLAKE": ParticleInfo("""Snowflake""", "snowflake", None),
    "SONIC_BOOM": ParticleInfo("""Sonic Boom""", "sonic_boom", None),
    "SOUL": ParticleInfo("""Soul""", "soul", None),
    "SOUL_FIRE_FLAME": ParticleInfo("""Soul Fire Flame""", "soul_fire_flame", None),
    "SPIT": ParticleInfo("""Spit""", "spit", None),
    "SPLASH": ParticleInfo("""Splash""", "splash", None),
    "SPORE_BLOSSOM_AIR": ParticleInfo("""Spore Blossom Air""", "spore_blossom_air", None),
    "SQUID_INK": ParticleInfo("""Squid Ink""", "squid_ink", None),
    "SULFUR_BUBBLES": ParticleInfo("""Sulfur Bubbles""", "sulfur_bubbles", None),
    "SULFUR_CUBE_GOO": ParticleInfo("""Sulfur Cube Goo""", "sulfur_cube_goo", None),
    "SWEEP_ATTACK": ParticleInfo("""Sweep Attack""", "sweep_attack", None),
    "TINTED_LEAVES": ParticleInfo("""Tinted Leaves""", "tinted_leaves", None),
    "TOTEM_OF_UNDYING": ParticleInfo("""Totem Of Undying""", "totem_of_undying", None),
    "TRAIL": ParticleInfo("""Trail""", "trail", None),
    "TRIAL_OMEN": ParticleInfo("""Trial Omen""", "trial_omen", None),
    "TRIAL_SPAWNER_DETECTION": ParticleInfo("""Trial Spawner Detection""", "trial_spawner_detection", None),
    "TRIAL_SPAWNER_DETECTION_OMINOUS": ParticleInfo("""Trial Spawner Detection Ominous""", "trial_spawner_detection_ominous", None),
    "UNDERWATER": ParticleInfo("""Underwater""", "underwater", None),
    "VAULT_CONNECTION": ParticleInfo("""Vault Connection""", "vault_connection", None),
    "VIBRATION": ParticleInfo("""Vibration""", "vibration", None),
    "WARPED_SPORE": ParticleInfo("""Warped Spore""", "warped_spore", None),
    "WAX_OFF": ParticleInfo("""Wax Off""", "wax_off", None),
    "WAX_ON": ParticleInfo("""Wax On""", "wax_on", None),
    "WHITE_ASH": ParticleInfo("""White Ash""", "white_ash", None),
    "WHITE_SMOKE": ParticleInfo("""White Smoke""", "white_smoke", None),
    "WITCH": ParticleInfo("""Witch""", "witch", None),
}

for __k in tuple(particles.keys()):
    v = particles[__k]
    particles[v.name] = v
    particles[v.value] = v


def as_particle(*values: StrOrArg) -> str | Tuple[str, ...]:
    return _as_things(PARTICLE_GROUP, __particle_dups, *values)



# PotterySherds
__potterysherd_dups = {}
ANGLER_POTTERY_SHERD = "angler_pottery_sherd"
ARCHER_POTTERY_SHERD = "archer_pottery_sherd"
ARMS_UP_POTTERY_SHERD = "arms_up_pottery_sherd"
BLADE_POTTERY_SHERD = "blade_pottery_sherd"
BREWER_POTTERY_SHERD = "brewer_pottery_sherd"
BURN_POTTERY_SHERD = "burn_pottery_sherd"
DANGER_POTTERY_SHERD = "danger_pottery_sherd"
EXPLORER_POTTERY_SHERD = "explorer_pottery_sherd"
FLOW_POTTERY_SHERD = "flow_pottery_sherd"
FRIEND_POTTERY_SHERD = "friend_pottery_sherd"
GUSTER_POTTERY_SHERD = "guster_pottery_sherd"
HEARTBREAK_POTTERY_SHERD = "heartbreak_pottery_sherd"
HEART_POTTERY_SHERD = "heart_pottery_sherd"
HOWL_POTTERY_SHERD = "howl_pottery_sherd"
MINER_POTTERY_SHERD = "miner_pottery_sherd"
MOURNER_POTTERY_SHERD = "mourner_pottery_sherd"
PLENTY_POTTERY_SHERD = "plenty_pottery_sherd"
PRIZE_POTTERY_SHERD = "prize_pottery_sherd"
SCRAPE_POTTERY_SHERD = "scrape_pottery_sherd"
SHEAF_POTTERY_SHERD = "sheaf_pottery_sherd"
SHELTER_POTTERY_SHERD = "shelter_pottery_sherd"
SKULL_POTTERY_SHERD = "skull_pottery_sherd"
SNORT_POTTERY_SHERD = "snort_pottery_sherd"
POTTERY_SHERD_GROUP = [
    ANGLER_POTTERY_SHERD, ARCHER_POTTERY_SHERD, ARMS_UP_POTTERY_SHERD, BLADE_POTTERY_SHERD, BREWER_POTTERY_SHERD, BURN_POTTERY_SHERD, DANGER_POTTERY_SHERD, EXPLORER_POTTERY_SHERD, FLOW_POTTERY_SHERD, FRIEND_POTTERY_SHERD, GUSTER_POTTERY_SHERD, HEARTBREAK_POTTERY_SHERD, HEART_POTTERY_SHERD, HOWL_POTTERY_SHERD, MINER_POTTERY_SHERD, MOURNER_POTTERY_SHERD, PLENTY_POTTERY_SHERD, PRIZE_POTTERY_SHERD, SCRAPE_POTTERY_SHERD, SHEAF_POTTERY_SHERD, SHELTER_POTTERY_SHERD, SKULL_POTTERY_SHERD, SNORT_POTTERY_SHERD
]

PotterySherdInfo = namedtuple("PotterySherd", ['name', 'value', 'desc'])
pottery_sherds = {
    "ANGLER_POTTERY_SHERD": PotterySherdInfo("""Angler Pottery Sherd""", "angler_pottery_sherd", None),
    "ARCHER_POTTERY_SHERD": PotterySherdInfo("""Archer Pottery Sherd""", "archer_pottery_sherd", None),
    "ARMS_UP_POTTERY_SHERD": PotterySherdInfo("""Arms Up Pottery Sherd""", "arms_up_pottery_sherd", None),
    "BLADE_POTTERY_SHERD": PotterySherdInfo("""Blade Pottery Sherd""", "blade_pottery_sherd", None),
    "BREWER_POTTERY_SHERD": PotterySherdInfo("""Brewer Pottery Sherd""", "brewer_pottery_sherd", None),
    "BURN_POTTERY_SHERD": PotterySherdInfo("""Burn Pottery Sherd""", "burn_pottery_sherd", None),
    "DANGER_POTTERY_SHERD": PotterySherdInfo("""Danger Pottery Sherd""", "danger_pottery_sherd", None),
    "EXPLORER_POTTERY_SHERD": PotterySherdInfo("""Explorer Pottery Sherd""", "explorer_pottery_sherd", None),
    "FLOW_POTTERY_SHERD": PotterySherdInfo("""Flow Pottery Sherd""", "flow_pottery_sherd", None),
    "FRIEND_POTTERY_SHERD": PotterySherdInfo("""Friend Pottery Sherd""", "friend_pottery_sherd", None),
    "GUSTER_POTTERY_SHERD": PotterySherdInfo("""Guster Pottery Sherd""", "guster_pottery_sherd", None),
    "HEARTBREAK_POTTERY_SHERD": PotterySherdInfo("""Heartbreak Pottery Sherd""", "heartbreak_pottery_sherd", None),
    "HEART_POTTERY_SHERD": PotterySherdInfo("""Heart Pottery Sherd""", "heart_pottery_sherd", None),
    "HOWL_POTTERY_SHERD": PotterySherdInfo("""Howl Pottery Sherd""", "howl_pottery_sherd", None),
    "MINER_POTTERY_SHERD": PotterySherdInfo("""Miner Pottery Sherd""", "miner_pottery_sherd", None),
    "MOURNER_POTTERY_SHERD": PotterySherdInfo("""Mourner Pottery Sherd""", "mourner_pottery_sherd", None),
    "PLENTY_POTTERY_SHERD": PotterySherdInfo("""Plenty Pottery Sherd""", "plenty_pottery_sherd", None),
    "PRIZE_POTTERY_SHERD": PotterySherdInfo("""Prize Pottery Sherd""", "prize_pottery_sherd", None),
    "SCRAPE_POTTERY_SHERD": PotterySherdInfo("""Scrape Pottery Sherd""", "scrape_pottery_sherd", None),
    "SHEAF_POTTERY_SHERD": PotterySherdInfo("""Sheaf Pottery Sherd""", "sheaf_pottery_sherd", None),
    "SHELTER_POTTERY_SHERD": PotterySherdInfo("""Shelter Pottery Sherd""", "shelter_pottery_sherd", None),
    "SKULL_POTTERY_SHERD": PotterySherdInfo("""Skull Pottery Sherd""", "skull_pottery_sherd", None),
    "SNORT_POTTERY_SHERD": PotterySherdInfo("""Snort Pottery Sherd""", "snort_pottery_sherd", None),
}

for __k in tuple(pottery_sherds.keys()):
    v = pottery_sherds[__k]
    pottery_sherds[v.name] = v
    pottery_sherds[v.value] = v


def as_potterysherd(*values: StrOrArg) -> str | Tuple[str, ...]:
    return _as_things(POTTERY_SHERD_GROUP, __potterysherd_dups, *values)



# Discs
__disc_dups = {}
BLOCKS = "music_disc_blocks"
CAT = "music_disc_cat"
CHIRP = "music_disc_chirp"
CREATOR = "music_disc_creator"
CREATOR_MUSIC_BOX = "music_disc_creator_music_box"
ELEVEN = "music_disc_11"
FAR = "music_disc_far"
FIVE = "music_disc_5"
LAVA_CHICKEN = "music_disc_lava_chicken"
MALL = "music_disc_mall"
MELLOHI = "music_disc_mellohi"
OTHERSIDE = "music_disc_otherside"
PIGSTEP = "music_disc_pigstep"
PRECIPICE = "music_disc_precipice"
RELIC = "music_disc_relic"
STAL = "music_disc_stal"
STRAD = "music_disc_strad"
TEARS = "music_disc_tears"
THIRTEEN = "music_disc_13"
WAIT = "music_disc_wait"
WARD = "music_disc_ward"
DISC_GROUP = [
    BLOCKS, CAT, CHIRP, CREATOR, CREATOR_MUSIC_BOX, ELEVEN, FAR, FIVE, LAVA_CHICKEN, MALL, MELLOHI, OTHERSIDE, PIGSTEP, PRECIPICE, RELIC, STAL, STRAD, TEARS, THIRTEEN, WAIT, WARD
]

DiscInfo = namedtuple("Disc", ['name', 'value', 'desc', 'composer'])
discs = {
    "BLOCKS": DiscInfo("""blocks""", "music_disc_blocks", None, "C418"),
    "CAT": DiscInfo("""cat""", "music_disc_cat", None, "C418"),
    "CHIRP": DiscInfo("""chirp""", "music_disc_chirp", None, "C418"),
    "CREATOR": DiscInfo("""Creator""", "music_disc_creator", None, "Lena Raine"),
    "CREATOR_MUSIC_BOX": DiscInfo("""Creator (Music Box)""", "music_disc_creator_music_box", None, "Lena Raine"),
    "ELEVEN": DiscInfo("""eleven""", "music_disc_11", None, "C418"),
    "FAR": DiscInfo("""far""", "music_disc_far", None, "C418"),
    "FIVE": DiscInfo("""five""", "music_disc_5", None, "Samuel Åberg"),
    "LAVA_CHICKEN": DiscInfo("""Lava Chicken""", "music_disc_lava_chicken", None, "Hyper Potions"),
    "MALL": DiscInfo("""mall""", "music_disc_mall", None, "C418"),
    "MELLOHI": DiscInfo("""mellohi""", "music_disc_mellohi", None, "C418"),
    "OTHERSIDE": DiscInfo("""otherside""", "music_disc_otherside", None, "Lena Raine"),
    "PIGSTEP": DiscInfo("""Pigstep""", "music_disc_pigstep", None, "Lena Raine"),
    "PRECIPICE": DiscInfo("""Precipice""", "music_disc_precipice", None, "Aaron Cherof"),
    "RELIC": DiscInfo("""Relic""", "music_disc_relic", None, "Aaron Cherof"),
    "STAL": DiscInfo("""stal""", "music_disc_stal", None, "C418"),
    "STRAD": DiscInfo("""strad""", "music_disc_strad", None, "C418"),
    "TEARS": DiscInfo("""Tears""", "music_disc_tears", None, "Amos Roddy"),
    "THIRTEEN": DiscInfo("""thirteen""", "music_disc_13", None, "C418"),
    "WAIT": DiscInfo("""wait""", "music_disc_wait", None, "C418"),
    "WARD": DiscInfo("""ward""", "music_disc_ward", None, "C418"),
}

for __k in tuple(discs.keys()):
    v = discs[__k]
    discs[v.name] = v
    discs[v.value] = v


def as_disc(*values: StrOrArg) -> str | Tuple[str, ...]:
    return _as_things(DISC_GROUP, __disc_dups, *values)



# Paintings
__painting_dups = {}
ALBANIAN = "alban"
BACKYARD = "backyard"
BAROQUE = "baroque"
BONJOUR_MONSIEUR_COURBET = "courbet"
BOUQUET = "bouquet"
BUST = "bust"
CAVEBIRD = "cavebird"
CHANGING = "changing"
COTAN = "cotan"
CREEBET = "creebet"
DENNIS = "dennis"
DE_AZTEC = "aztec"
DE_AZTEC_2 = "aztec2"
EARTH = "earth"
ENDBOSS = "endboss"
FERN = "fern"
FIGHTERS = "fighters"
FINDING = "finding"
FIRE = "fire"
GRAHAM = "graham"
HUMBLE = "humble"
KEBAB_MED_TRE_PEPPERONI = "kebab"
KONG = "donkey_kong"
LOWMIST = "lowmist"
MATCH = "match"
MEDITATIVE = "meditative"
MORTAL_COIL = "skeleton"
ORB = "orb"
OWLEMONS = "owlemons"
PARADISTRAD = "plant"
PASSAGE = "passage"
PIGSCENE = "pigscene"
POINTER = "pointer"
POND = "pond"
PRAIRIE_RIDE = "prairie_ride"
SEASIDE = "sea"
SKULL_AND_ROSES = "skull_and_roses"
SKULL_ON_FIRE = "burning_skull"
SUNFLOWERS = "sunflowers"
SUNSET_DENSE = "sunset"
TARGET_SUCCESSFULLY_BOMBED = "bomb"
THE_POOL = "pool"
THE_STAGE_IS_SET = "stage"
__painting_dups["the_void"] = "void"
TIDES = "tides"
UNPACKED = "unpacked"
WANDERER = "wanderer"
WASTELAND = "wasteland"
WATER = "water"
WIND = "wind"
PAINTING_GROUP = [
    ALBANIAN, BACKYARD, BAROQUE, BONJOUR_MONSIEUR_COURBET, BOUQUET, BUST, CAVEBIRD, CHANGING, COTAN, CREEBET, DENNIS, DE_AZTEC, DE_AZTEC_2, EARTH, ENDBOSS, FERN, FIGHTERS, FINDING, FIRE, GRAHAM, HUMBLE, KEBAB_MED_TRE_PEPPERONI, KONG, LOWMIST, MATCH, MEDITATIVE, MORTAL_COIL, ORB, OWLEMONS, PARADISTRAD, PASSAGE, PIGSCENE, POINTER, POND, PRAIRIE_RIDE, SEASIDE, SKULL_AND_ROSES, SKULL_ON_FIRE, SUNFLOWERS, SUNSET_DENSE, TARGET_SUCCESSFULLY_BOMBED, THE_POOL, THE_STAGE_IS_SET, "void", TIDES, UNPACKED, WANDERER, WASTELAND, WATER, WIND, "wither"
]

PaintingInfo = namedtuple("Painting", ['name', 'value', 'desc', 'artist', 'size'])
paintings = {
    "ALBANIAN": PaintingInfo("""Albanian""", "alban", None, "Kristoffer Zetterstrand", (1, 1)),
    "BACKYARD": PaintingInfo("""Backyard""", "backyard", None, "Kristoffer Zetterstrand", (3, 4)),
    "BAROQUE": PaintingInfo("""Baroque""", "baroque", None, "Sarah Boeving", (2, 2)),
    "BONJOUR_MONSIEUR_COURBET": PaintingInfo("""Bonjour Monsieur Courbet""", "courbet", None, "Kristoffer Zetterstrand", (2, 1)),
    "BOUQUET": PaintingInfo("""Bouquet""", "bouquet", None, "Kristoffer Zetterstrand", (3, 3)),
    "BUST": PaintingInfo("""Bust""", "bust", None, "Kristoffer Zetterstrand", (2, 2)),
    "CAVEBIRD": PaintingInfo("""Cavebird""", "cavebird", None, "Kristoffer Zetterstrand", (3, 3)),
    "CHANGING": PaintingInfo("""Changing""", "changing", None, "Kristoffer Zetterstrand", (4, 2)),
    "COTAN": PaintingInfo("""Cotán""", "cotan", None, "Kristoffer Zetterstrand", (3, 3)),
    "CREEBET": PaintingInfo("""Creebet""", "creebet", None, "Kristoffer Zetterstrand", (2, 1)),
    "DENNIS": PaintingInfo("""Dennis""", "dennis", None, "Sarah Boeving", (3, 3)),
    "DE_AZTEC": PaintingInfo("""de_aztec""", "aztec", None, "Kristoffer Zetterstrand", (1, 1)),
    "DE_AZTEC_2": PaintingInfo("""de_aztec 2""", "aztec2", None, "Kristoffer Zetterstrand", (1, 1)),
    "EARTH": PaintingInfo("""Earth""", "earth", None, "", (2, 2)),
    "ENDBOSS": PaintingInfo("""Endboss""", "endboss", None, "Kristoffer Zetterstrand", (3, 3)),
    "FERN": PaintingInfo("""Fern""", "fern", None, "Kristoffer Zetterstrand", (3, 3)),
    "FIGHTERS": PaintingInfo("""Fighters""", "fighters", None, "Kristoffer Zetterstrand", (4, 2)),
    "FINDING": PaintingInfo("""Finding""", "finding", None, "Kristoffer Zetterstrand", (4, 2)),
    "FIRE": PaintingInfo("""Fire""", "fire", None, "", (2, 2)),
    "GRAHAM": PaintingInfo("""Graham""", "graham", None, "Kristoffer Zetterstrand", (1, 2)),
    "HUMBLE": PaintingInfo("""Humble""", "humble", None, "Sarah Boeving", (2, 2)),
    "KEBAB_MED_TRE_PEPPERONI": PaintingInfo("""Kebab med tre pepperoni""", "kebab", None, "Kristoffer Zetterstrand", (1, 1)),
    "KONG": PaintingInfo("""Kong""", "donkey_kong", None, "Kristoffer Zetterstrand", (4, 3)),
    "LOWMIST": PaintingInfo("""Lowmist""", "lowmist", None, "Kristoffer Zetterstrand", (4, 2)),
    "MATCH": PaintingInfo("""Match""", "match", None, "Kristoffer Zetterstrand", (2, 2)),
    "MEDITATIVE": PaintingInfo("""Meditative""", "meditative", None, "Sarah Boeving", (1, 1)),
    "MORTAL_COIL": PaintingInfo("""Mortal Coil""", "skeleton", None, "Kristoffer Zetterstrand", (4, 3)),
    "ORB": PaintingInfo("""Orb""", "orb", None, "Kristoffer Zetterstrand", (4, 4)),
    "OWLEMONS": PaintingInfo("""Owlemons""", "owlemons", None, "Kristoffer Zetterstrand", (3, 3)),
    "PARADISTRAD": PaintingInfo("""Paradisträd""", "plant", None, "Kristoffer Zetterstrand", (1, 1)),
    "PASSAGE": PaintingInfo("""Passage""", "passage", None, "Kristoffer Zetterstrand", (4, 2)),
    "PIGSCENE": PaintingInfo("""Pigscene""", "pigscene", None, "Kristoffer Zetterstrand", (4, 4)),
    "POINTER": PaintingInfo("""Pointer""", "pointer", None, "Kristoffer Zetterstrand", (4, 4)),
    "POND": PaintingInfo("""Pond""", "pond", None, "Kristoffer Zetterstrand", (3, 4)),
    "PRAIRIE_RIDE": PaintingInfo("""Prairie Ride""", "prairie_ride", None, "Sarah Boeving", (1, 2)),
    "SEASIDE": PaintingInfo("""Seaside""", "sea", None, "Kristoffer Zetterstrand", (2, 1)),
    "SKULL_AND_ROSES": PaintingInfo("""Skull and Roses""", "skull_and_roses", None, "Kristoffer Zetterstrand", (2, 2)),
    "SKULL_ON_FIRE": PaintingInfo("""Skull On Fire""", "burning_skull", None, "Kristoffer Zetterstrand", (4, 4)),
    "SUNFLOWERS": PaintingInfo("""Sunflowers""", "sunflowers", None, "Kristoffer Zetterstrand", (3, 3)),
    "SUNSET_DENSE": PaintingInfo("""sunset_dense""", "sunset", None, "Kristoffer Zetterstrand", (2, 1)),
    "TARGET_SUCCESSFULLY_BOMBED": PaintingInfo("""Target Successfully Bombed""", "bomb", None, "Kristoffer Zetterstrand", (1, 1)),
    "THE_POOL": PaintingInfo("""The Pool""", "pool", None, "Kristoffer Zetterstrand", (2, 1)),
    "THE_STAGE_IS_SET": PaintingInfo("""The Stage Is Set""", "stage", None, "Kristoffer Zetterstrand", (2, 2)),
    "THE_VOID": PaintingInfo("""The void""", "void", None, "Kristoffer Zetterstrand", (2, 2)),
    "TIDES": PaintingInfo("""Tides""", "tides", None, "Kristoffer Zetterstrand", (3, 3)),
    "UNPACKED": PaintingInfo("""Unpacked""", "unpacked", None, "Sarah Boeving", (4, 4)),
    "WANDERER": PaintingInfo("""Wanderer""", "wanderer", None, "Kristoffer Zetterstrand", (1, 2)),
    "WASTELAND": PaintingInfo("""Wasteland""", "wasteland", None, "Kristoffer Zetterstrand", (1, 1)),
    "WATER": PaintingInfo("""Water""", "water", None, "", (2, 2)),
    "WIND": PaintingInfo("""Wind""", "wind", None, "", (2, 2)),
    "WITHER": PaintingInfo("""Wither""", "wither", None, "", (2, 2)),
}

for __k in tuple(paintings.keys()):
    v = paintings[__k]
    paintings[v.name] = v
    paintings[v.value] = v


def as_painting(*values: StrOrArg) -> str | Tuple[str, ...]:
    return _as_things(PAINTING_GROUP, __painting_dups, *values)

