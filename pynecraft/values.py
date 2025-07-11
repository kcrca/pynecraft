from collections import namedtuple
from typing import Tuple

from pynecraft.base import StrOrArg, _in_group, de_arg, is_arg


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



# TeamOptions
# Derived from https://minecraft.wiki/Commands/team, 2025-06-30T18:19:21-07:00
__teamoption_dups = {}
__teamoption_dups["displayname"] = "displayName"
COLOR = "color"
FRIENDLY_FIRE = "friendlyFire"
SEE_FRIENDLY_INVISIBLES = "seeFriendlyInvisibles"
NAMETAG_VISIBILITY = "nametagVisibility"
DEATH_MESSAGE_VISIBILITY = "deathMessageVisibility"
COLLISION_RULE = "collisionRule"
PREFIX = "prefix"
SUFFIX = "suffix"
TEAM_OPTION_GROUP = [
    "displayName", COLOR, FRIENDLY_FIRE, SEE_FRIENDLY_INVISIBLES, NAMETAG_VISIBILITY, DEATH_MESSAGE_VISIBILITY, COLLISION_RULE, PREFIX, SUFFIX
]

TeamOptionInfo = namedtuple("TeamOption", ['name', 'value', 'desc', 'type'])
team_options = {
    "DISPLAY_NAME": TeamOptionInfo("""display Name""", "displayName", """Sets the display name of the team.""", 'Nbt'),
    "COLOR": TeamOptionInfo("""color""", "color", """Decides the color of the team and players in chat, above their head, on the Tab menu, and on the sidebar. Also changes the color of the outline of the entities caused by the Glowing effect.""", 'Nbt'),
    "FRIENDLY_FIRE": TeamOptionInfo("""friendly Fire""", "friendlyFire", """Enables/Disables players inflicting damage to each other when on the same team. (Note: players can still inflict status effects on each other.) Does not affect some non-player entities in a team.""", bool),
    "SEE_FRIENDLY_INVISIBLES": TeamOptionInfo("""see Friendly Invisibles""", "seeFriendlyInvisibles", """Decides whether invisible players are semi-transparent or completely invisible to other players on their team.""", bool),
    "NAMETAG_VISIBILITY": TeamOptionInfo("""nametag Visibility""", "nametagVisibility", """Decides whose name tags above their heads can be seen.""", ['never', 'hideForOtherTeams', 'hideForOwnTeam', 'always']),
    "DEATH_MESSAGE_VISIBILITY": TeamOptionInfo("""death Message Visibility""", "deathMessageVisibility", """Controls the visibility of death messages for players.""", ['never', 'hideForOtherTeams', 'hideForOwnTeam', 'always']),
    "COLLISION_RULE": TeamOptionInfo("""collision Rule""", "collisionRule", """Controls the way entities on the team collide with other entities.""", ['always', 'never', 'pushOtherTeams', 'pushOwnTeam']),
    "PREFIX": TeamOptionInfo("""prefix""", "prefix", """Modifies the prefix that displays at the beginning of players' names.""", 'Nbt'),
    "SUFFIX": TeamOptionInfo("""suffix""", "suffix", """Modifies the suffix that displays at the end of players' names.""", 'Nbt'),
}

for __k in tuple(team_options.keys()):
    v = team_options[__k]
    team_options[v.name] = v
    team_options[v.value] = v


def as_teamoption(*values: StrOrArg) -> str | Tuple[str, ...]:
    return _as_things(TEAM_OPTION_GROUP, __teamoption_dups, *values)



# Patterns
# Derived from https://minecraft.wiki/Banner/Patterns, 2025-06-30T18:19:21-07:00
__pattern_dups = {}
BASE = "base"
STRIPE_BOTTOM = "stripe_bottom"
STRIPE_TOP = "stripe_top"
STRIPE_LEFT = "stripe_left"
STRIPE_RIGHT = "stripe_right"
STRIPE_CENTER = "stripe_center"
STRIPE_MIDDLE = "stripe_middle"
STRIPE_DOWNRIGHT = "stripe_downright"
STRIPE_DOWNLEFT = "stripe_downleft"
SMALL_STRIPES = "small_stripes"
CROSS = "cross"
STRAIGHT_CROSS = "straight_cross"
DIAGONAL_LEFT = "diagonal_left"
DIAGONAL_RIGHT = "diagonal_right"
DIAGONAL_UP_LEFT = "diagonal_up_left"
DIAGONAL_UP_RIGHT = "diagonal_up_right"
HALF_VERTICAL = "half_vertical"
HALF_VERTICAL_RIGHT = "half_vertical_right"
HALF_HORIZONTAL = "half_horizontal"
HALF_HORIZONTAL_BOTTOM = "half_horizontal_bottom"
SQUARE_BOTTOM_LEFT = "square_bottom_left"
SQUARE_BOTTOM_RIGHT = "square_bottom_right"
SQUARE_TOP_LEFT = "square_top_left"
SQUARE_TOP_RIGHT = "square_top_right"
TRIANGLE_BOTTOM = "triangle_bottom"
TRIANGLE_TOP = "triangle_top"
TRIANGLES_BOTTOM = "triangles_bottom"
TRIANGLES_TOP = "triangles_top"
CIRCLE = "circle"
RHOMBUS = "rhombus"
BORDER = "border"
CURLY_BORDER = "curly_border"
BRICKS = "bricks"
GRADIENT = "gradient"
GRADIENT_UP = "gradient_up"
CREEPER = "creeper"
SKULL = "skull"
FLOWER = "flower"
MOJANG = "mojang"
GLOBE = "globe"
PIGLIN = "piglin"
FLOW = "flow"
GUSTER = "guster"
PATTERN_GROUP = [
    BASE, STRIPE_BOTTOM, STRIPE_TOP, STRIPE_LEFT, STRIPE_RIGHT, STRIPE_CENTER, STRIPE_MIDDLE, STRIPE_DOWNRIGHT, STRIPE_DOWNLEFT, SMALL_STRIPES, CROSS, STRAIGHT_CROSS, DIAGONAL_LEFT, DIAGONAL_RIGHT, DIAGONAL_UP_LEFT, DIAGONAL_UP_RIGHT, HALF_VERTICAL, HALF_VERTICAL_RIGHT, HALF_HORIZONTAL, HALF_HORIZONTAL_BOTTOM, SQUARE_BOTTOM_LEFT, SQUARE_BOTTOM_RIGHT, SQUARE_TOP_LEFT, SQUARE_TOP_RIGHT, TRIANGLE_BOTTOM, TRIANGLE_TOP, TRIANGLES_BOTTOM, TRIANGLES_TOP, CIRCLE, RHOMBUS, BORDER, CURLY_BORDER, BRICKS, GRADIENT, GRADIENT_UP, CREEPER, SKULL, FLOWER, MOJANG, GLOBE, PIGLIN, FLOW, GUSTER
]

PatternInfo = namedtuple("Pattern", ['name', 'value', 'desc'])
patterns = {
    "BASE": PatternInfo("""Base""", "base", """Fully color Field."""),
    "STRIPE_BOTTOM": PatternInfo("""Stripe Bottom""", "stripe_bottom", """Base."""),
    "STRIPE_TOP": PatternInfo("""Stripe Top""", "stripe_top", """Chief."""),
    "STRIPE_LEFT": PatternInfo("""Stripe Left""", "stripe_left", """Pale Dexter."""),
    "STRIPE_RIGHT": PatternInfo("""Stripe Right""", "stripe_right", """Pale Sinister."""),
    "STRIPE_CENTER": PatternInfo("""Stripe Center""", "stripe_center", """Pale."""),
    "STRIPE_MIDDLE": PatternInfo("""Stripe Middle""", "stripe_middle", """Fess."""),
    "STRIPE_DOWNRIGHT": PatternInfo("""Stripe Downright""", "stripe_downright", """Bend."""),
    "STRIPE_DOWNLEFT": PatternInfo("""Stripe Downleft""", "stripe_downleft", """Bend Sinister."""),
    "SMALL_STRIPES": PatternInfo("""Small Stripes""", "small_stripes", """Paly."""),
    "CROSS": PatternInfo("""Cross""", "cross", """Saltire."""),
    "STRAIGHT_CROSS": PatternInfo("""Straight Cross""", "straight_cross", """Cross."""),
    "DIAGONAL_LEFT": PatternInfo("""Diagonal Left""", "diagonal_left", """Per Bend Sinister."""),
    "DIAGONAL_RIGHT": PatternInfo("""Diagonal Right""", "diagonal_right", """Per Bend."""),
    "DIAGONAL_UP_LEFT": PatternInfo("""Diagonal Up Left""", "diagonal_up_left", """Per Bend Inverted."""),
    "DIAGONAL_UP_RIGHT": PatternInfo("""Diagonal Up Right""", "diagonal_up_right", """Per Bend Sinister Inverted."""),
    "HALF_VERTICAL": PatternInfo("""Half Vertical""", "half_vertical", """Per Pale."""),
    "HALF_VERTICAL_RIGHT": PatternInfo("""Half Vertical Right""", "half_vertical_right", """Per Pale Inverted."""),
    "HALF_HORIZONTAL": PatternInfo("""Half Horizontal""", "half_horizontal", """Per Fess."""),
    "HALF_HORIZONTAL_BOTTOM": PatternInfo("""Half Horizontal Bottom""", "half_horizontal_bottom", """Per Fess Inverted."""),
    "SQUARE_BOTTOM_LEFT": PatternInfo("""Square Bottom Left""", "square_bottom_left", """Base Dexter Canton."""),
    "SQUARE_BOTTOM_RIGHT": PatternInfo("""Square Bottom Right""", "square_bottom_right", """Base Sinister Canton."""),
    "SQUARE_TOP_LEFT": PatternInfo("""Square Top Left""", "square_top_left", """Chief Dexter Canton."""),
    "SQUARE_TOP_RIGHT": PatternInfo("""Square Top Right""", "square_top_right", """Chief Sinister Canton."""),
    "TRIANGLE_BOTTOM": PatternInfo("""Triangle Bottom""", "triangle_bottom", """Chevron."""),
    "TRIANGLE_TOP": PatternInfo("""Triangle Top""", "triangle_top", """Inverted Chevron."""),
    "TRIANGLES_BOTTOM": PatternInfo("""Triangles Bottom""", "triangles_bottom", """Base Indented."""),
    "TRIANGLES_TOP": PatternInfo("""Triangles Top""", "triangles_top", """Chief Indented."""),
    "CIRCLE": PatternInfo("""Circle""", "circle", """Roundel."""),
    "RHOMBUS": PatternInfo("""Rhombus""", "rhombus", """Lozenge."""),
    "BORDER": PatternInfo("""Border""", "border", """Bordure."""),
    "CURLY_BORDER": PatternInfo("""Curly Border""", "curly_border", """Bordure Indented."""),
    "BRICKS": PatternInfo("""Bricks""", "bricks", """Field Masoned."""),
    "GRADIENT": PatternInfo("""Gradient""", "gradient", """Gradient."""),
    "GRADIENT_UP": PatternInfo("""Gradient Up""", "gradient_up", """Base Gradient."""),
    "CREEPER": PatternInfo("""Creeper""", "creeper", """Creeper Charge."""),
    "SKULL": PatternInfo("""Skull""", "skull", """Skull Charge."""),
    "FLOWER": PatternInfo("""Flower""", "flower", """Flower Charge."""),
    "MOJANG": PatternInfo("""Mojang""", "mojang", """Thing."""),
    "GLOBE": PatternInfo("""Globe""", "globe", """Globe."""),
    "PIGLIN": PatternInfo("""Piglin""", "piglin", """Snout."""),
    "FLOW": PatternInfo("""Flow""", "flow", """Flow."""),
    "GUSTER": PatternInfo("""Guster""", "guster", """Guster."""),
}

for __k in tuple(patterns.keys()):
    v = patterns[__k]
    patterns[v.name] = v
    patterns[v.value] = v


def as_pattern(*values: StrOrArg) -> str | Tuple[str, ...]:
    return _as_things(PATTERN_GROUP, __pattern_dups, *values)



# Advancements
# Derived from https://minecraft.wiki/Advancement#List_of_advancements, 2025-06-30T18:19:21-07:00
__advancement_dups = {}
MINECRAFT = "story/root"
STONE_AGE = "story/mine_stone"
GETTING_AN_UPGRADE = "story/upgrade_tools"
ACQUIRE_HARDWARE = "story/smelt_iron"
SUIT_UP = "story/obtain_armor"
HOT_STUFF = "story/lava_bucket"
ISNT_IT_IRON_PICK = "story/iron_tools"
NOT_TODAY_THANK_YOU = "story/deflect_arrow"
ICE_BUCKET_CHALLENGE = "story/form_obsidian"
DIAMONDS = "story/mine_diamond"
WE_NEED_TO_GO_DEEPER = "story/enter_the_nether"
COVER_ME_WITH_DIAMONDS = "story/shiny_gear"
ENCHANTER = "story/enchant_item"
ZOMBIE_DOCTOR = "story/cure_zombie_villager"
EYE_SPY = "story/follow_ender_eye"
ENTER_THE_END = "story/enter_the_end"
__advancement_dups["nether"] = "nether/root"
RETURN_TO_SENDER = "nether/return_to_sender"
THOSE_WERE_THE_DAYS = "nether/find_bastion"
HIDDEN_IN_THE_DEPTHS = "nether/obtain_ancient_debris"
SUBSPACE_BUBBLE = "nether/fast_travel"
A_TERRIBLE_FORTRESS = "nether/find_fortress"
WHO_IS_CUTTING_ONIONS = "nether/obtain_crying_obsidian"
OH_SHINY = "nether/distract_piglin"
THIS_BOAT_HAS_LEGS = "nether/ride_strider"
UNEASY_ALLIANCE = "nether/uneasy_alliance"
WAR_PIGS = "nether/loot_bastion"
COVER_ME_IN_DEBRIS = "nether/netherite_armor"
SPOOKY_SCARY_SKELETON = "nether/get_wither_skull"
INTO_FIRE = "nether/obtain_blaze_rod"
NOT_QUITE_NINE_LIVES = "nether/charge_respawn_anchor"
FEELS_LIKE_HOME = "nether/ride_strider_in_overworld_lava"
HOT_TOURIST_DESTINATIONS = "nether/explore_nether"
WITHERING_HEIGHTS = "nether/summon_wither"
LOCAL_BREWERY = "nether/brew_potion"
BRING_HOME_THE_BEACON = "nether/create_beacon"
A_FURIOUS_COCKTAIL = "nether/all_potions"
BEACONATOR = "nether/create_full_beacon"
HOW_DID_WE_GET_HERE = "nether/all_effects"
__advancement_dups["the_end"] = "end/root"
FREE_THE_END = "end/kill_dragon"
THE_NEXT_GENERATION = "end/dragon_egg"
REMOTE_GETAWAY = "end/enter_end_gateway"
THE_END_AGAIN = "end/respawn_dragon"
YOU_NEED_A_MINT = "end/dragon_breath"
THE_CITY_AT_THE_END_OF_THE_GAME = "end/find_end_city"
SKYS_THE_LIMIT = "end/elytra"
GREAT_VIEW_FROM_UP_HERE = "end/levitate"
__advancement_dups["adventure"] = "adventure/root"
HEART_TRANSPLANTER = "adventure/heart_transplanter"
VOLUNTARY_EXILE = "adventure/voluntary_exile"
COUNTRY_LODE_TAKE_ME_HOME = "adventure/use_lodestone"
IS_IT_A_BIRD = "adventure/spyglass_at_parrot"
MONSTER_HUNTER = "adventure/kill_a_mob"
THE_POWER_OF_BOOKS = "adventure/read_power_of_chiseled_bookshelf"
WHAT_A_DEAL = "adventure/trade"
CRAFTING_A_NEW_LOOK = "adventure/trim_with_any_armor_pattern"
STICKY_SITUATION = "adventure/honey_block_slide"
OL_BETSY = "adventure/ol_betsy"
SURGE_PROTECTOR = "adventure/lightning_rod_with_villager_no_fire"
CAVES__CLIFFS = "adventure/fall_from_world_height"
RESPECTING_THE_REMNANTS = "adventure/salvage_sherd"
SNEAK_100 = "adventure/avoid_vibration"
SWEET_DREAMS = "adventure/sleep_in_bed"
HERO_OF_THE_VILLAGE = "adventure/hero_of_the_village"
IS_IT_A_BALLOON = "adventure/spyglass_at_ghast"
A_THROWAWAY_JOKE = "adventure/throw_trident"
IT_SPREADS = "adventure/kill_mob_near_sculk_catalyst"
TAKE_AIM = "adventure/shoot_arrow"
MONSTERS_HUNTED = "adventure/kill_all_mobs"
POSTMORTAL = "adventure/totem_of_undying"
HIRED_HELP = "adventure/summon_iron_golem"
STAR_TRADER = "adventure/trade_at_world_height"
SMITHING_WITH_STYLE = "adventure/trim_with_all_exclusive_armor_patterns"
TWO_BIRDS_ONE_ARROW = "adventure/two_birds_one_arrow"
WHOS_THE_PILLAGER_NOW = "adventure/whos_the_pillager_now"
ARBALISTIC = "adventure/arbalistic"
CAREFUL_RESTORATION = "adventure/craft_decorated_pot_using_only_sherds"
ADVENTURING_TIME = "adventure/adventuring_time"
SOUND_OF_MUSIC = "adventure/play_jukebox_in_meadows"
LIGHT_AS_A_RABBIT = "adventure/walk_on_powder_snow_with_leather_boots"
IS_IT_A_PLANE = "adventure/spyglass_at_dragon"
VERY_VERY_FRIGHTENING = "adventure/very_very_frightening"
SNIPER_DUEL = "adventure/sniper_duel"
BULLSEYE = "adventure/bullseye"
ISNT_IT_SCUTE = "adventure/brush_armadillo"
MINECRAFT_TRIALS_EDITION = "adventure/minecraft_trials_edition"
CRAFTERS_CRAFTING_CRAFTERS = "adventure/crafters_crafting_crafters"
LIGHTEN_UP = "adventure/lighten_up"
WHO_NEEDS_ROCKETS = "adventure/who_needs_rockets"
UNDER_LOCK_AND_KEY = "adventure/under_lock_and_key"
REVAULTING = "adventure/revaulting"
BLOWBACK = "adventure/blowback"
OVEROVERKILL = "adventure/overoverkill"
__advancement_dups["husbandry"] = "husbandry/root"
STAY_HYDRATED = "husbandry/place_dried_ghast_in_water"
BEE_OUR_GUEST = "husbandry/safely_harvest_honey"
THE_PARROTS_AND_THE_BATS = "husbandry/breed_an_animal"
YOUVE_GOT_A_FRIEND_IN_ME = "husbandry/allay_deliver_item_to_player"
WHATEVER_FLOATS_YOUR_GOAT = "husbandry/ride_a_boat_with_a_goat"
BEST_FRIENDS_FOREVER = "husbandry/tame_an_animal"
GLOW_AND_BEHOLD = "husbandry/make_a_sign_glow"
FISHY_BUSINESS = "husbandry/fishy_business"
TOTAL_BEELOCATION = "husbandry/silk_touch_nest"
BUKKIT_BUKKIT = "husbandry/tadpole_in_a_bucket"
SMELLS_INTERESTING = "husbandry/obtain_sniffer_egg"
A_SEEDY_PLACE = "husbandry/plant_seed"
WAX_ON = "husbandry/wax_on"
TWO_BY_TWO = "husbandry/bred_all_animals"
BIRTHDAY_SONG = "husbandry/allay_deliver_cake_to_note_block"
A_COMPLETE_CATALOGUE = "husbandry/complete_catalogue"
TACTICAL_FISHING = "husbandry/tactical_fishing"
WHEN_THE_SQUAD_HOPS_INTO_TOWN = "husbandry/leash_all_frog_variants"
LITTLE_SNIFFS = "husbandry/feed_snifflet"
A_BALANCED_DIET = "husbandry/balanced_diet"
SERIOUS_DEDICATION = "husbandry/obtain_netherite_hoe"
WAX_OFF = "husbandry/wax_off"
THE_CUTEST_PREDATOR = "husbandry/axolotl_in_a_bucket"
WITH_OUR_POWERS_COMBINED = "husbandry/froglights"
PLANTING_THE_PAST = "husbandry/plant_any_sniffer_seed"
THE_HEALING_POWER_OF_FRIENDSHIP = "husbandry/kill_axolotl_target"
GOOD_AS_NEW = "husbandry/repair_wolf_armor"
THE_WHOLE_PACK = "husbandry/whole_pack"
SHEAR_BRILLIANCE = "husbandry/remove_wolf_armor"
ADVANCEMENT_GROUP = [
    MINECRAFT, STONE_AGE, GETTING_AN_UPGRADE, ACQUIRE_HARDWARE, SUIT_UP, HOT_STUFF, ISNT_IT_IRON_PICK, NOT_TODAY_THANK_YOU, ICE_BUCKET_CHALLENGE, DIAMONDS, WE_NEED_TO_GO_DEEPER, COVER_ME_WITH_DIAMONDS, ENCHANTER, ZOMBIE_DOCTOR, EYE_SPY, ENTER_THE_END, "nether/root", RETURN_TO_SENDER, THOSE_WERE_THE_DAYS, HIDDEN_IN_THE_DEPTHS, SUBSPACE_BUBBLE, A_TERRIBLE_FORTRESS, WHO_IS_CUTTING_ONIONS, OH_SHINY, THIS_BOAT_HAS_LEGS, UNEASY_ALLIANCE, WAR_PIGS, COVER_ME_IN_DEBRIS, SPOOKY_SCARY_SKELETON, INTO_FIRE, NOT_QUITE_NINE_LIVES, FEELS_LIKE_HOME, HOT_TOURIST_DESTINATIONS, WITHERING_HEIGHTS, LOCAL_BREWERY, BRING_HOME_THE_BEACON, A_FURIOUS_COCKTAIL, BEACONATOR, HOW_DID_WE_GET_HERE, "end/root", FREE_THE_END, THE_NEXT_GENERATION, REMOTE_GETAWAY, THE_END_AGAIN, YOU_NEED_A_MINT, THE_CITY_AT_THE_END_OF_THE_GAME, SKYS_THE_LIMIT, GREAT_VIEW_FROM_UP_HERE, "adventure/root", HEART_TRANSPLANTER, VOLUNTARY_EXILE, COUNTRY_LODE_TAKE_ME_HOME, IS_IT_A_BIRD, MONSTER_HUNTER, THE_POWER_OF_BOOKS, WHAT_A_DEAL, CRAFTING_A_NEW_LOOK, STICKY_SITUATION, OL_BETSY, SURGE_PROTECTOR, CAVES__CLIFFS, RESPECTING_THE_REMNANTS, SNEAK_100, SWEET_DREAMS, HERO_OF_THE_VILLAGE, IS_IT_A_BALLOON, A_THROWAWAY_JOKE, IT_SPREADS, TAKE_AIM, MONSTERS_HUNTED, POSTMORTAL, HIRED_HELP, STAR_TRADER, SMITHING_WITH_STYLE, TWO_BIRDS_ONE_ARROW, WHOS_THE_PILLAGER_NOW, ARBALISTIC, CAREFUL_RESTORATION, ADVENTURING_TIME, SOUND_OF_MUSIC, LIGHT_AS_A_RABBIT, IS_IT_A_PLANE, VERY_VERY_FRIGHTENING, SNIPER_DUEL, BULLSEYE, ISNT_IT_SCUTE, MINECRAFT_TRIALS_EDITION, CRAFTERS_CRAFTING_CRAFTERS, LIGHTEN_UP, WHO_NEEDS_ROCKETS, UNDER_LOCK_AND_KEY, REVAULTING, BLOWBACK, OVEROVERKILL, "husbandry/root", STAY_HYDRATED, BEE_OUR_GUEST, THE_PARROTS_AND_THE_BATS, YOUVE_GOT_A_FRIEND_IN_ME, WHATEVER_FLOATS_YOUR_GOAT, BEST_FRIENDS_FOREVER, GLOW_AND_BEHOLD, FISHY_BUSINESS, TOTAL_BEELOCATION, BUKKIT_BUKKIT, SMELLS_INTERESTING, A_SEEDY_PLACE, WAX_ON, TWO_BY_TWO, BIRTHDAY_SONG, A_COMPLETE_CATALOGUE, TACTICAL_FISHING, WHEN_THE_SQUAD_HOPS_INTO_TOWN, LITTLE_SNIFFS, A_BALANCED_DIET, SERIOUS_DEDICATION, WAX_OFF, THE_CUTEST_PREDATOR, WITH_OUR_POWERS_COMBINED, PLANTING_THE_PAST, THE_HEALING_POWER_OF_FRIENDSHIP, GOOD_AS_NEW, THE_WHOLE_PACK, SHEAR_BRILLIANCE
]

AdvancementInfo = namedtuple("Advancement", ['name', 'value', 'desc'])
advancements = {
    "MINECRAFT": AdvancementInfo("""Minecraft""", "story/root", """The heart and story of the game."""),
    "STONE_AGE": AdvancementInfo("""Stone Age""", "story/mine_stone", """Mine Stone with your new Pickaxe."""),
    "GETTING_AN_UPGRADE": AdvancementInfo("""Getting an Upgrade""", "story/upgrade_tools", """Construct a better Pickaxe."""),
    "ACQUIRE_HARDWARE": AdvancementInfo("""Acquire Hardware""", "story/smelt_iron", """Smelt an Iron Ingot."""),
    "SUIT_UP": AdvancementInfo("""Suit Up""", "story/obtain_armor", """Protect yourself with a piece of iron armor."""),
    "HOT_STUFF": AdvancementInfo("""Hot Stuff""", "story/lava_bucket", """Fill a Bucket with lava."""),
    "ISNT_IT_IRON_PICK": AdvancementInfo("""Isn't It Iron Pick""", "story/iron_tools", """Upgrade your Pickaxe."""),
    "NOT_TODAY_THANK_YOU": AdvancementInfo("""Not Today, Thank You""", "story/deflect_arrow", """Deflect a projectile with a Shield."""),
    "ICE_BUCKET_CHALLENGE": AdvancementInfo("""Ice Bucket Challenge""", "story/form_obsidian", """Obtain a block of Obsidian."""),
    "DIAMONDS": AdvancementInfo("""Diamonds!""", "story/mine_diamond", """Acquire diamonds."""),
    "WE_NEED_TO_GO_DEEPER": AdvancementInfo("""We Need to Go Deeper""", "story/enter_the_nether", """Build, light and enter a Nether Portal."""),
    "COVER_ME_WITH_DIAMONDS": AdvancementInfo("""Cover Me with Diamonds""", "story/shiny_gear", """Diamond armor saves lives."""),
    "ENCHANTER": AdvancementInfo("""Enchanter""", "story/enchant_item", """Enchant an item at an Enchanting Table."""),
    "ZOMBIE_DOCTOR": AdvancementInfo("""Zombie Doctor""", "story/cure_zombie_villager", """Weaken and then cure a Zombie Villager."""),
    "EYE_SPY": AdvancementInfo("""Eye Spy""", "story/follow_ender_eye", """Follow an Eye of Ender."""),
    "ENTER_THE_END": AdvancementInfo("""The End?""", "story/enter_the_end", """Enter the End Portal."""),
    "NETHER": AdvancementInfo("""Nether""", "nether/root", """Bring summer clothes."""),
    "RETURN_TO_SENDER": AdvancementInfo("""Return to Sender""", "nether/return_to_sender", """Destroy a Ghast with a fireball."""),
    "THOSE_WERE_THE_DAYS": AdvancementInfo("""Those Were the Days""", "nether/find_bastion", """Enter a Bastion Remnant."""),
    "HIDDEN_IN_THE_DEPTHS": AdvancementInfo("""Hidden in the Depths""", "nether/obtain_ancient_debris", """Obtain Ancient Debris."""),
    "SUBSPACE_BUBBLE": AdvancementInfo("""Subspace Bubble""", "nether/fast_travel", """Use the Nether to travel 7 km in the Overworld."""),
    "A_TERRIBLE_FORTRESS": AdvancementInfo("""A Terrible Fortress""", "nether/find_fortress", """Break your way into a Nether Fortress."""),
    "WHO_IS_CUTTING_ONIONS": AdvancementInfo("""Who is Cutting Onions?""", "nether/obtain_crying_obsidian", """Obtain Crying Obsidian."""),
    "OH_SHINY": AdvancementInfo("""Oh Shiny""", "nether/distract_piglin", """Distract Piglins with gold."""),
    "THIS_BOAT_HAS_LEGS": AdvancementInfo("""This Boat Has Legs""", "nether/ride_strider", """Ride a Strider with a Warped Fungus on a Stick."""),
    "UNEASY_ALLIANCE": AdvancementInfo("""Uneasy Alliance""", "nether/uneasy_alliance", """Rescue a Ghast from the Nether, bring it safely home to the Overworld... and then kill it."""),
    "WAR_PIGS": AdvancementInfo("""War Pigs""", "nether/loot_bastion", """Loot a Chest in a Bastion Remnant."""),
    "COVER_ME_IN_DEBRIS": AdvancementInfo("""Cover Me in Debris""", "nether/netherite_armor", """Get a full suit of Netherite armor."""),
    "SPOOKY_SCARY_SKELETON": AdvancementInfo("""Spooky Scary Skeleton""", "nether/get_wither_skull", """Obtain a Wither Skeleton's skull."""),
    "INTO_FIRE": AdvancementInfo("""Into Fire""", "nether/obtain_blaze_rod", """Relieve a Blaze of its rod."""),
    "NOT_QUITE_NINE_LIVES": AdvancementInfo("""Not Quite "Nine" Lives""", "nether/charge_respawn_anchor", """Charge a Respawn Anchor to the maximum."""),
    "FEELS_LIKE_HOME": AdvancementInfo("""Feels Like Home""", "nether/ride_strider_in_overworld_lava", """Take a Strider for a loooong ride on a lava lake in the Overworld."""),
    "HOT_TOURIST_DESTINATIONS": AdvancementInfo("""Hot Tourist Destinations""", "nether/explore_nether", """Explore all Nether biomes."""),
    "WITHERING_HEIGHTS": AdvancementInfo("""Withering Heights""", "nether/summon_wither", """Summon the Wither."""),
    "LOCAL_BREWERY": AdvancementInfo("""Local Brewery""", "nether/brew_potion", """Brew a Potion."""),
    "BRING_HOME_THE_BEACON": AdvancementInfo("""Bring Home the Beacon""", "nether/create_beacon", """Construct and place a Beacon."""),
    "A_FURIOUS_COCKTAIL": AdvancementInfo("""A Furious Cocktail""", "nether/all_potions", """Have every potion effect applied at the same time."""),
    "BEACONATOR": AdvancementInfo("""Beaconator""", "nether/create_full_beacon", """Bring a Beacon to full power."""),
    "HOW_DID_WE_GET_HERE": AdvancementInfo("""How Did We Get Here?""", "nether/all_effects", """Have every effect applied at the same time."""),
    "THE_END": AdvancementInfo("""The End""", "end/root", """Or the beginning?"""),
    "FREE_THE_END": AdvancementInfo("""Free the End""", "end/kill_dragon", """Good luck."""),
    "THE_NEXT_GENERATION": AdvancementInfo("""The Next Generation""", "end/dragon_egg", """Hold the Dragon Egg."""),
    "REMOTE_GETAWAY": AdvancementInfo("""Remote Getaway""", "end/enter_end_gateway", """Escape the island."""),
    "THE_END_AGAIN": AdvancementInfo("""The End... Again...""", "end/respawn_dragon", """Respawn the Ender Dragon."""),
    "YOU_NEED_A_MINT": AdvancementInfo("""You Need a Mint""", "end/dragon_breath", """Collect Dragon's Breath in a Glass Bottle."""),
    "THE_CITY_AT_THE_END_OF_THE_GAME": AdvancementInfo("""The City at the End of the Game""", "end/find_end_city", """Go on in, what could happen?"""),
    "SKYS_THE_LIMIT": AdvancementInfo("""Sky's the Limit""", "end/elytra", """Find Elytra."""),
    "GREAT_VIEW_FROM_UP_HERE": AdvancementInfo("""Great View From Up Here""", "end/levitate", """Levitate up 50 blocks from the attacks of a Shulker."""),
    "ADVENTURE": AdvancementInfo("""Adventure""", "adventure/root", """Adventure, exploration and combat."""),
    "HEART_TRANSPLANTER": AdvancementInfo("""Heart Transplanter""", "adventure/heart_transplanter", """Place a Creaking Heart with the correct alignment between two Pale Oak Log blocks."""),
    "VOLUNTARY_EXILE": AdvancementInfo("""Voluntary Exile""", "adventure/voluntary_exile", """Kill a raid captain.Maybe consider staying away from villages for the time being..."""),
    "COUNTRY_LODE_TAKE_ME_HOME": AdvancementInfo("""Country Lode, Take Me Home""", "adventure/use_lodestone", """Use a Compass on a Lodestone."""),
    "IS_IT_A_BIRD": AdvancementInfo("""Is It a Bird?""", "adventure/spyglass_at_parrot", """Look at a Parrot through a Spyglass."""),
    "MONSTER_HUNTER": AdvancementInfo("""Monster Hunter""", "adventure/kill_a_mob", """Kill any hostile monster."""),
    "THE_POWER_OF_BOOKS": AdvancementInfo("""The Power of Books""", "adventure/read_power_of_chiseled_bookshelf", """Read the power signal of a Chiseled Bookshelf using a Comparator."""),
    "WHAT_A_DEAL": AdvancementInfo("""What a Deal!""", "adventure/trade", """Successfully trade with a Villager."""),
    "CRAFTING_A_NEW_LOOK": AdvancementInfo("""Crafting a New Look""", "adventure/trim_with_any_armor_pattern", """Craft a trimmed armor at a Smithing Table."""),
    "STICKY_SITUATION": AdvancementInfo("""Sticky Situation""", "adventure/honey_block_slide", """Jump into a Honey Block to break your fall."""),
    "OL_BETSY": AdvancementInfo("""Ol' Betsy""", "adventure/ol_betsy", """Shoot a Crossbow."""),
    "SURGE_PROTECTOR": AdvancementInfo("""Surge Protector""", "adventure/lightning_rod_with_villager_no_fire", """Protect a Villager from an undesired shock without starting a fire."""),
    "CAVES__CLIFFS": AdvancementInfo("""Caves & Cliffs""", "adventure/fall_from_world_height", """Free fall from the top of the world (build limit) to the bottom of the world and survive."""),
    "RESPECTING_THE_REMNANTS": AdvancementInfo("""Respecting the Remnants""", "adventure/salvage_sherd", """Brush a Suspicious block to obtain a Pottery Sherd."""),
    "SNEAK_100": AdvancementInfo("""Sneak 100""", "adventure/avoid_vibration", """Sneak near a Sculk Sensor or Warden to prevent it from detecting you."""),
    "SWEET_DREAMS": AdvancementInfo("""Sweet Dreams""", "adventure/sleep_in_bed", """Sleep in a Bed to change your respawn point."""),
    "HERO_OF_THE_VILLAGE": AdvancementInfo("""Hero of the Village""", "adventure/hero_of_the_village", """Successfully defend a village from a raid."""),
    "IS_IT_A_BALLOON": AdvancementInfo("""Is It a Balloon?""", "adventure/spyglass_at_ghast", """Look at a Ghast through a Spyglass."""),
    "A_THROWAWAY_JOKE": AdvancementInfo("""A Throwaway Joke""", "adventure/throw_trident", """Throw a Trident at something.Note: Throwing away your only weapon is not a good idea."""),
    "IT_SPREADS": AdvancementInfo("""It Spreads""", "adventure/kill_mob_near_sculk_catalyst", """Kill a mob near a Sculk Catalyst."""),
    "TAKE_AIM": AdvancementInfo("""Take Aim""", "adventure/shoot_arrow", """Shoot something with an Arrow."""),
    "MONSTERS_HUNTED": AdvancementInfo("""Monsters Hunted""", "adventure/kill_all_mobs", """Kill one of every hostile monster."""),
    "POSTMORTAL": AdvancementInfo("""Postmortal""", "adventure/totem_of_undying", """Use a Totem of Undying to cheat death."""),
    "HIRED_HELP": AdvancementInfo("""Hired Help""", "adventure/summon_iron_golem", """Summon an Iron Golem to help defend a village."""),
    "STAR_TRADER": AdvancementInfo("""Star Trader""", "adventure/trade_at_world_height", """Trade with a Villager at the build height limit."""),
    "SMITHING_WITH_STYLE": AdvancementInfo("""Smithing with Style""", "adventure/trim_with_all_exclusive_armor_patterns", """Apply these smithing templates at least once: Spire, Snout, Rib, Ward, Silence, Vex, Tide, Wayfinder."""),
    "TWO_BIRDS_ONE_ARROW": AdvancementInfo("""Two Birds, One Arrow""", "adventure/two_birds_one_arrow", """Kill two Phantoms with a piercing Arrow."""),
    "WHOS_THE_PILLAGER_NOW": AdvancementInfo("""Who's the Pillager Now?""", "adventure/whos_the_pillager_now", """Give a Pillager a taste of their own medicine."""),
    "ARBALISTIC": AdvancementInfo("""Arbalistic""", "adventure/arbalistic", """Kill five unique mobs with one crossbow shot."""),
    "CAREFUL_RESTORATION": AdvancementInfo("""Careful Restoration""", "adventure/craft_decorated_pot_using_only_sherds", """Make a Decorated Pot out of 4 Pottery Sherds."""),
    "ADVENTURING_TIME": AdvancementInfo("""Adventuring Time""", "adventure/adventuring_time", """Discover every biome."""),
    "SOUND_OF_MUSIC": AdvancementInfo("""Sound of Music""", "adventure/play_jukebox_in_meadows", """Make the Meadows come alive with the sound of music from a Jukebox."""),
    "LIGHT_AS_A_RABBIT": AdvancementInfo("""Light as a Rabbit""", "adventure/walk_on_powder_snow_with_leather_boots", """Walk on Powder Snow... without sinking in it."""),
    "IS_IT_A_PLANE": AdvancementInfo("""Is It a Plane?""", "adventure/spyglass_at_dragon", """Look at the Ender Dragon through a Spyglass."""),
    "VERY_VERY_FRIGHTENING": AdvancementInfo("""Very Very Frightening""", "adventure/very_very_frightening", """Strike a Villager with lightning."""),
    "SNIPER_DUEL": AdvancementInfo("""Sniper Duel""", "adventure/sniper_duel", """Kill a Skeleton from at least 50 meters away."""),
    "BULLSEYE": AdvancementInfo("""Bullseye""", "adventure/bullseye", """Hit the bullseye of a Target block from at least 30 meters away."""),
    "ISNT_IT_SCUTE": AdvancementInfo("""Isn't It Scute?""", "adventure/brush_armadillo", """Get Armadillo Scutes from an Armadillo using a Brush."""),
    "MINECRAFT_TRIALS_EDITION": AdvancementInfo("""Minecraft: Trial(s) Edition""", "adventure/minecraft_trials_edition", """Step foot in a Trial Chamber."""),
    "CRAFTERS_CRAFTING_CRAFTERS": AdvancementInfo("""Crafters Crafting Crafters""", "adventure/crafters_crafting_crafters", """Be near a Crafter when it crafts a Crafter."""),
    "LIGHTEN_UP": AdvancementInfo("""Lighten Up""", "adventure/lighten_up", """Scrape a Copper Bulb with an Axe to make it brighter."""),
    "WHO_NEEDS_ROCKETS": AdvancementInfo("""Who Needs Rockets?""", "adventure/who_needs_rockets", """Use a Wind Charge to launch yourself upwards 8 blocks."""),
    "UNDER_LOCK_AND_KEY": AdvancementInfo("""Under Lock and Key""", "adventure/under_lock_and_key", """Use a Trial Key on a Vault."""),
    "REVAULTING": AdvancementInfo("""Revaulting""", "adventure/revaulting", """Use an Ominous Trial Key on an Ominous Vault."""),
    "BLOWBACK": AdvancementInfo("""Blowback""", "adventure/blowback", """Kill a Breeze with a deflected Breeze-shot Wind Charge."""),
    "OVEROVERKILL": AdvancementInfo("""Over-Overkill""", "adventure/overoverkill", """Deal 50 hearts of damage in a single hit using the Mace."""),
    "HUSBANDRY": AdvancementInfo("""Husbandry""", "husbandry/root", """The world is full of friends and food."""),
    "STAY_HYDRATED": AdvancementInfo("""Stay Hydrated!""", "husbandry/place_dried_ghast_in_water", """Place a Dried Ghast block into water."""),
    "BEE_OUR_GUEST": AdvancementInfo("""Bee Our Guest""", "husbandry/safely_harvest_honey", """Use a Campfire to collect Honey from a Beehive using a Glass Bottle without aggravating the Bees."""),
    "THE_PARROTS_AND_THE_BATS": AdvancementInfo("""The Parrots and the Bats""", "husbandry/breed_an_animal", """Breed two animals together."""),
    "YOUVE_GOT_A_FRIEND_IN_ME": AdvancementInfo("""You've Got a Friend in Me""", "husbandry/allay_deliver_item_to_player", """Have an Allay deliver items to you."""),
    "WHATEVER_FLOATS_YOUR_GOAT": AdvancementInfo("""Whatever Floats Your Goat!""", "husbandry/ride_a_boat_with_a_goat", """Get in a Boat and float with a Goat."""),
    "BEST_FRIENDS_FOREVER": AdvancementInfo("""Best Friends Forever""", "husbandry/tame_an_animal", """Tame an animal."""),
    "GLOW_AND_BEHOLD": AdvancementInfo("""Glow and Behold!""", "husbandry/make_a_sign_glow", """Make the text of any kind of sign glow."""),
    "FISHY_BUSINESS": AdvancementInfo("""Fishy Business""", "husbandry/fishy_business", """Catch a fish."""),
    "TOTAL_BEELOCATION": AdvancementInfo("""Total Beelocation""", "husbandry/silk_touch_nest", """Move a Bee Nest, with 3 Bees inside, using Silk Touch."""),
    "BUKKIT_BUKKIT": AdvancementInfo("""Bukkit Bukkit""", "husbandry/tadpole_in_a_bucket", """Catch a Tadpole in a Bucket."""),
    "SMELLS_INTERESTING": AdvancementInfo("""Smells Interesting""", "husbandry/obtain_sniffer_egg", """Obtain a Sniffer Egg."""),
    "A_SEEDY_PLACE": AdvancementInfo("""A Seedy Place""", "husbandry/plant_seed", """Plant a seed and watch it grow."""),
    "WAX_ON": AdvancementInfo("""Wax On""", "husbandry/wax_on", """Apply Honeycomb to a Copper block!"""),
    "TWO_BY_TWO": AdvancementInfo("""Two by Two""", "husbandry/bred_all_animals", """Breed all the animals!"""),
    "BIRTHDAY_SONG": AdvancementInfo("""Birthday Song""", "husbandry/allay_deliver_cake_to_note_block", """Have an Allay drop a Cake at a Note Block."""),
    "A_COMPLETE_CATALOGUE": AdvancementInfo("""A Complete Catalogue""", "husbandry/complete_catalogue", """Tame all Cat variants!"""),
    "TACTICAL_FISHING": AdvancementInfo("""Tactical Fishing""", "husbandry/tactical_fishing", """Catch a Fish... without a Fishing Rod!"""),
    "WHEN_THE_SQUAD_HOPS_INTO_TOWN": AdvancementInfo("""When the Squad Hops into Town""", "husbandry/leash_all_frog_variants", """Get each Frog variant on a Lead."""),
    "LITTLE_SNIFFS": AdvancementInfo("""Little Sniffs""", "husbandry/feed_snifflet", """Feed a Snifflet."""),
    "A_BALANCED_DIET": AdvancementInfo("""A Balanced Diet""", "husbandry/balanced_diet", """Eat everything that is edible, even if it's not good for you."""),
    "SERIOUS_DEDICATION": AdvancementInfo("""Serious Dedication""", "husbandry/obtain_netherite_hoe", """Use a Netherite Ingot to upgrade a Hoe, and then reevaluate your life choices."""),
    "WAX_OFF": AdvancementInfo("""Wax Off""", "husbandry/wax_off", """Scrape Wax off of a Copper block!"""),
    "THE_CUTEST_PREDATOR": AdvancementInfo("""The Cutest Predator""", "husbandry/axolotl_in_a_bucket", """Catch an Axolotl in a Bucket."""),
    "WITH_OUR_POWERS_COMBINED": AdvancementInfo("""With Our Powers Combined!""", "husbandry/froglights", """Have all Froglights in your inventory."""),
    "PLANTING_THE_PAST": AdvancementInfo("""Planting the Past""", "husbandry/plant_any_sniffer_seed", """Plant any Sniffer seed."""),
    "THE_HEALING_POWER_OF_FRIENDSHIP": AdvancementInfo("""The Healing Power of Friendship!""", "husbandry/kill_axolotl_target", """Team up with an axolotl and win a fight."""),
    "GOOD_AS_NEW": AdvancementInfo("""Good as New""", "husbandry/repair_wolf_armor", """Repair a damaged Wolf Armor using Armadillo Scutes."""),
    "THE_WHOLE_PACK": AdvancementInfo("""The Whole Pack""", "husbandry/whole_pack", """Tame one of each Wolf variant."""),
    "SHEAR_BRILLIANCE": AdvancementInfo("""Shear Brilliance""", "husbandry/remove_wolf_armor", """Remove Wolf Armor from a Wolf using Shears."""),
}

for __k in tuple(advancements.keys()):
    v = advancements[__k]
    advancements[v.name] = v
    advancements[v.value] = v


def as_advancement(*values: StrOrArg) -> str | Tuple[str, ...]:
    return _as_things(ADVANCEMENT_GROUP, __advancement_dups, *values)



# Biomes
# Derived from https://minecraft.wiki/Biome/ID, 2025-06-30T18:19:22-07:00
__biome_dups = {}
THE_VOID = "the_void"
__biome_dups["plains"] = "plains"
SUNFLOWER_PLAINS = "sunflower_plains"
SNOWY_PLAINS = "snowy_plains"
ICE_SPIKES = "ice_spikes"
__biome_dups["desert"] = "desert"
__biome_dups["swamp"] = "swamp"
MANGROVE_SWAMP = "mangrove_swamp"
FOREST = "forest"
FLOWER_FOREST = "flower_forest"
BIRCH_FOREST = "birch_forest"
DARK_FOREST = "dark_forest"
PALE_GARDEN = "pale_garden"
OLD_GROWTH_BIRCH_FOREST = "old_growth_birch_forest"
OLD_GROWTH_PINE_TAIGA = "old_growth_pine_taiga"
OLD_GROWTH_SPRUCE_TAIGA = "old_growth_spruce_taiga"
__biome_dups["taiga"] = "taiga"
SNOWY_TAIGA = "snowy_taiga"
__biome_dups["savanna"] = "savanna"
SAVANNA_PLATEAU = "savanna_plateau"
WINDSWEPT_HILLS = "windswept_hills"
WINDSWEPT_GRAVELLY_HILLS = "windswept_gravelly_hills"
WINDSWEPT_FOREST = "windswept_forest"
WINDSWEPT_SAVANNA = "windswept_savanna"
__biome_dups["jungle"] = "jungle"
SPARSE_JUNGLE = "sparse_jungle"
BAMBOO_JUNGLE = "bamboo_jungle"
BADLANDS = "badlands"
ERODED_BADLANDS = "eroded_badlands"
WOODED_BADLANDS = "wooded_badlands"
MEADOW = "meadow"
CHERRY_GROVE = "cherry_grove"
GROVE = "grove"
SNOWY_SLOPES = "snowy_slopes"
FROZEN_PEAKS = "frozen_peaks"
JAGGED_PEAKS = "jagged_peaks"
STONY_PEAKS = "stony_peaks"
RIVER = "river"
FROZEN_RIVER = "frozen_river"
BEACH = "beach"
SNOWY_BEACH = "snowy_beach"
STONY_SHORE = "stony_shore"
WARM_OCEAN = "warm_ocean"
LUKEWARM_OCEAN = "lukewarm_ocean"
DEEP_LUKEWARM_OCEAN = "deep_lukewarm_ocean"
OCEAN = "ocean"
DEEP_OCEAN = "deep_ocean"
COLD_OCEAN = "cold_ocean"
DEEP_COLD_OCEAN = "deep_cold_ocean"
FROZEN_OCEAN = "frozen_ocean"
DEEP_FROZEN_OCEAN = "deep_frozen_ocean"
MUSHROOM_FIELDS = "mushroom_fields"
DRIPSTONE_CAVES = "dripstone_caves"
LUSH_CAVES = "lush_caves"
DEEP_DARK = "deep_dark"
NETHER_WASTES = "nether_wastes"
WARPED_FOREST = "warped_forest"
CRIMSON_FOREST = "crimson_forest"
SOUL_SAND_VALLEY = "soul_sand_valley"
BASALT_DELTAS = "basalt_deltas"
__biome_dups["the_end"] = "the_end"
END_HIGHLANDS = "end_highlands"
END_MIDLANDS = "end_midlands"
SMALL_END_ISLANDS = "small_end_islands"
END_BARRENS = "end_barrens"
BIOME_GROUP = [
    THE_VOID, "plains", SUNFLOWER_PLAINS, SNOWY_PLAINS, ICE_SPIKES, "desert", "swamp", MANGROVE_SWAMP, FOREST, FLOWER_FOREST, BIRCH_FOREST, DARK_FOREST, PALE_GARDEN, OLD_GROWTH_BIRCH_FOREST, OLD_GROWTH_PINE_TAIGA, OLD_GROWTH_SPRUCE_TAIGA, "taiga", SNOWY_TAIGA, "savanna", SAVANNA_PLATEAU, WINDSWEPT_HILLS, WINDSWEPT_GRAVELLY_HILLS, WINDSWEPT_FOREST, WINDSWEPT_SAVANNA, "jungle", SPARSE_JUNGLE, BAMBOO_JUNGLE, BADLANDS, ERODED_BADLANDS, WOODED_BADLANDS, MEADOW, CHERRY_GROVE, GROVE, SNOWY_SLOPES, FROZEN_PEAKS, JAGGED_PEAKS, STONY_PEAKS, RIVER, FROZEN_RIVER, BEACH, SNOWY_BEACH, STONY_SHORE, WARM_OCEAN, LUKEWARM_OCEAN, DEEP_LUKEWARM_OCEAN, OCEAN, DEEP_OCEAN, COLD_OCEAN, DEEP_COLD_OCEAN, FROZEN_OCEAN, DEEP_FROZEN_OCEAN, MUSHROOM_FIELDS, DRIPSTONE_CAVES, LUSH_CAVES, DEEP_DARK, NETHER_WASTES, WARPED_FOREST, CRIMSON_FOREST, SOUL_SAND_VALLEY, BASALT_DELTAS, "the_end", END_HIGHLANDS, END_MIDLANDS, SMALL_END_ISLANDS, END_BARRENS
]

BiomeInfo = namedtuple("Biome", ['name', 'value', 'desc'])
biomes = {
    "THE_VOID": BiomeInfo("""The Void""", "the_void", """The Void."""),
    "PLAINS": BiomeInfo("""Plains""", "plains", """Plains."""),
    "SUNFLOWER_PLAINS": BiomeInfo("""Sunflower Plains""", "sunflower_plains", """Sunflower Plains."""),
    "SNOWY_PLAINS": BiomeInfo("""Snowy Plains""", "snowy_plains", """Snowy Plains."""),
    "ICE_SPIKES": BiomeInfo("""Ice Spikes""", "ice_spikes", """Ice Spikes."""),
    "DESERT": BiomeInfo("""Desert""", "desert", """Desert."""),
    "SWAMP": BiomeInfo("""Swamp""", "swamp", """Swamp."""),
    "MANGROVE_SWAMP": BiomeInfo("""Mangrove Swamp""", "mangrove_swamp", """Mangrove Swamp."""),
    "FOREST": BiomeInfo("""Forest""", "forest", """Forest."""),
    "FLOWER_FOREST": BiomeInfo("""Flower Forest""", "flower_forest", """Flower Forest."""),
    "BIRCH_FOREST": BiomeInfo("""Birch Forest""", "birch_forest", """Birch Forest."""),
    "DARK_FOREST": BiomeInfo("""Dark Forest""", "dark_forest", """Dark Forest."""),
    "PALE_GARDEN": BiomeInfo("""Pale Garden""", "pale_garden", """Pale Garden."""),
    "OLD_GROWTH_BIRCH_FOREST": BiomeInfo("""Old Growth Birch Forest""", "old_growth_birch_forest", """Old Growth Birch Forest."""),
    "OLD_GROWTH_PINE_TAIGA": BiomeInfo("""Old Growth Pine Taiga""", "old_growth_pine_taiga", """Old Growth Pine Taiga."""),
    "OLD_GROWTH_SPRUCE_TAIGA": BiomeInfo("""Old Growth Spruce Taiga""", "old_growth_spruce_taiga", """Old Growth Spruce Taiga."""),
    "TAIGA": BiomeInfo("""Taiga""", "taiga", """Taiga."""),
    "SNOWY_TAIGA": BiomeInfo("""Snowy Taiga""", "snowy_taiga", """Snowy Taiga."""),
    "SAVANNA": BiomeInfo("""Savanna""", "savanna", """Savanna."""),
    "SAVANNA_PLATEAU": BiomeInfo("""Savanna Plateau""", "savanna_plateau", """Savanna Plateau."""),
    "WINDSWEPT_HILLS": BiomeInfo("""Windswept Hills""", "windswept_hills", """Windswept Hills."""),
    "WINDSWEPT_GRAVELLY_HILLS": BiomeInfo("""Windswept Gravelly Hills""", "windswept_gravelly_hills", """Windswept Gravelly Hills."""),
    "WINDSWEPT_FOREST": BiomeInfo("""Windswept Forest""", "windswept_forest", """Windswept Forest."""),
    "WINDSWEPT_SAVANNA": BiomeInfo("""Windswept Savanna""", "windswept_savanna", """Windswept Savanna."""),
    "JUNGLE": BiomeInfo("""Jungle""", "jungle", """Jungle."""),
    "SPARSE_JUNGLE": BiomeInfo("""Sparse Jungle""", "sparse_jungle", """Sparse Jungle."""),
    "BAMBOO_JUNGLE": BiomeInfo("""Bamboo Jungle""", "bamboo_jungle", """Bamboo Jungle."""),
    "BADLANDS": BiomeInfo("""Badlands""", "badlands", """Badlands."""),
    "ERODED_BADLANDS": BiomeInfo("""Eroded Badlands""", "eroded_badlands", """Eroded Badlands."""),
    "WOODED_BADLANDS": BiomeInfo("""Wooded Badlands""", "wooded_badlands", """Wooded Badlands."""),
    "MEADOW": BiomeInfo("""Meadow""", "meadow", """Meadow."""),
    "CHERRY_GROVE": BiomeInfo("""Cherry Grove""", "cherry_grove", """Cherry Grove."""),
    "GROVE": BiomeInfo("""Grove""", "grove", """Grove."""),
    "SNOWY_SLOPES": BiomeInfo("""Snowy Slopes""", "snowy_slopes", """Snowy Slopes."""),
    "FROZEN_PEAKS": BiomeInfo("""Frozen Peaks""", "frozen_peaks", """Frozen Peaks."""),
    "JAGGED_PEAKS": BiomeInfo("""Jagged Peaks""", "jagged_peaks", """Jagged Peaks."""),
    "STONY_PEAKS": BiomeInfo("""Stony Peaks""", "stony_peaks", """Stony Peaks."""),
    "RIVER": BiomeInfo("""River""", "river", """River."""),
    "FROZEN_RIVER": BiomeInfo("""Frozen River""", "frozen_river", """Frozen River."""),
    "BEACH": BiomeInfo("""Beach""", "beach", """Beach."""),
    "SNOWY_BEACH": BiomeInfo("""Snowy Beach""", "snowy_beach", """Snowy Beach."""),
    "STONY_SHORE": BiomeInfo("""Stony Shore""", "stony_shore", """Stony Shore."""),
    "WARM_OCEAN": BiomeInfo("""Warm Ocean""", "warm_ocean", """Warm Ocean."""),
    "LUKEWARM_OCEAN": BiomeInfo("""Lukewarm Ocean""", "lukewarm_ocean", """Lukewarm Ocean."""),
    "DEEP_LUKEWARM_OCEAN": BiomeInfo("""Deep Lukewarm Ocean""", "deep_lukewarm_ocean", """Deep Lukewarm Ocean."""),
    "OCEAN": BiomeInfo("""Ocean""", "ocean", """Ocean."""),
    "DEEP_OCEAN": BiomeInfo("""Deep Ocean""", "deep_ocean", """Deep Ocean."""),
    "COLD_OCEAN": BiomeInfo("""Cold Ocean""", "cold_ocean", """Cold Ocean."""),
    "DEEP_COLD_OCEAN": BiomeInfo("""Deep Cold Ocean""", "deep_cold_ocean", """Deep Cold Ocean."""),
    "FROZEN_OCEAN": BiomeInfo("""Frozen Ocean""", "frozen_ocean", """Frozen Ocean."""),
    "DEEP_FROZEN_OCEAN": BiomeInfo("""Deep Frozen Ocean""", "deep_frozen_ocean", """Deep Frozen Ocean."""),
    "MUSHROOM_FIELDS": BiomeInfo("""Mushroom Fields""", "mushroom_fields", """Mushroom Fields."""),
    "DRIPSTONE_CAVES": BiomeInfo("""Dripstone Caves""", "dripstone_caves", """Dripstone Caves."""),
    "LUSH_CAVES": BiomeInfo("""Lush Caves""", "lush_caves", """Lush Caves."""),
    "DEEP_DARK": BiomeInfo("""Deep Dark""", "deep_dark", """Deep Dark."""),
    "NETHER_WASTES": BiomeInfo("""Nether Wastes""", "nether_wastes", """Nether Wastes."""),
    "WARPED_FOREST": BiomeInfo("""Warped Forest""", "warped_forest", """Warped Forest."""),
    "CRIMSON_FOREST": BiomeInfo("""Crimson Forest""", "crimson_forest", """Crimson Forest."""),
    "SOUL_SAND_VALLEY": BiomeInfo("""Soul Sand Valley""", "soul_sand_valley", """Soul Sand Valley."""),
    "BASALT_DELTAS": BiomeInfo("""Basalt Deltas""", "basalt_deltas", """Basalt Deltas."""),
    "THE_END": BiomeInfo("""The End""", "the_end", """The End."""),
    "END_HIGHLANDS": BiomeInfo("""End Highlands""", "end_highlands", """End Highlands."""),
    "END_MIDLANDS": BiomeInfo("""End Midlands""", "end_midlands", """End Midlands."""),
    "SMALL_END_ISLANDS": BiomeInfo("""Small End Islands""", "small_end_islands", """Small End Islands."""),
    "END_BARRENS": BiomeInfo("""End Barrens""", "end_barrens", """End Barrens."""),
}

for __k in tuple(biomes.keys()):
    v = biomes[__k]
    biomes[v.name] = v
    biomes[v.value] = v


def as_biome(*values: StrOrArg) -> str | Tuple[str, ...]:
    return _as_things(BIOME_GROUP, __biome_dups, *values)



# Effects
# Derived from https://minecraft.wiki/Effect?so=search#Effect_list, 2025-06-30T18:19:22-07:00
__effect_dups = {}
SPEED = "speed"
SLOWNESS = "slowness"
HASTE = "haste"
MINING_FATIGUE = "mining_fatigue"
STRENGTH = "strength"
INSTANT_HEALTH = "instant_health"
INSTANT_DAMAGE = "instant_damage"
JUMP_BOOST = "jump_boost"
NAUSEA = "nausea"
REGENERATION = "regeneration"
RESISTANCE = "resistance"
FIRE_RESISTANCE = "fire_resistance"
WATER_BREATHING = "water_breathing"
INVISIBILITY = "invisibility"
BLINDNESS = "blindness"
NIGHT_VISION = "night_vision"
HUNGER = "hunger"
WEAKNESS = "weakness"
POISON = "poison"
WITHER = "wither"
HEALTH_BOOST = "health_boost"
ABSORPTION = "absorption"
SATURATION = "saturation"
GLOWING = "glowing"
LEVITATION = "levitation"
LUCK = "luck"
BAD_LUCK = "unluck"
SLOW_FALLING = "slow_falling"
CONDUIT_POWER = "conduit_power"
DOLPHINS_GRACE = "dolphins_grace"
BAD_OMEN = "bad_omen"
__effect_dups["adventure/hero_of_the_village"] = "hero_of_the_village"
DARKNESS = "darkness"
TRIAL_OMEN = "trial_omen"
RAID_OMEN = "raid_omen"
WIND_CHARGED = "wind_charged"
WEAVING = "weaving"
OOZING = "oozing"
INFESTED = "infested"
EFFECT_GROUP = [
    SPEED, SLOWNESS, HASTE, MINING_FATIGUE, STRENGTH, INSTANT_HEALTH, INSTANT_DAMAGE, JUMP_BOOST, NAUSEA, REGENERATION, RESISTANCE, FIRE_RESISTANCE, WATER_BREATHING, INVISIBILITY, BLINDNESS, NIGHT_VISION, HUNGER, WEAKNESS, POISON, WITHER, HEALTH_BOOST, ABSORPTION, SATURATION, GLOWING, LEVITATION, LUCK, BAD_LUCK, SLOW_FALLING, CONDUIT_POWER, DOLPHINS_GRACE, BAD_OMEN, "hero_of_the_village", DARKNESS, TRIAL_OMEN, RAID_OMEN, WIND_CHARGED, WEAVING, OOZING, INFESTED
]

EffectInfo = namedtuple("Effect", ['name', 'value', 'desc', 'positive'])
effects = {
    "SPEED": EffectInfo("""Speed""", "speed", """Increases walking speed; higher levels make the affected entity faster and increases the player's field of view when affected.""", True),
    "SLOWNESS": EffectInfo("""Slowness""", "slowness", """Decreases walking speed; higher levels make the affected entity slower and decreases the player's field of view when affected.""", False),
    "HASTE": EffectInfo("""Haste""", "haste", """Increases mining and attack speed, higher levels increase the player's mining and attack speed.""", True),
    "MINING_FATIGUE": EffectInfo("""Mining Fatigue""", "mining_fatigue", """Decreases mining and attack speed, higher levels decrease the player's mining and attack speed.""", False),
    "STRENGTH": EffectInfo("""Strength""", "strength", """Increases melee damage, higher levels make the affected entity do more melee damage.""", True),
    "INSTANT_HEALTH": EffectInfo("""Instant Health""", "instant_health", """Heals living entities, damages undead, higher levels heal more health and do more damage.""", True),
    "INSTANT_DAMAGE": EffectInfo("""Instant Damage""", "instant_damage", """Damages living entities, heals undead, higher levels do more damage and heal more health.""", False),
    "JUMP_BOOST": EffectInfo("""Jump Boost""", "jump_boost", """Increases jump height and reduces fall damage, higher levels make the affected entity jump higher and reduces more fall damage.""", True),
    "NAUSEA": EffectInfo("""Nausea""", "nausea", """Wobbles and warps the screen, and increasingly gets worse.""", False),
    "REGENERATION": EffectInfo("""Regeneration""", "regeneration", """Regenerates health over time, higher levels make health regenerate quicker.""", True),
    "RESISTANCE": EffectInfo("""Resistance""", "resistance", """Reduces damage, higher levels reduce more damage.""", True),
    "FIRE_RESISTANCE": EffectInfo("""Fire Resistance""", "fire_resistance", """Prevents the affected entity from taking damage due to fire, lava and other sources of fire damage.""", True),
    "WATER_BREATHING": EffectInfo("""Water Breathing""", "water_breathing", """Prevents drowning and lets the affected entity breathe underwater.""", True),
    "INVISIBILITY": EffectInfo("""Invisibility""", "invisibility", """Makes the affected entity invisible (but not the item they hold or the armor they wear), and reduces other mobs' detection range for the affected entity.""", True),
    "BLINDNESS": EffectInfo("""Blindness""", "blindness", """Impairs vision by adding close black fog and disables the ability to sprint and critical hit.""", False),
    "NIGHT_VISION": EffectInfo("""Night Vision""", "night_vision", """Lets the player see well in darkness and underwater.""", True),
    "HUNGER": EffectInfo("""Hunger""", "hunger", """Increases food exhaustion, higher levels cause the player to starve quicker.""", False),
    "WEAKNESS": EffectInfo("""Weakness""", "weakness", """Decreases melee damage, higher levels decrease more melee damage.""", False),
    "POISON": EffectInfo("""Poison""", "poison", """Inflicts damage over time (but can't kill), higher levels do more damage per second, doesn't affect undead.""", False),
    "WITHER": EffectInfo("""Wither""", "wither", """Inflicts damage over time (can kill), higher levels do more damage per second.""", False),
    "HEALTH_BOOST": EffectInfo("""Health Boost""", "health_boost", """Increases maximum health, higher levels give the affected entity more maximum health.""", True),
    "ABSORPTION": EffectInfo("""Absorption""", "absorption", """Adds damage absorption (additional hearts that can't be regenerated), higher levels give more absorption.""", True),
    "SATURATION": EffectInfo("""Saturation""", "saturation", """Restores hunger and saturation.""", True),
    "GLOWING": EffectInfo("""Glowing""", "glowing", """Outlines the affected entity (the outline can be seen through blocks).""", None),
    "LEVITATION": EffectInfo("""Levitation""", "levitation", """Floats the affected entity upward, higher levels make the affected entity float up faster.""", False),
    "LUCK": EffectInfo("""Luck""", "luck", """Increases chances of better loot from fishing, higher levels increase the chances of better and more loot.""", True),
    "BAD_LUCK": EffectInfo("""Bad Luck""", "unluck", """Reduces chances of better and more loot from fishing and chests, higher levels reduces the chances of good loot even more.""", False),
    "SLOW_FALLING": EffectInfo("""Slow Falling""", "slow_falling", """Decreases falling speed and negates fall damage.""", True),
    "CONDUIT_POWER": EffectInfo("""Conduit Power""", "conduit_power", """Increases underwater visibility and mining speed, prevents drowning.""", True),
    "DOLPHINS_GRACE": EffectInfo("""Dolphin's Grace""", "dolphins_grace", """Increases swimming speed (only obtainable from dolphins and commands).""", True),
    "BAD_OMEN": EffectInfo("""Bad Omen""", "bad_omen", """Causes an ominous event upon entering a village or a trial chamber.""", None),
    "HERO_OF_THE_VILLAGE": EffectInfo("""Hero of the Village""", "hero_of_the_village", """Gives discounts on trades with villagers, and makes villagers throw items at the player depending on their profession.""", True),
    "DARKNESS": EffectInfo("""Darkness""", "darkness", """Adds a pulsating darkening affect to the players screen and pulsating black fog.""", False),
    "TRIAL_OMEN": EffectInfo("""Trial Omen""", "trial_omen", """Transforms nearby trial spawners into ominous trial spawners.""", None),
    "RAID_OMEN": EffectInfo("""Raid Omen""", "raid_omen", """Starts a raid at the location the player gained the Raid Omen, once the effect expires.""", None),
    "WIND_CHARGED": EffectInfo("""Wind Charged""", "wind_charged", """Affected entities emit a burst of wind upon death.""", False),
    "WEAVING": EffectInfo("""Weaving""", "weaving", """Affected entities spread cobweb blocks upon death and increases movement speed in cobwebs by 15%.""", False),
    "OOZING": EffectInfo("""Oozing""", "oozing", """Makes the entity spawn 2 slimes upon death.""", False),
    "INFESTED": EffectInfo("""Infested""", "infested", """Gives the entity a 10% chance to spawn between 1 and 3 silverfish when hurt.""", False),
}

for __k in tuple(effects.keys()):
    v = effects[__k]
    effects[v.name] = v
    effects[v.value] = v


def as_effect(*values: StrOrArg) -> str | Tuple[str, ...]:
    return _as_things(EFFECT_GROUP, __effect_dups, *values)



# Enchantments
# Derived from https://minecraft.wiki/Enchanting#Summary_of_enchantments, 2025-06-30T18:19:22-07:00
__enchantment_dups = {}
AQUA_AFFINITY = "aqua_affinity"
BANE_OF_ARTHROPODS = "bane_of_arthropods"
BLAST_PROTECTION = "blast_protection"
BREACH = "breach"
CHANNELING = "channeling"
CURSE_OF_BINDING = "curse_of_binding"
CURSE_OF_VANISHING = "curse_of_vanishing"
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
CLEAVING = "cleaving"
ENCHANTMENT_GROUP = [
    AQUA_AFFINITY, BANE_OF_ARTHROPODS, BLAST_PROTECTION, BREACH, CHANNELING, CURSE_OF_BINDING, CURSE_OF_VANISHING, DENSITY, DEPTH_STRIDER, EFFICIENCY, FEATHER_FALLING, FIRE_ASPECT, FIRE_PROTECTION, FLAME, FORTUNE, FROST_WALKER, IMPALING, INFINITY, KNOCKBACK, LOOTING, LOYALTY, LUCK_OF_THE_SEA, LURE, MENDING, MULTISHOT, PIERCING, POWER, PROJECTILE_PROTECTION, PROTECTION, PUNCH, QUICK_CHARGE, RESPIRATION, RIPTIDE, SHARPNESS, SILK_TOUCH, SMITE, SOUL_SPEED, SWEEPING_EDGE, SWIFT_SNEAK, THORNS, UNBREAKING, WIND_BURST, CLEAVING
]

EnchantmentInfo = namedtuple("Enchantment", ['name', 'value', 'desc', 'max_level'])
enchantments = {
    "AQUA_AFFINITY": EnchantmentInfo("""Aqua Affinity""", "aqua_affinity", """Removes the mining speed reduction that occurs when underwater.""", 1),
    "BANE_OF_ARTHROPODS": EnchantmentInfo("""Bane of Arthropods""", "bane_of_arthropods", """Increases damage and applies Slowness IV to arthropod mobs (spiders, cave spiders, silverfish, endermites and bees).""", 5),
    "BLAST_PROTECTION": EnchantmentInfo("""Blast Protection""", "blast_protection", """Reduces explosion damage and knockback.""", 4),
    "BREACH": EnchantmentInfo("""Breach""", "breach", """Reduces the effectiveness of armor on the target, including innate armor points.""", 4),
    "CHANNELING": EnchantmentInfo("""Channeling""", "channeling", """During thunderstorms, a thrown trident summons a lightning bolt on the target upon hit.""", 1),
    "CURSE_OF_BINDING": EnchantmentInfo("""Curse of Binding""", "curse_of_binding", """Items cannot be removed from armor slots.""", 1),
    "CURSE_OF_VANISHING": EnchantmentInfo("""Curse of Vanishing""", "curse_of_vanishing", """Item disappears on death.""", 1),
    "DENSITY": EnchantmentInfo("""Density""", "density", """Increases the damage of a mace's smash attack.""", 5),
    "DEPTH_STRIDER": EnchantmentInfo("""Depth Strider""", "depth_strider", """Lessens the movement speed reduction that occurs when in water.""", 3),
    "EFFICIENCY": EnchantmentInfo("""Efficiency""", "efficiency", """Increases mining speed.""", 5),
    "FEATHER_FALLING": EnchantmentInfo("""Feather Falling""", "feather_falling", """Reduces fall damage.""", 4),
    "FIRE_ASPECT": EnchantmentInfo("""Fire Aspect""", "fire_aspect", """Sets targets on fire.""", 2),
    "FIRE_PROTECTION": EnchantmentInfo("""Fire Protection""", "fire_protection", """Reduces fire damage and burning time.""", 4),
    "FLAME": EnchantmentInfo("""Flame""", "flame", """Arrows set targets on fire.""", 1),
    "FORTUNE": EnchantmentInfo("""Fortune""", "fortune", """Chance to receive more item drops from certain blocks.""", 3),
    "FROST_WALKER": EnchantmentInfo("""Frost Walker""", "frost_walker", """Turns water into frosted ice beneath the wearer's feet, and provides immunity to campfire and magma block damage.""", 2),
    "IMPALING": EnchantmentInfo("""Impaling""", "impaling", """In Java Edition, increases damage against aquatic mobs. In Bedrock Edition, increases damage against mobs in water or rain.""", 5),
    "INFINITY": EnchantmentInfo("""Infinity""", "infinity", """Prevents consumption of arrows, but not spectral arrows or tipped arrows.""", 1),
    "KNOCKBACK": EnchantmentInfo("""Knockback""", "knockback", """Increases melee knockback.""", 2),
    "LOOTING": EnchantmentInfo("""Looting""", "looting", """Chance to receive more item drops from certain mobs.""", 3),
    "LOYALTY": EnchantmentInfo("""Loyalty""", "loyalty", """Returns the trident to its owner upon landing after being thrown.""", 3),
    "LUCK_OF_THE_SEA": EnchantmentInfo("""Luck of the Sea""", "luck_of_the_sea", """Increases the rate of treasure items from fishing.""", 3),
    "LURE": EnchantmentInfo("""Lure""", "lure", """Decreases time for bites when fishing.""", 3),
    "MENDING": EnchantmentInfo("""Mending""", "mending", """Repairs the item using experience.""", 1),
    "MULTISHOT": EnchantmentInfo("""Multishot""", "multishot", """Adds 2 arrows to the sides of the center arrow, at the cost of increasing incurred durability damage.""", 1),
    "PIERCING": EnchantmentInfo("""Piercing""", "piercing", """Causes fired arrows to pierce entities, allowing for a single arrow to hit multiple mobs, and allows arrows to be picked up again after hitting a target.""", 4),
    "POWER": EnchantmentInfo("""Power""", "power", """Increases arrow damage.""", 5),
    "PROJECTILE_PROTECTION": EnchantmentInfo("""Projectile Protection""", "projectile_protection", """Reduces damage from projectiles.""", 4),
    "PROTECTION": EnchantmentInfo("""Protection""", "protection", """Reduces most forms of damage.""", 4),
    "PUNCH": EnchantmentInfo("""Punch""", "punch", """Increases arrow knockback.""", 2),
    "QUICK_CHARGE": EnchantmentInfo("""Quick Charge""", "quick_charge", """Increases crossbow charging speed.""", 3),
    "RESPIRATION": EnchantmentInfo("""Respiration""", "respiration", """Extends underwater breathing time.""", 3),
    "RIPTIDE": EnchantmentInfo("""Riptide""", "riptide", """Trident when used launches the wielder while in water or rain, replacing its ability to be thrown as a projectile.""", 3),
    "SHARPNESS": EnchantmentInfo("""Sharpness""", "sharpness", """Increases melee damage.""", 5),
    "SILK_TOUCH": EnchantmentInfo("""Silk Touch""", "silk_touch", """Certain blocks that would otherwise drop different items or nothing will drop themselves instead.""", 1),
    "SMITE": EnchantmentInfo("""Smite""", "smite", """Increases damage dealt against undead mobs.""", 5),
    "SOUL_SPEED": EnchantmentInfo("""Soul Speed""", "soul_speed", """Movement speed on soul sand is increased instead of decreased, and movement speed on soul soil is increased.""", 3),
    "SWEEPING_EDGE": EnchantmentInfo("""Sweeping Edge""", "sweeping_edge", """Increases the damage of a sword sweep attack. This increase applies to nearby entities that are close to the attacked entity, but does not apply to the attacked entity itself.""", 3),
    "SWIFT_SNEAK": EnchantmentInfo("""Swift Sneak""", "swift_sneak", """Lessens the movement speed reduction that occurs when sneaking.""", 3),
    "THORNS": EnchantmentInfo("""Thorns""", "thorns", """Random chance to damage entities that attack the user, at the cost of increasing incurred durability damage.""", 3),
    "UNBREAKING": EnchantmentInfo("""Unbreaking""", "unbreaking", """Gives a chance for items to ignore durability loss, effectively increasing their durability.""", 3),
    "WIND_BURST": EnchantmentInfo("""Wind Burst""", "wind_burst", """Causes a burst of wind upon executing a mace smash attack that launches the attacker upward.""", 3),
    "CLEAVING": EnchantmentInfo("""Cleaving""", "cleaving", """Increases the damage and shield stun time of an axe.""", 3),
}

for __k in tuple(enchantments.keys()):
    v = enchantments[__k]
    enchantments[v.name] = v
    enchantments[v.value] = v


def as_enchantment(*values: StrOrArg) -> str | Tuple[str, ...]:
    return _as_things(ENCHANTMENT_GROUP, __enchantment_dups, *values)



# GameRules
# Derived from https://minecraft.wiki/Game_rule?so=search#List_of_game_rules, 2025-06-30T18:19:23-07:00
__gamerule_dups = {}
ALLOW_FIRE_TICKS_AWAY_FROM_PLAYER = "allowFireTicksAwayFromPlayer"
ANNOUNCE_ADVANCEMENTS = "announceAdvancements"
BLOCK_EXPLOSION_DROP_DECAY = "blockExplosionDropDecay"
COMMAND_BLOCK_OUTPUT = "commandBlockOutput"
COMMAND_MODIFICATION_BLOCK_LIMIT = "commandModificationBlockLimit"
DISABLE_ELYTRA_MOVEMENT_CHECK = "disableElytraMovementCheck"
DISABLE_PLAYER_MOVEMENT_CHECK = "disablePlayerMovementCheck"
DISABLE_RAIDS = "disableRaids"
DO_DAYLIGHT_CYCLE = "doDaylightCycle"
DO_ENTITY_DROPS = "doEntityDrops"
DO_FIRE_TICK = "doFireTick"
DO_IMMEDIATE_RESPAWN = "doImmediateRespawn"
DO_INSOMNIA = "doInsomnia"
DO_LIMITED_CRAFTING = "doLimitedCrafting"
DO_MOB_LOOT = "doMobLoot"
DO_MOB_SPAWNING = "doMobSpawning"
DO_PATROL_SPAWNING = "doPatrolSpawning"
DO_TILE_DROPS = "doTileDrops"
DO_TRADER_SPAWNING = "doTraderSpawning"
DO_VINES_SPREAD = "doVinesSpread"
DO_WEATHER_CYCLE = "doWeatherCycle"
DO_WARDEN_SPAWNING = "doWardenSpawning"
DROWNING_DAMAGE = "drowningDamage"
ENDER_PEARLS_VANISH_ON_DEATH = "enderPearlsVanishOnDeath"
FALL_DAMAGE = "fallDamage"
FIRE_DAMAGE = "fireDamage"
FORGIVE_DEAD_PLAYERS = "forgiveDeadPlayers"
FREEZE_DAMAGE = "freezeDamage"
GLOBAL_SOUND_EVENTS = "globalSoundEvents"
KEEP_INVENTORY = "keepInventory"
LAVA_SOURCE_CONVERSION = "lavaSourceConversion"
LOCATOR_BAR = "locatorBar"
LOG_ADMIN_COMMANDS = "logAdminCommands"
MAX_COMMAND_CHAIN_LENGTH = "maxCommandChainLength"
MAX_COMMAND_FORK_COUNT = "maxCommandForkCount"
MAX_ENTITY_CRAMMING = "maxEntityCramming"
MINECART_MAX_SPEED = "minecartMaxSpeed"
MOB_EXPLOSION_DROP_DECAY = "mobExplosionDropDecay"
MOB_GRIEFING = "mobGriefing"
NATURAL_REGENERATION = "naturalRegeneration"
PLAYERS_NETHER_PORTAL_CREATIVE_DELAY = "playersNetherPortalCreativeDelay"
PLAYERS_NETHER_PORTAL_DEFAULT_DELAY = "playersNetherPortalDefaultDelay"
PLAYERS_SLEEPING_PERCENTAGE = "playersSleepingPercentage"
PROJECTILES_CAN_BREAK_BLOCKS = "projectilesCanBreakBlocks"
RANDOM_TICK_SPEED = "randomTickSpeed"
REDUCED_DEBUG_INFO = "reducedDebugInfo"
SEND_COMMAND_FEEDBACK = "sendCommandFeedback"
SHOW_DEATH_MESSAGES = "showDeathMessages"
SNOW_ACCUMULATION_HEIGHT = "snowAccumulationHeight"
SPAWN_CHUNK_RADIUS = "spawnChunkRadius"
SPAWN_RADIUS = "spawnRadius"
SPECTATORS_GENERATE_CHUNKS = "spectatorsGenerateChunks"
TNT_EXPLODES = "tntExplodes"
TNT_EXPLOSION_DROP_DECAY = "tntExplosionDropDecay"
UNIVERSAL_ANGER = "universalAnger"
WATER_SOURCE_CONVERSION = "waterSourceConversion"
GAME_RULE_GROUP = [
    ALLOW_FIRE_TICKS_AWAY_FROM_PLAYER, ANNOUNCE_ADVANCEMENTS, BLOCK_EXPLOSION_DROP_DECAY, COMMAND_BLOCK_OUTPUT, COMMAND_MODIFICATION_BLOCK_LIMIT, DISABLE_ELYTRA_MOVEMENT_CHECK, DISABLE_PLAYER_MOVEMENT_CHECK, DISABLE_RAIDS, DO_DAYLIGHT_CYCLE, DO_ENTITY_DROPS, DO_FIRE_TICK, DO_IMMEDIATE_RESPAWN, DO_INSOMNIA, DO_LIMITED_CRAFTING, DO_MOB_LOOT, DO_MOB_SPAWNING, DO_PATROL_SPAWNING, DO_TILE_DROPS, DO_TRADER_SPAWNING, DO_VINES_SPREAD, DO_WEATHER_CYCLE, DO_WARDEN_SPAWNING, DROWNING_DAMAGE, ENDER_PEARLS_VANISH_ON_DEATH, FALL_DAMAGE, FIRE_DAMAGE, FORGIVE_DEAD_PLAYERS, FREEZE_DAMAGE, GLOBAL_SOUND_EVENTS, KEEP_INVENTORY, LAVA_SOURCE_CONVERSION, LOCATOR_BAR, LOG_ADMIN_COMMANDS, MAX_COMMAND_CHAIN_LENGTH, MAX_COMMAND_FORK_COUNT, MAX_ENTITY_CRAMMING, MINECART_MAX_SPEED, MOB_EXPLOSION_DROP_DECAY, MOB_GRIEFING, NATURAL_REGENERATION, PLAYERS_NETHER_PORTAL_CREATIVE_DELAY, PLAYERS_NETHER_PORTAL_DEFAULT_DELAY, PLAYERS_SLEEPING_PERCENTAGE, PROJECTILES_CAN_BREAK_BLOCKS, RANDOM_TICK_SPEED, REDUCED_DEBUG_INFO, SEND_COMMAND_FEEDBACK, SHOW_DEATH_MESSAGES, SNOW_ACCUMULATION_HEIGHT, SPAWN_CHUNK_RADIUS, SPAWN_RADIUS, SPECTATORS_GENERATE_CHUNKS, TNT_EXPLODES, TNT_EXPLOSION_DROP_DECAY, UNIVERSAL_ANGER, WATER_SOURCE_CONVERSION
]

GameRuleInfo = namedtuple("GameRule", ['name', 'value', 'desc', 'rule_type'])
game_rules = {
    "ALLOW_FIRE_TICKS_AWAY_FROM_PLAYER": GameRuleInfo("""allow Fire Ticks Away From Player""", "allowFireTicksAwayFromPlayer", """Whether fire and lava ticks can occur outside of an 8 chunk range of a player.""", bool),
    "ANNOUNCE_ADVANCEMENTS": GameRuleInfo("""announce Advancements""", "announceAdvancements", """Whether advancements should be announced in chat.""", bool),
    "BLOCK_EXPLOSION_DROP_DECAY": GameRuleInfo("""block Explosion Drop Decay""", "blockExplosionDropDecay", """Whether block loot is dropped by all blocks (false) or randomly (true) depending on how far the block is from the center of a block explosion (e.g. clicking a bed in dimensions other than the Overworld).""", bool),
    "COMMAND_BLOCK_OUTPUT": GameRuleInfo("""command Block Output""", "commandBlockOutput", """Whether command blocks should notify admins when they perform commands.""", bool),
    "COMMAND_MODIFICATION_BLOCK_LIMIT": GameRuleInfo("""command Modification Block Limit""", "commandModificationBlockLimit", """Controls the maximum number of blocks changed when using /clone, /fill, or /fillbiome.""", int),
    "DISABLE_ELYTRA_MOVEMENT_CHECK": GameRuleInfo("""disable Elytra Movement Check""", "disableElytraMovementCheck", """Whether the server should skip checking player speed when the player is wearing elytra. Often helps with jittering due to lag in multiplayer.""", bool),
    "DISABLE_PLAYER_MOVEMENT_CHECK": GameRuleInfo("""disable Player Movement Check""", "disablePlayerMovementCheck", """Whether the server should skip checking player speed.""", bool),
    "DISABLE_RAIDS": GameRuleInfo("""disable Raids""", "disableRaids", """Whether raids are disabled.""", bool),
    "DO_DAYLIGHT_CYCLE": GameRuleInfo("""do Daylight Cycle""", "doDaylightCycle", """Whether the daylight cycle and moon phases progress.""", bool),
    "DO_ENTITY_DROPS": GameRuleInfo("""do Entity Drops""", "doEntityDrops", """Whether entities that are not mobs should have drops.""", bool),
    "DO_FIRE_TICK": GameRuleInfo("""do Fire Tick""", "doFireTick", """Whether fire should spread and naturally extinguish.""", bool),
    "DO_IMMEDIATE_RESPAWN": GameRuleInfo("""do Immediate Respawn""", "doImmediateRespawn", """Players respawn immediately without showing the death screen.""", bool),
    "DO_INSOMNIA": GameRuleInfo("""do Insomnia""", "doInsomnia", """Whether phantoms can spawn in the nighttime.""", bool),
    "DO_LIMITED_CRAFTING": GameRuleInfo("""do Limited Crafting""", "doLimitedCrafting", """Whether players can craft only those recipes that they have unlocked.""", bool),
    "DO_MOB_LOOT": GameRuleInfo("""do Mob Loot""", "doMobLoot", """Whether mobs should drop items and experience orbs.""", bool),
    "DO_MOB_SPAWNING": GameRuleInfo("""do Mob Spawning""", "doMobSpawning", """Whether mobs should spawn naturally, or via global spawning logic, such as for cats, phantoms, patrols, wandering traders, or zombie sieges. Does not affect special spawning attempts, like monster spawners, raids, or iron golems.""", bool),
    "DO_PATROL_SPAWNING": GameRuleInfo("""do Patrol Spawning""", "doPatrolSpawning", """Whether patrols can spawn.""", bool),
    "DO_TILE_DROPS": GameRuleInfo("""do Tile Drops""", "doTileDrops", """Whether blocks should have drops.""", bool),
    "DO_TRADER_SPAWNING": GameRuleInfo("""do Trader Spawning""", "doTraderSpawning", """Whether wandering traders can spawn.""", bool),
    "DO_VINES_SPREAD": GameRuleInfo("""do Vines Spread""", "doVinesSpread", """Whether vines can spread to other blocks. Cave vines, weeping vines, and twisting vines are not affected.""", bool),
    "DO_WEATHER_CYCLE": GameRuleInfo("""do Weather Cycle""", "doWeatherCycle", """Whether the weather can change naturally. The /weather command can still change weather.""", bool),
    "DO_WARDEN_SPAWNING": GameRuleInfo("""do Warden Spawning""", "doWardenSpawning", """Whether wardens can spawn.""", bool),
    "DROWNING_DAMAGE": GameRuleInfo("""drowning Damage""", "drowningDamage", """Whether the player should take damage when drowning.""", bool),
    "ENDER_PEARLS_VANISH_ON_DEATH": GameRuleInfo("""ender Pearls Vanish On Death""", "enderPearlsVanishOnDeath", """Controls whether thrown ender pearls vanish when the player dies.""", bool),
    "FALL_DAMAGE": GameRuleInfo("""fall Damage""", "fallDamage", """Whether the player should take fall damage.""", bool),
    "FIRE_DAMAGE": GameRuleInfo("""fire Damage""", "fireDamage", """Whether the player should take damage in fire, lava, campfires, or on magma blocks.""", bool),
    "FORGIVE_DEAD_PLAYERS": GameRuleInfo("""forgive Dead Players""", "forgiveDeadPlayers", """Makes angered neutral mobs within 65 x 21 x 65 blocks centered on the targeted player stop being angry when the player dies.""", bool),
    "FREEZE_DAMAGE": GameRuleInfo("""freeze Damage""", "freezeDamage", """Whether the player should take damage when inside powder snow.""", bool),
    "GLOBAL_SOUND_EVENTS": GameRuleInfo("""global Sound Events""", "globalSoundEvents", """Whether the wither's spawning sound, the ender dragon's death sound and the end portal activation sound are heard by all players regardless of location.""", bool),
    "KEEP_INVENTORY": GameRuleInfo("""keep Inventory""", "keepInventory", """Whether the player should keep items and experience in their inventory after death.""", bool),
    "LAVA_SOURCE_CONVERSION": GameRuleInfo("""lava Source Conversion""", "lavaSourceConversion", """Whether new sources of lava are allowed to form.""", bool),
    "LOCATOR_BAR": GameRuleInfo("""locator Bar""", "locatorBar", """Whether the player's locator bar is enabled, indicating the location of players or entities.""", bool),
    "LOG_ADMIN_COMMANDS": GameRuleInfo("""log Admin Commands""", "logAdminCommands", """Whether to log admin commands to server log.""", bool),
    "MAX_COMMAND_CHAIN_LENGTH": GameRuleInfo("""max Command Chain Length""", "maxCommandChainLength", """The maximum length of a chain of commands that can be executed during one tick. Applies to command blocks and functions.""", int),
    "MAX_COMMAND_FORK_COUNT": GameRuleInfo("""max Command Fork Count""", "maxCommandForkCount", """The maximum number of forks (contexts) that can be created during one tick. Applies to command blocks and functions.""", int),
    "MAX_ENTITY_CRAMMING": GameRuleInfo("""max Entity Cramming""", "maxEntityCramming", """The maximum number of pushable entities a mob or player can push, before taking 6HP entity cramming damage per half-second. Setting to 0 or lower disables the rule. Damage affects Survival-mode or Adventure-mode players, and all mobs but bats. Pushable entities include non-Spectator-mode players, any mob except bats, as well as boats and minecarts.""", int),
    "MINECART_MAX_SPEED": GameRuleInfo("""minecart Max Speed""", "minecartMaxSpeed", """The maximum speed a minecart may reach.""", bool),
    "MOB_EXPLOSION_DROP_DECAY": GameRuleInfo("""mob Explosion Drop Decay""", "mobExplosionDropDecay", """Whether block loot is dropped by all blocks (false) or randomly (true) depending on how far the block is from the center of a mob explosion (e.g. Creeper explosion).""", bool),
    "MOB_GRIEFING": GameRuleInfo("""mob Griefing""", "mobGriefing", """Whether creepers, zombies, endermen, ghasts, withers, ender dragons, rabbits, sheep, villagers, silverfish, snow golems, and end crystals.""", bool),
    "NATURAL_REGENERATION": GameRuleInfo("""natural Regeneration""", "naturalRegeneration", """Whether the player can regenerate health naturally if their hunger is full enough (doesn't affect external healing, such as golden apples, the Regeneration effect, etc.).""", bool),
    "PLAYERS_NETHER_PORTAL_CREATIVE_DELAY": GameRuleInfo("""players Nether Portal Creative Delay""", "playersNetherPortalCreativeDelay", """Controls the time that a creative player needs to stand in a nether portal before changing dimensions.""", int),
    "PLAYERS_NETHER_PORTAL_DEFAULT_DELAY": GameRuleInfo("""players Nether Portal Default Delay""", "playersNetherPortalDefaultDelay", """Controls the time that a non-creative player needs to stand in a nether portal before changing dimensions.""", int),
    "PLAYERS_SLEEPING_PERCENTAGE": GameRuleInfo("""players Sleeping Percentage""", "playersSleepingPercentage", """What percentage of players in the Overworld must sleep to skip the night. A percentage value of 0 or less allows the night to be skipped by just 1 player, and a percentage value more than 100 prevents players from skipping the night.""", int),
    "PROJECTILES_CAN_BREAK_BLOCKS": GameRuleInfo("""projectiles Can Break Blocks""", "projectilesCanBreakBlocks", """Whether impact projectiles destroy blocks that are destructible by them, i.e. chorus flowers, pointed dripstone, and decorated pots.""", bool),
    "RANDOM_TICK_SPEED": GameRuleInfo("""random Tick Speed""", "randomTickSpeed", """How often a random block tick occurs (such as plant growth, leaf decay, etc.) per chunk section per game tick. 0 and negative values disables random ticks, higher numbers increase random ticks. Setting to a high integer results in high speeds of decay and growth. Numbers over 4096 make plant growth or leaf decay instantaneous.""", int),
    "REDUCED_DEBUG_INFO": GameRuleInfo("""reduced Debug Info""", "reducedDebugInfo", """Whether the debug screen shows all or reduced information; and whether the effects of F3 + B (entity hitboxes) and F3 + G (chunk boundaries) are shown.""", bool),
    "SEND_COMMAND_FEEDBACK": GameRuleInfo("""send Command Feedback""", "sendCommandFeedback", """Whether the feedback from commands executed by a player should show up in chat. Also affects the default behavior of whether command blocks store their output text.""", bool),
    "SHOW_DEATH_MESSAGES": GameRuleInfo("""show Death Messages""", "showDeathMessages", """Whether death messages are put into chat when a player dies. Also affects whether a message is sent to the pet's owner when the pet dies.""", bool),
    "SNOW_ACCUMULATION_HEIGHT": GameRuleInfo("""snow Accumulation Height""", "snowAccumulationHeight", """The maximum number of snow layers that can be accumulated on each block.""", int),
    "SPAWN_CHUNK_RADIUS": GameRuleInfo("""spawn Chunk Radius""", "spawnChunkRadius", """The size of the spawn chunks of the world.""", bool),
    "SPAWN_RADIUS": GameRuleInfo("""spawn Radius""", "spawnRadius", """The number of blocks outward from the world spawn coordinates that a player spawns in when first joining a server or when dying without a personal spawnpoint. Has no effect on servers where the default game mode is Adventure.""", int),
    "SPECTATORS_GENERATE_CHUNKS": GameRuleInfo("""spectators Generate Chunks""", "spectatorsGenerateChunks", """Whether players in Spectator mode can generate chunks.""", bool),
    "TNT_EXPLODES": GameRuleInfo("""tnt Explodes""", "tntExplodes", """Whether TNT explodes after activation.""", bool),
    "TNT_EXPLOSION_DROP_DECAY": GameRuleInfo("""tnt Explosion Drop Decay""", "tntExplosionDropDecay", """Whether block loot is dropped by all blocks (false) or randomly (true) depending on how far the block is from the center of a TNT explosion.""", bool),
    "UNIVERSAL_ANGER": GameRuleInfo("""universal Anger""", "universalAnger", """Makes angered neutral mobs attack any nearby player, not just the player that angered them. Works best if forgiveDeadPlayers is disabled.""", bool),
    "WATER_SOURCE_CONVERSION": GameRuleInfo("""water Source Conversion""", "waterSourceConversion", """Whether new sources of water are allowed to form.""", bool),
}

for __k in tuple(game_rules.keys()):
    v = game_rules[__k]
    game_rules[v.name] = v
    game_rules[v.value] = v


def as_gamerule(*values: StrOrArg) -> str | Tuple[str, ...]:
    return _as_things(GAME_RULE_GROUP, __gamerule_dups, *values)



# ScoreCriteria
# Derived from https://minecraft.wiki/Scoreboard#Criteria, 2025-06-30T18:19:23-07:00
__scorecriteria_dups = {}
DUMMY = "dummy"
TRIGGER = "trigger"
DEATH_COUNT = "deathCount"
PLAYER_KILL_COUNT = "playerKillCount"
TOTAL_KILL_COUNT = "totalKillCount"
HEALTH = "health"
XP = "xp"
LEVEL = "level"
FOOD = "food"
AIR = "air"
ARMOR = "armor"
SCORE_CRITERIA_GROUP = [
    DUMMY, TRIGGER, DEATH_COUNT, PLAYER_KILL_COUNT, TOTAL_KILL_COUNT, HEALTH, XP, LEVEL, FOOD, AIR, ARMOR
]

ScoreCriteriaInfo = namedtuple("ScoreCriteria", ['name', 'value', 'desc'])
score_criteria = {
    "DUMMY": ScoreCriteriaInfo("""dummy""", "dummy", """A score that can be changed only by commands and not automatically by the game. This can be used for storing integer states and variables, which can then be used with the scoreboard's operations to perform arithmetic calculations."""),
    "TRIGGER": ScoreCriteriaInfo("""trigger""", "trigger", """A score that can be changed by commands and not automatically by the game. The /trigger command allows players to set, increment, or decrement their own score. The command fails if the objective has not been "enabled" for the player using it. After a player uses it, the objective is automatically disabled for them. By default, all trigger objectives are disabled for players. Ordinary players can use the /trigger command, even if cheats are disabled or they are not server operators, making it useful for safely taking input from non-operator players."""),
    "DEATH_COUNT": ScoreCriteriaInfo("""death Count""", "deathCount", """The score increments automatically when a player dies."""),
    "PLAYER_KILL_COUNT": ScoreCriteriaInfo("""player Kill Count""", "playerKillCount", """The score increments automatically when a player kills another player."""),
    "TOTAL_KILL_COUNT": ScoreCriteriaInfo("""total Kill Count""", "totalKillCount", """The score increments automatically when a player kills another player or a mob."""),
    "HEALTH": ScoreCriteriaInfo("""health""", "health", """Ranges from 0 to 20 (and greater) for a normal player; represents the amount of half-hearts a player has. It may appear as 0 for players before their health has changed for the first time. The health score can surpass 20 points with extra hearts from attributes, Health Boost or Absorption effects."""),
    "XP": ScoreCriteriaInfo("""xp""", "xp", """Matches the total amount of experience the player has collected since their last death."""),
    "LEVEL": ScoreCriteriaInfo("""level""", "level", """Matches the current experience level of the player."""),
    "FOOD": ScoreCriteriaInfo("""food""", "food", """Ranges from 0 to 20; represents the amount of hunger points a player has. It may appear as 0 for players before their food level has changed for the first time."""),
    "AIR": ScoreCriteriaInfo("""air""", "air", """Ranges from 0 to 300; represents the amount of air a player has left while swimming underwater. It matches the air NBT tag of the player."""),
    "ARMOR": ScoreCriteriaInfo("""armor""", "armor", """Ranges from 0 to 20; represents the amount of armor points a player has. It may appear as 0 for players before their armor level has changed for the first time."""),
}

for __k in tuple(score_criteria.keys()):
    v = score_criteria[__k]
    score_criteria[v.name] = v
    score_criteria[v.value] = v


def as_scorecriteria(*values: StrOrArg) -> str | Tuple[str, ...]:
    return _as_things(SCORE_CRITERIA_GROUP, __scorecriteria_dups, *values)



# Particles
# Derived from https://minecraft.wiki/Particles_(Java_Edition)#Types_of_particles, 2025-06-30T18:19:23-07:00
__particle_dups = {}
ANGRY_VILLAGER = "angry_villager"
ASH = "ash"
__particle_dups["block"] = "block"
BLOCK_CRUMBLE = "block_crumble"
__particle_dups["block_marker"] = "block_marker"
BUBBLE = "bubble"
BUBBLE_COLUMN_UP = "bubble_column_up"
BUBBLE_POP = "bubble_pop"
CAMPFIRE_COSY_SMOKE = "campfire_cosy_smoke"
CAMPFIRE_SIGNAL_SMOKE = "campfire_signal_smoke"
CHERRY_LEAVES = "cherry_leaves"
CLOUD = "cloud"
COMPOSTER = "composter"
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
__particle_dups["dust_pillar"] = "dust_pillar"
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
__particle_dups["falling_dust"] = "falling_dust"
FALLING_HONEY = "falling_honey"
FALLING_LAVA = "falling_lava"
FALLING_NECTAR = "falling_nectar"
FALLING_OBSIDIAN_TEAR = "falling_obsidian_tear"
FALLING_SPORE_BLOSSOM = "falling_spore_blossom"
FALLING_WATER = "falling_water"
FIREFLY = "firefly"
FIREWORK = "firework"
FISHING = "fishing"
__particle_dups["flame"] = "flame"
FLASH = "flash"
GLOW = "glow"
GLOW_SQUID_INK = "glow_squid_ink"
GUST = "gust"
GUST_EMITTER = "gust_emitter"
HAPPY_VILLAGER = "happy_villager"
HEART = "heart"
__particle_dups["infested"] = "infested"
INSTANT_EFFECT = "instant_effect"
__particle_dups["item"] = "item"
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
OMINOUS_SPAWNING = "ominous_spawning"
PALE_OAK_LEAVES = "pale_oak_leaves"
POOF = "poof"
PORTAL = "portal"
__particle_dups["raid_omen"] = "raid_omen"
__particle_dups["rain"] = "rain"
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
SWEEP_ATTACK = "sweep_attack"
TINTED_LEAVES = "tinted_leaves"
TOTEM_OF_UNDYING = "totem_of_undying"
TRAIL = "trail"
__particle_dups["trial_omen"] = "trial_omen"
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
    ANGRY_VILLAGER, ASH, "block", BLOCK_CRUMBLE, "block_marker", BUBBLE, BUBBLE_COLUMN_UP, BUBBLE_POP, CAMPFIRE_COSY_SMOKE, CAMPFIRE_SIGNAL_SMOKE, CHERRY_LEAVES, CLOUD, COMPOSTER, CRIMSON_SPORE, CRIT, CURRENT_DOWN, DAMAGE_INDICATOR, DOLPHIN, DRAGON_BREATH, DRIPPING_DRIPSTONE_LAVA, DRIPPING_DRIPSTONE_WATER, DRIPPING_HONEY, DRIPPING_LAVA, DRIPPING_OBSIDIAN_TEAR, DRIPPING_WATER, DUST, DUST_COLOR_TRANSITION, "dust_pillar", DUST_PLUME, EFFECT, EGG_CRACK, ELDER_GUARDIAN, ELECTRIC_SPARK, ENCHANT, ENCHANTED_HIT, END_ROD, ENTITY_EFFECT, EXPLOSION, EXPLOSION_EMITTER, FALLING_DRIPSTONE_LAVA, FALLING_DRIPSTONE_WATER, "falling_dust", FALLING_HONEY, FALLING_LAVA, FALLING_NECTAR, FALLING_OBSIDIAN_TEAR, FALLING_SPORE_BLOSSOM, FALLING_WATER, FIREFLY, FIREWORK, FISHING, "flame", FLASH, GLOW, GLOW_SQUID_INK, GUST, GUST_EMITTER, HAPPY_VILLAGER, HEART, "infested", INSTANT_EFFECT, "item", ITEM_COBWEB, ITEM_SLIME, ITEM_SNOWBALL, LANDING_HONEY, LANDING_LAVA, LANDING_OBSIDIAN_TEAR, LARGE_SMOKE, LAVA, MYCELIUM, NAUTILUS, NOTE, OMINOUS_SPAWNING, PALE_OAK_LEAVES, POOF, PORTAL, "raid_omen", "rain", REVERSE_PORTAL, SCRAPE, SCULK_CHARGE, SCULK_CHARGE_POP, SCULK_SOUL, SHRIEK, SMALL_FLAME, SMALL_GUST, SMOKE, SNEEZE, SNOWFLAKE, SONIC_BOOM, SOUL, SOUL_FIRE_FLAME, SPIT, SPLASH, SPORE_BLOSSOM_AIR, SQUID_INK, SWEEP_ATTACK, TINTED_LEAVES, TOTEM_OF_UNDYING, TRAIL, "trial_omen", TRIAL_SPAWNER_DETECTION, TRIAL_SPAWNER_DETECTION_OMINOUS, UNDERWATER, VAULT_CONNECTION, VIBRATION, WARPED_SPORE, "wax_off", "wax_on", WHITE_ASH, WHITE_SMOKE, WITCH
]

ParticleInfo = namedtuple("Particle", ['name', 'value', 'desc'])
particles = {
    "ANGRY_VILLAGER": ParticleInfo("""Angry Villager""", "angry_villager", """Produced when when villagers fail to breed or when a job site block gets unclaimed due to the villager being unable to reach it."""),
    "ASH": ParticleInfo("""Ash""", "ash", """Floats throughout the atmosphere in the soul sand valley biome."""),
    "BLOCK": ParticleInfo("""Block""", "block", """Produced when blocks are broken, flakes off blocks being brushed, produced when iron golems walk, produced when entities fall a long distance, produced when players and cats sprint, displayed when armor stands are broken, appears when sheep eat grass."""),
    "BLOCK_CRUMBLE": ParticleInfo("""Block Crumble""", "block_crumble", """Shown when a creaking heart is destroyed along with its creaking."""),
    "BLOCK_MARKER": ParticleInfo("""Block Marker""", "block_marker", """Marks the position of barriers and light blocks when they are held in the main hand."""),
    "BUBBLE": ParticleInfo("""Bubble""", "bubble", """Appears around entities splashing in water, emitted by guardian lasers, produced by guardians moving, appears by the fishing bobber and along the path of a fish, trails behind projectiles and eyes of ender underwater."""),
    "BUBBLE_COLUMN_UP": ParticleInfo("""Bubble Column Up""", "bubble_column_up", """Represents upward bubble columns."""),
    "BUBBLE_POP": ParticleInfo("""Bubble Pop""", "bubble_pop", """Unused."""),
    "CAMPFIRE_COSY_SMOKE": ParticleInfo("""Campfire Cosy Smoke""", "campfire_cosy_smoke", """Floats off the top of campfires and soul campfires."""),
    "CAMPFIRE_SIGNAL_SMOKE": ParticleInfo("""Campfire Signal Smoke""", "campfire_signal_smoke", """Floats off the top of campfires and soul campfires above hay bales."""),
    "CHERRY_LEAVES": ParticleInfo("""Cherry Leaves""", "cherry_leaves", """Falls off the bottom of cherry leaves."""),
    "CLOUD": ParticleInfo("""Cloud""", "cloud", """Appears when placing wet sponges in the Nether, shown when entering a village with the Bad Omen effect."""),
    "COMPOSTER": ParticleInfo("""Composter""", "composter", """Produced when placing items in a composter."""),
    "CRIMSON_SPORE": ParticleInfo("""Crimson Spore""", "crimson_spore", """Floats throughout the atmosphere in the crimson forest biome."""),
    "CRIT": ParticleInfo("""Crit""", "crit", """Trails behind crossbow shots and fully charged bow shots, produced by evoker fangs, appears when landing a critical hit on an entity."""),
    "CURRENT_DOWN": ParticleInfo("""Current Down""", "current_down", """Represents downward bubble columns."""),
    "DAMAGE_INDICATOR": ParticleInfo("""Damage Indicator""", "damage_indicator", """Appears when a melee attack damages an entity."""),
    "DOLPHIN": ParticleInfo("""Dolphin""", "dolphin", """Trails behind dolphins."""),
    "DRAGON_BREATH": ParticleInfo("""Dragon Breath""", "dragon_breath", """Spit out by the ender dragon, trails behind dragon fireballs, emitted by clouds of dragon's breath, produced when dragon fireballs explode."""),
    "DRIPPING_DRIPSTONE_LAVA": ParticleInfo("""Dripping Dripstone Lava""", "dripping_dripstone_lava", """Represents lava drips collected on pointed dripstone with lava above that have not yet dripped down."""),
    "DRIPPING_DRIPSTONE_WATER": ParticleInfo("""Dripping Dripstone Water""", "dripping_dripstone_water", """Represents water drips collected on pointed dripstone with water or nothing above that have not yet dripped down."""),
    "DRIPPING_HONEY": ParticleInfo("""Dripping Honey""", "dripping_honey", """Represents honey drips collected on the bottom of full bee nests or beehives that have not yet dripped down."""),
    "DRIPPING_LAVA": ParticleInfo("""Dripping Lava""", "dripping_lava", """Represents lava drips collected on the bottom of blocks with lava above that have not yet dripped down."""),
    "DRIPPING_OBSIDIAN_TEAR": ParticleInfo("""Dripping Obsidian Tear""", "dripping_obsidian_tear", """Represents tears collected on the sides or bottom of crying obsidian that have not yet dripped down."""),
    "DRIPPING_WATER": ParticleInfo("""Dripping Water""", "dripping_water", """Represents water drips collected on the bottom of leaves in rain and blocks with water above or the bottom and sides of wet sponges that have not yet dripped down."""),
    "DUST": ParticleInfo("""Dust""", "dust", """Emitted by powered redstone torches, powered levers, redstone ore, powered redstone dust, and powered redstone repeaters."""),
    "DUST_COLOR_TRANSITION": ParticleInfo("""Dust Color Transition""", "dust_color_transition", """Emitted by activated sculk sensors."""),
    "DUST_PILLAR": ParticleInfo("""Dust Pillar""", "dust_pillar", """Produced by mace smash attacks."""),
    "DUST_PLUME": ParticleInfo("""Dust Plume""", "dust_plume", """Shown when adding items to decorated pots."""),
    "EFFECT": ParticleInfo("""Effect""", "effect", """Produced by splash potions."""),
    "EGG_CRACK": ParticleInfo("""Egg Crack""", "egg_crack", """Appears when sniffer eggs are placed on moss blocks, appears when sniffer eggs crack."""),
    "ELDER_GUARDIAN": ParticleInfo("""Elder Guardian""", "elder_guardian", """Displayed when elder guardians inflict Mining Fatigue."""),
    "ELECTRIC_SPARK": ParticleInfo("""Electric Spark""", "electric_spark", """Emitted by lightning rods during thunderstorms, produced when lightning hits copper."""),
    "ENCHANT": ParticleInfo("""Enchant""", "enchant", """Floats from bookshelves to enchanting tables."""),
    "ENCHANTED_HIT": ParticleInfo("""Enchanted Hit""", "enchanted_hit", """Appears when hitting the respective entities with a weapon enchanted with Sharpness, Bane of Arthropods, Smite or Impaling ."""),
    "END_ROD": ParticleInfo("""End Rod""", "end_rod", """Emitted by end rods, trails behind shulker bullets."""),
    "ENTITY_EFFECT": ParticleInfo("""Entity Effect""", "entity_effect", """Emitted by tipped arrows, produced by ravagers when stunned, produced when lingering potions break open, emitted by area effect clouds, produced when evokers cast spells, emitted by the wither as it charges up and when its health is below half, produced by entities with effects from sources other than conduits or beacons."""),
    "EXPLOSION": ParticleInfo("""Explosion""", "explosion", """Produced by explosion_emitter particles, shown when shearing mooshrooms, appears when shulker bullets hit the ground, emitted by the ender dragon as it dies, shown when the ender dragon breaks blocks."""),
    "EXPLOSION_EMITTER": ParticleInfo("""Explosion Emitter""", "explosion_emitter", """Produced by explosions."""),
    "FALLING_DRIPSTONE_LAVA": ParticleInfo("""Falling Dripstone Lava""", "falling_dripstone_lava", """Drips off pointed dripstone with lava above."""),
    "FALLING_DRIPSTONE_WATER": ParticleInfo("""Falling Dripstone Water""", "falling_dripstone_water", """Drips off pointed dripstone with nothing or water above."""),
    "FALLING_DUST": ParticleInfo("""Falling Dust""", "falling_dust", """Falls off the bottom of floating blocks affected by gravity."""),
    "FALLING_HONEY": ParticleInfo("""Falling Honey""", "falling_honey", """Drips off beehives and bee nests that are full of honey."""),
    "FALLING_LAVA": ParticleInfo("""Falling Lava""", "falling_lava", """Drips off the bottom of blocks with lava above."""),
    "FALLING_NECTAR": ParticleInfo("""Falling Nectar""", "falling_nectar", """Falls off bees that have collected pollen."""),
    "FALLING_OBSIDIAN_TEAR": ParticleInfo("""Falling Obsidian Tear""", "falling_obsidian_tear", """Drips off crying obsidian."""),
    "FALLING_SPORE_BLOSSOM": ParticleInfo("""Falling Spore Blossom""", "falling_spore_blossom", """Drips off of spore blossoms."""),
    "FALLING_WATER": ParticleInfo("""Falling Water""", "falling_water", """Drips off of the bottom of blocks with water above, drips off the bottom of leaves during rain, drips off of wet sponges."""),
    "FIREFLY": ParticleInfo("""Firefly""", "firefly", """Spawns from firefly bushes when the internal light level is at 13 or lower."""),
    "FIREWORK": ParticleInfo("""Firework""", "firework", """Trails behind fireworks, produced when fireworks crafted with firework stars explode."""),
    "FISHING": ParticleInfo("""Fishing""", "fishing", """Represents the fish trail when fishing."""),
    "FLAME": ParticleInfo("""Flame""", "flame", """Appears inside of monster spawners, produced by magma cubes, represents the flame of torches, emitted by furnaces."""),
    "FLASH": ParticleInfo("""Flash""", "flash", """Shown when fireworks with crafted with firework stars explode."""),
    "GLOW": ParticleInfo("""Glow""", "glow", """Emitted by glow squid."""),
    "GLOW_SQUID_INK": ParticleInfo("""Glow Squid Ink""", "glow_squid_ink", """Produced by glow squid when hit."""),
    "GUST": ParticleInfo("""Gust""", "gust", """Created when a wind charge hits a block."""),
    "GUST_EMITTER": ParticleInfo("""Gust Emitter""", "gust_emitter", """Created when a wind charge hits a block. Spawns a number of gust particles."""),
    "HAPPY_VILLAGER": ParticleInfo("""Happy Villager""", "happy_villager", """Shown when using bone meal on plants, appears when trading with villagers, appears when feeding baby animals or dolphins, emitted by villagers upon claiming a job site block or a bed, shown when bees pollinate crops, appears when turtle eggs are placed on sand, appears when turtle eggs hatch."""),
    "HEART": ParticleInfo("""Heart""", "heart", """Appears when taming mobs, emitted by breeding mobs, feeding mobs, appears when allays duplicate."""),
    "INFESTED": ParticleInfo("""Infested""", "infested", """Produced by entities with the Infested effect."""),
    "INSTANT_EFFECT": ParticleInfo("""Instant Effect""", "instant_effect", """Produced when splash potions or lingering potions of Instant Health or Instant Damage break. Also produced trailing spectral arrow entities."""),
    "ITEM": ParticleInfo("""Item""", "item", """Produced when tools break, produced when eating food, produced when splash potions or lingering potions break, shown when eyes of ender break."""),
    "ITEM_COBWEB": ParticleInfo("""Item Cobweb""", "item_cobweb", """Produced by entities with the Weaving effect."""),
    "ITEM_SLIME": ParticleInfo("""Item Slime""", "item_slime", """Shown when slimes jump and produced by entities with the Oozing effect."""),
    "ITEM_SNOWBALL": ParticleInfo("""Item Snowball""", "item_snowball", """Produced when thrown snowballs break."""),
    "LANDING_HONEY": ParticleInfo("""Landing Honey""", "landing_honey", """Created when falling_honey particles hit the ground."""),
    "LANDING_LAVA": ParticleInfo("""Landing Lava""", "landing_lava", """Created when falling_lava or falling_dripstone_lava particles hit the ground."""),
    "LANDING_OBSIDIAN_TEAR": ParticleInfo("""Landing Obsidian Tear""", "landing_obsidian_tear", """Created when falling_obsidian_tear particles hit the ground."""),
    "LARGE_SMOKE": ParticleInfo("""Large Smoke""", "large_smoke", """Floats off the top of fire, produced by blazes, appears when trying to place water in the Nether, appears when obsidian, stone, or cobblestone is created by lava and water."""),
    "LAVA": ParticleInfo("""Lava""", "lava", """Produced by campfires, produced by lava."""),
    "MYCELIUM": ParticleInfo("""Mycelium""", "mycelium", """Appears above mycelium, trails behind the wings of phantoms."""),
    "NAUTILUS": ParticleInfo("""Nautilus""", "nautilus", """Appears and floats toward conduits, appears and floats toward mobs being attacked by a conduit."""),
    "NOTE": ParticleInfo("""Note""", "note", """Produced by jukeboxes, produced by note blocks."""),
    "OMINOUS_SPAWNING": ParticleInfo("""Ominous Spawning""", "ominous_spawning", """Appears when an ominous item spawner spawns a item during an ominous event."""),
    "PALE_OAK_LEAVES": ParticleInfo("""Pale Oak Leaves""", "pale_oak_leaves", """Falls off the bottom of pale oak leaves."""),
    "POOF": ParticleInfo("""Poof""", "poof", """Appears when mobs die, shown when ravagers roar after being stunned, produced when silverfish enter stone, appear around mobs spawned by spawners, shown when zombies trample turtle eggs, created when fireworks crafted without stars expire."""),
    "PORTAL": ParticleInfo("""Portal""", "portal", """Trails behind eyes of ender, shown when eyes of ender break, floats toward where ender pearls break, points toward where dragon eggs teleport, floats toward where players teleport with chorus fruit, appears and floats toward nether portals, appears and floats toward end gateway portals, appears and floats toward ender chests, emitted by endermen, appears and floats toward endermites."""),
    "RAID_OMEN": ParticleInfo("""Raid Omen""", "raid_omen", """Produced by players and mobs with the Raid Omen effect."""),
    "RAIN": ParticleInfo("""Rain""", "rain", """Appears on the ground during rain."""),
    "REVERSE_PORTAL": ParticleInfo("""Reverse Portal""", "reverse_portal", """Floats off the top of respawn anchors that have some level of charge."""),
    "SCRAPE": ParticleInfo("""Scrape""", "scrape", """Shown when scraping oxidization off copper."""),
    "SCULK_CHARGE": ParticleInfo("""Sculk Charge""", "sculk_charge", """Marks the path of a sculk charge."""),
    "SCULK_CHARGE_POP": ParticleInfo("""Sculk Charge Pop""", "sculk_charge_pop", """Appears when a sculk charge ends."""),
    "SCULK_SOUL": ParticleInfo("""Sculk Soul""", "sculk_soul", """Appears above sculk catalysts when activated."""),
    "SHRIEK": ParticleInfo("""Shriek""", "shriek", """Emitted by activated sculk shriekers."""),
    "SMALL_FLAME": ParticleInfo("""Small Flame""", "small_flame", """Represents the flame of candles."""),
    "SMALL_GUST": ParticleInfo("""Small Gust""", "small_gust", """Produced by mobs with the Wind Charged effect."""),
    "SMOKE": ParticleInfo("""Smoke""", "smoke", """Floats off the top of monster spawners, represents the smoke from candles, appears when TNT is primed, floats off the top of wither roses, floats off the top of brewing stands, represents the smoke of torches and soul torches, trails behind ghast fireballs, emitted by withers, trails behind wither skulls, produced when dispensers or droppers fire, trails behind blaze fireballs, emitted by lava and campfires during rain, emitted by furnaces, emitted by blast furnaces, emitted by smokers, produced when placing eyes of ender in an end portal frame, emitted by end portals, produced when redstone torches burn out, floats off the top of food placed on a campfire, shown when campfires and soul campfires are extinguished, shown when failing to tame a mob, trails behind lava particles."""),
    "SNEEZE": ParticleInfo("""Sneeze""", "sneeze", """Sneezed out by pandas."""),
    "SNOWFLAKE": ParticleInfo("""Snowflake""", "snowflake", """Created by entities in powder snow."""),
    "SONIC_BOOM": ParticleInfo("""Sonic Boom""", "sonic_boom", """Produced by the warden during its sonic boom attack."""),
    "SOUL": ParticleInfo("""Soul""", "soul", """Created by players with Soul Speed boots running on soul sand or soul soil."""),
    "SOUL_FIRE_FLAME": ParticleInfo("""Soul Fire Flame""", "soul_fire_flame", """Represents the flame of soul torches."""),
    "SPIT": ParticleInfo("""Spit""", "spit", """Spit out by llamas."""),
    "SPLASH": ParticleInfo("""Splash""", "splash", """Produced by entities splashing in water, produced by villagers sweating during a raid, appears above the surface of the water when fishing, created when falling_water or falling_dripstone_water particles hit the ground, shaken off by wolves after exiting water."""),
    "SPORE_BLOSSOM_AIR": ParticleInfo("""Spore Blossom Air""", "spore_blossom_air", """Floats in the atmosphere around spore blossoms."""),
    "SQUID_INK": ParticleInfo("""Squid Ink""", "squid_ink", """Produced by squid when hit."""),
    "SWEEP_ATTACK": ParticleInfo("""Sweep Attack""", "sweep_attack", """Appears when a sweeping attack is performed."""),
    "TINTED_LEAVES": ParticleInfo("""Tinted Leaves""", "tinted_leaves", """Falls off the bottom of any type leaves except pale oak leaves. Its color corresponds to the leaves block its falling off."""),
    "TOTEM_OF_UNDYING": ParticleInfo("""Totem Of Undying""", "totem_of_undying", """Produced when a totem of undying is used."""),
    "TRAIL": ParticleInfo("""Trail""", "trail", """Trace a trail between two points. Shown when the creaking is attacked, to link it to its heart, and when eyeblossoms open or close."""),
    "TRIAL_OMEN": ParticleInfo("""Trial Omen""", "trial_omen", """Produced by players and mobs with the Trial Omen effect."""),
    "TRIAL_SPAWNER_DETECTION": ParticleInfo("""Trial Spawner Detection""", "trial_spawner_detection", """Produced when a trial spawner is activated."""),
    "TRIAL_SPAWNER_DETECTION_OMINOUS": ParticleInfo("""Trial Spawner Detection Ominous""", "trial_spawner_detection_ominous", """Produced when an ominous trial spawner is activated."""),
    "UNDERWATER": ParticleInfo("""Underwater""", "underwater", """Floats in the atmosphere underwater."""),
    "VAULT_CONNECTION": ParticleInfo("""Vault Connection""", "vault_connection", """Produced when a player is near a vault."""),
    "VIBRATION": ParticleInfo("""Vibration""", "vibration", """Moves from sounds to the warden or a sculk sensor, moves from note blocks to allays."""),
    "WARPED_SPORE": ParticleInfo("""Warped Spore""", "warped_spore", """Floats in the atmosphere in warped forest biomes."""),
    "WAX_OFF": ParticleInfo("""Wax Off""", "wax_off", """Produced when scraping wax off copper."""),
    "WAX_ON": ParticleInfo("""Wax On""", "wax_on", """Produced when using honeycomb on copper."""),
    "WHITE_ASH": ParticleInfo("""White Ash""", "white_ash", """Floats in the atmosphere in basalt delta biomes."""),
    "WHITE_SMOKE": ParticleInfo("""White Smoke""", "white_smoke", """Emitted by crafters when ejecting an item."""),
    "WITCH": ParticleInfo("""Witch""", "witch", """Emitted by witches."""),
}

for __k in tuple(particles.keys()):
    v = particles[__k]
    particles[v.name] = v
    particles[v.value] = v


def as_particle(*values: StrOrArg) -> str | Tuple[str, ...]:
    return _as_things(PARTICLE_GROUP, __particle_dups, *values)



# PotterySherds
# Derived from https://minecraft.wiki/Pottery_Sherd, 2025-06-30T18:19:23-07:00
__potterysherd_dups = {}
SCRAPE_POTTERY_SHERD = "scrape_pottery_sherd"
GUSTER_POTTERY_SHERD = "guster_pottery_sherd"
FLOW_POTTERY_SHERD = "flow_pottery_sherd"
SKULL_POTTERY_SHERD = "skull_pottery_sherd"
ARMS_UP_POTTERY_SHERD = "arms_up_pottery_sherd"
BREWER_POTTERY_SHERD = "brewer_pottery_sherd"
ANGLER_POTTERY_SHERD = "angler_pottery_sherd"
SHELTER_POTTERY_SHERD = "shelter_pottery_sherd"
SNORT_POTTERY_SHERD = "snort_pottery_sherd"
BLADE_POTTERY_SHERD = "blade_pottery_sherd"
EXPLORER_POTTERY_SHERD = "explorer_pottery_sherd"
MOURNER_POTTERY_SHERD = "mourner_pottery_sherd"
PLENTY_POTTERY_SHERD = "plenty_pottery_sherd"
BURN_POTTERY_SHERD = "burn_pottery_sherd"
DANGER_POTTERY_SHERD = "danger_pottery_sherd"
FRIEND_POTTERY_SHERD = "friend_pottery_sherd"
HEART_POTTERY_SHERD = "heart_pottery_sherd"
HEARTBREAK_POTTERY_SHERD = "heartbreak_pottery_sherd"
HOWL_POTTERY_SHERD = "howl_pottery_sherd"
SHEAF_POTTERY_SHERD = "sheaf_pottery_sherd"
POTTERY_SHERD_GROUP = [
    SCRAPE_POTTERY_SHERD, GUSTER_POTTERY_SHERD, FLOW_POTTERY_SHERD, SKULL_POTTERY_SHERD, ARMS_UP_POTTERY_SHERD, BREWER_POTTERY_SHERD, ANGLER_POTTERY_SHERD, SHELTER_POTTERY_SHERD, SNORT_POTTERY_SHERD, BLADE_POTTERY_SHERD, EXPLORER_POTTERY_SHERD, MOURNER_POTTERY_SHERD, PLENTY_POTTERY_SHERD, BURN_POTTERY_SHERD, DANGER_POTTERY_SHERD, FRIEND_POTTERY_SHERD, HEART_POTTERY_SHERD, HEARTBREAK_POTTERY_SHERD, HOWL_POTTERY_SHERD, SHEAF_POTTERY_SHERD
]

PotterySherdInfo = namedtuple("PotterySherd", ['name', 'value', 'desc'])
pottery_sherds = {
    "SCRAPE_POTTERY_SHERD": PotterySherdInfo("""Scrape Pottery Sherd""", "scrape_pottery_sherd", None),
    "GUSTER_POTTERY_SHERD": PotterySherdInfo("""Guster Pottery Sherd""", "guster_pottery_sherd", None),
    "FLOW_POTTERY_SHERD": PotterySherdInfo("""Flow Pottery Sherd""", "flow_pottery_sherd", None),
    "SKULL_POTTERY_SHERD": PotterySherdInfo("""Skull Pottery Sherd""", "skull_pottery_sherd", None),
    "ARMS_UP_POTTERY_SHERD": PotterySherdInfo("""Arms Up Pottery Sherd""", "arms_up_pottery_sherd", None),
    "BREWER_POTTERY_SHERD": PotterySherdInfo("""Brewer Pottery Sherd""", "brewer_pottery_sherd", None),
    "ANGLER_POTTERY_SHERD": PotterySherdInfo("""Angler Pottery Sherd""", "angler_pottery_sherd", None),
    "SHELTER_POTTERY_SHERD": PotterySherdInfo("""Shelter Pottery Sherd""", "shelter_pottery_sherd", None),
    "SNORT_POTTERY_SHERD": PotterySherdInfo("""Snort Pottery Sherd""", "snort_pottery_sherd", None),
    "BLADE_POTTERY_SHERD": PotterySherdInfo("""Blade Pottery Sherd""", "blade_pottery_sherd", None),
    "EXPLORER_POTTERY_SHERD": PotterySherdInfo("""Explorer Pottery Sherd""", "explorer_pottery_sherd", None),
    "MOURNER_POTTERY_SHERD": PotterySherdInfo("""Mourner Pottery Sherd""", "mourner_pottery_sherd", None),
    "PLENTY_POTTERY_SHERD": PotterySherdInfo("""Plenty Pottery Sherd""", "plenty_pottery_sherd", None),
    "BURN_POTTERY_SHERD": PotterySherdInfo("""Burn Pottery Sherd""", "burn_pottery_sherd", None),
    "DANGER_POTTERY_SHERD": PotterySherdInfo("""Danger Pottery Sherd""", "danger_pottery_sherd", None),
    "FRIEND_POTTERY_SHERD": PotterySherdInfo("""Friend Pottery Sherd""", "friend_pottery_sherd", None),
    "HEART_POTTERY_SHERD": PotterySherdInfo("""Heart Pottery Sherd""", "heart_pottery_sherd", None),
    "HEARTBREAK_POTTERY_SHERD": PotterySherdInfo("""Heartbreak Pottery Sherd""", "heartbreak_pottery_sherd", None),
    "HOWL_POTTERY_SHERD": PotterySherdInfo("""Howl Pottery Sherd""", "howl_pottery_sherd", None),
    "SHEAF_POTTERY_SHERD": PotterySherdInfo("""Sheaf Pottery Sherd""", "sheaf_pottery_sherd", None),
}

for __k in tuple(pottery_sherds.keys()):
    v = pottery_sherds[__k]
    pottery_sherds[v.name] = v
    pottery_sherds[v.value] = v


def as_potterysherd(*values: StrOrArg) -> str | Tuple[str, ...]:
    return _as_things(POTTERY_SHERD_GROUP, __potterysherd_dups, *values)



# Discs
# Derived from https://minecraft.wiki/Music_Disc#Discs, 2025-06-30T18:19:24-07:00
__disc_dups = {}
THIRTEEN = "music_disc_13"
CAT = "music_disc_cat"
BLOCKS = "music_disc_blocks"
CHIRP = "music_disc_chirp"
FAR = "music_disc_far"
MALL = "music_disc_mall"
MELLOHI = "music_disc_mellohi"
STAL = "music_disc_stal"
STRAD = "music_disc_strad"
WARD = "music_disc_ward"
ELEVEN = "music_disc_11"
WAIT = "music_disc_wait"
PIGSTEP = "music_disc_pigstep"
OTHERSIDE = "music_disc_otherside"
CREATOR = "music_disc_creator"
CREATOR_MUSIC_BOX = "music_disc_creator_music_box"
FIVE = "music_disc_5"
RELIC = "music_disc_relic"
PRECIPICE = "music_disc_precipice"
TEARS = "music_disc_tears"
LAVA_CHICKEN = "music_disc_lava_chicken"
DISC_GROUP = [
    THIRTEEN, CAT, BLOCKS, CHIRP, FAR, MALL, MELLOHI, STAL, STRAD, WARD, ELEVEN, WAIT, PIGSTEP, OTHERSIDE, CREATOR, CREATOR_MUSIC_BOX, FIVE, RELIC, PRECIPICE, TEARS, LAVA_CHICKEN
]

DiscInfo = namedtuple("Disc", ['name', 'value', 'desc', 'composer'])
discs = {
    "THIRTEEN": DiscInfo("""thirteen""", "music_disc_13", None, "C418"),
    "CAT": DiscInfo("""cat""", "music_disc_cat", None, ""),
    "BLOCKS": DiscInfo("""blocks""", "music_disc_blocks", None, ""),
    "CHIRP": DiscInfo("""chirp""", "music_disc_chirp", None, ""),
    "FAR": DiscInfo("""far""", "music_disc_far", None, ""),
    "MALL": DiscInfo("""mall""", "music_disc_mall", None, ""),
    "MELLOHI": DiscInfo("""mellohi""", "music_disc_mellohi", None, ""),
    "STAL": DiscInfo("""stal""", "music_disc_stal", None, ""),
    "STRAD": DiscInfo("""strad""", "music_disc_strad", None, ""),
    "WARD": DiscInfo("""ward""", "music_disc_ward", None, ""),
    "ELEVEN": DiscInfo("""eleven""", "music_disc_11", None, ""),
    "WAIT": DiscInfo("""wait""", "music_disc_wait", None, ""),
    "PIGSTEP": DiscInfo("""Pigstep""", "music_disc_pigstep", None, "Lena Raine"),
    "OTHERSIDE": DiscInfo("""otherside""", "music_disc_otherside", None, ""),
    "CREATOR": DiscInfo("""Creator""", "music_disc_creator", None, ""),
    "CREATOR_MUSIC_BOX": DiscInfo("""Creator Music Box""", "music_disc_creator_music_box", None, ""),
    "FIVE": DiscInfo("""five""", "music_disc_5", None, "Samuel Åberg"),
    "RELIC": DiscInfo("""Relic""", "music_disc_relic", None, "Aaron Cherof"),
    "PRECIPICE": DiscInfo("""Precipice""", "music_disc_precipice", None, ""),
    "TEARS": DiscInfo("""Tears""", "music_disc_tears", None, "Amos Roddy"),
    "LAVA_CHICKEN": DiscInfo("""Lava Chicken""", "music_disc_lava_chicken", None, "Hyper Potions"),
}

for __k in tuple(discs.keys()):
    v = discs[__k]
    discs[v.name] = v
    discs[v.value] = v


def as_disc(*values: StrOrArg) -> str | Tuple[str, ...]:
    return _as_things(DISC_GROUP, __disc_dups, *values)



# Paintings
# Derived from https://minecraft.wiki/Painting#Canvases, 2025-06-30T18:19:24-07:00
__painting_dups = {}
KEBAB = "Kebab med tre pepperoni"
AZTEC = "de_aztec"
ALBAN = "Albanian"
AZTEC2 = "de_aztec 2"
BOMB = "Target Successfully Bombed"
PLANT = "Paradisträd"
WASTELAND = "Wasteland"
MEDITATIVE = "Meditative"
WANDERER = "Wanderer"
GRAHAM = "Graham"
PRAIRIE_RIDE = "Prairie Ride"
POOL = "The Pool"
COURBET = "Bonjour Monsieur Courbet"
__painting_dups["sunset"] = "sunset_dense"
SEA = "Seaside"
CREEBET = "Creebet"
MATCH = "Match"
BUST = "Bust"
STAGE = "The Stage Is Set"
VOID = "The void"
SKULL_AND_ROSES = "Skull and Roses"
__painting_dups["wither"] = "Wither"
BAROQUE = "Baroque"
HUMBLE = "Humble"
BOUQUET = "Bouquet"
CAVEBIRD = "Cavebird"
COTAN = "Cotán"
ENDBOSS = "Endboss"
FERN = "Fern"
OWLEMONS = "Owlemons"
SUNFLOWERS = "Sunflowers"
TIDES = "Tides"
DENNIS = "Dennis"
BACKYARD = "Backyard"
POND = "Pond"
FIGHTERS = "Fighters"
CHANGING = "Changing"
FINDING = "Finding"
LOWMIST = "Lowmist"
PASSAGE = "Passage"
SKELETON = "Mortal Coil"
DONKEY_KONG = "Kong"
POINTER = "Pointer"
PIGSCENE = "Pigscene"
BURNING_SKULL = "Skull On Fire"
ORB = "Orb"
UNPACKED = "Unpacked"
EARTH = "Earth"
WIND = "Wind"
FIRE = "Fire"
WATER = "Water"
PAINTING_GROUP = [
    KEBAB, AZTEC, ALBAN, AZTEC2, BOMB, PLANT, WASTELAND, MEDITATIVE, WANDERER, GRAHAM, PRAIRIE_RIDE, POOL, COURBET, "sunset_dense", SEA, CREEBET, MATCH, BUST, STAGE, VOID, SKULL_AND_ROSES, "Wither", BAROQUE, HUMBLE, BOUQUET, CAVEBIRD, COTAN, ENDBOSS, FERN, OWLEMONS, SUNFLOWERS, TIDES, DENNIS, BACKYARD, POND, FIGHTERS, CHANGING, FINDING, LOWMIST, PASSAGE, SKELETON, DONKEY_KONG, POINTER, PIGSCENE, BURNING_SKULL, ORB, UNPACKED, EARTH, WIND, FIRE, WATER
]

PaintingInfo = namedtuple("Painting", ['name', 'value', 'desc', 'artist', 'size'])
paintings = {
    "KEBAB": PaintingInfo("""kebab""", "Kebab med tre pepperoni", """A kebab with three green chili peppers.""", "Kristoffer Zetterstrand", (1, 1)),
    "AZTEC": PaintingInfo("""aztec""", "de_aztec", """Free-look perspective of the map Aztec from the video game series Counter-Strike.""", "Kristoffer Zetterstrand", (1, 1)),
    "ALBAN": PaintingInfo("""alban""", "Albanian", """A man wearing a fez next to a house and a bush. As the name of the painting suggests, it may be a landscape in Albania.""", "Kristoffer Zetterstrand", (1, 1)),
    "AZTEC2": PaintingInfo("""aztec2""", "de_aztec 2", """Free-look perspective of the map Aztec from the video game series Counter-Strike.""", "Kristoffer Zetterstrand", (1, 1)),
    "BOMB": PaintingInfo("""bomb""", "Target Successfully Bombed", """The map Dust II from the video game series Counter-Strike, named “target successfully bombed” in reference to the video game.""", "Kristoffer Zetterstrand", (1, 1)),
    "PLANT": PaintingInfo("""plant""", "Paradisträd", """Still life of two plants in pots. “Paradisträd” is Swedish for “jade plant”, which is a common name for the depicted species in Scandinavia.""", "Kristoffer Zetterstrand", (1, 1)),
    "WASTELAND": PaintingInfo("""wasteland""", "Wasteland", """A view of some wasteland; a small animal, presumably a rabbit, is sitting on the windowsill.""", "Kristoffer Zetterstrand", (1, 1)),
    "MEDITATIVE": PaintingInfo("""meditative""", "Meditative", """A version of Salvador Dali’s Meditative Rose. Its added stem references Minecraft’s removed rose.""", "Sarah Boeving", (1, 1)),
    "WANDERER": PaintingInfo("""wanderer""", "Wanderer", """A version of Caspar David Friedrich’s famous painting Wanderer above the Sea of Fog.""", "Kristoffer Zetterstrand", (1, 2)),
    "GRAHAM": PaintingInfo("""graham""", "Graham", """King Graham, the player character in the video game series King’s Quest. The original painting is based on Still Life with Quince, Cabbage, Melon, and Cucumber by Juan Sánchez Cotán.""", "Kristoffer Zetterstrand", (1, 2)),
    "PRAIRIE_RIDE": PaintingInfo("""prairie_ride""", "Prairie Ride", """A version of Frederic Remington’s The Cowboy. Instead of a cowboy, it shows Noor riding a horse.""", "Sarah Boeving", (1, 2)),
    "POOL": PaintingInfo("""pool""", "The Pool", """Some men and women skinny-dipping in a pool over a cube of sorts. Also there is an old man resting in the lower-right edge.""", "Kristoffer Zetterstrand", (2, 1)),
    "COURBET": PaintingInfo("""courbet""", "Bonjour Monsieur Courbet", """Two hikers with pointy beards seemingly greeting each other. Based on Gustave Courbet’s painting The Meeting.""", "Kristoffer Zetterstrand", (2, 1)),
    "SUNSET": PaintingInfo("""sunset""", "sunset_dense", """A view of mountains at sunset.""", "Kristoffer Zetterstrand", (2, 1)),
    "SEA": PaintingInfo("""sea""", "Seaside", """Mountains and a lake, with a small photo of a mountain and a bright-colored plant on the window ledge. The texture was changed in Alpha v1.1.1.""", "Kristoffer Zetterstrand", (2, 1)),
    "CREEBET": PaintingInfo("""creebet""", "Creebet", """The same painting as Seaside, but the bright-colored plant was replaced with a Creeper head.""", "Kristoffer Zetterstrand", (2, 1)),
    "MATCH": PaintingInfo("""match""", "Match", """A hand holding a match, causing fire on a white cubic gas fireplace.""", "Kristoffer Zetterstrand", (2, 2)),
    "BUST": PaintingInfo("""bust""", "Bust", """A bust of Marcus Aurelius surrounded by fire.""", "Kristoffer Zetterstrand", (2, 2)),
    "STAGE": PaintingInfo("""stage""", "The Stage Is Set", """Scenery from the video game Space Quest I, with the character Graham from the video game series King’s Quest appearing twice. The texture was changed in Alpha v1.1.1.""", "Kristoffer Zetterstrand", (2, 2)),
    "VOID": PaintingInfo("""void""", "The void", """An angel praying into a void with fire below.""", "Kristoffer Zetterstrand", (2, 2)),
    "SKULL_AND_ROSES": PaintingInfo("""skull_and_roses""", "Skull and Roses", """A skeleton at night with red flowers in the foreground. The original painting is different, depicting a woman sitting in a couch, while the skull is in the middle of a body of glacial water of sorts.""", "Kristoffer Zetterstrand", (2, 2)),
    "WITHER": PaintingInfo("""wither""", "Wither", """The creation of the wither. This is the first painting in Minecraft that is not based on a real painting. (See the trivia section for more info.).""", "Mojang(Jens Bergensten)", (2, 2)),
    "BAROQUE": PaintingInfo("""baroque""", "Baroque", """A decorated pot, a cake, and a sunflower on a dark background, resembling Baroque painting.""", "Sarah Boeving", (2, 2)),
    "HUMBLE": PaintingInfo("""humble""", "Humble", """A version of Grant Wood’s American Gothic, where two villagers are in front of a village house.""", "Sarah Boeving", (2, 2)),
    "BOUQUET": PaintingInfo("""bouquet""", "Bouquet", """A bouquet of flowers next to a stairway with a person sitting beside it.""", "Kristoffer Zetterstrand", (3, 3)),
    "CAVEBIRD": PaintingInfo("""cavebird""", "Cavebird", """A cave in a cliff with a bird flying overhead.""", "Kristoffer Zetterstrand", (3, 3)),
    "COTAN": PaintingInfo("""cotan""", "Cotán", """A golden apple and an inverted glistering melon slice in a windowsill. The golden apple is tied by a string in the air and the glistering melon slice is sitting on the windowsill. Like Graham, this painting is based on Still Life with Quince, Cabbage, Melon, and Cucumber by Juan Sánchez Cotán.""", "Kristoffer Zetterstrand", (3, 3)),
    "ENDBOSS": PaintingInfo("""endboss""", "Endboss", """A skeleton in a brick archway. It features a white silhouette of the character Graham from the video game series King’s Quest.""", "Kristoffer Zetterstrand", (3, 3)),
    "FERN": PaintingInfo("""fern""", "Fern", """A potted fern on a desk with a small fire.""", "Kristoffer Zetterstrand", (3, 3)),
    "OWLEMONS": PaintingInfo("""owlemons""", "Owlemons", """A two-dimensional owl inside a box, next to some lemons. The background is based on the painting An Old Man and his Grandson by Domenico Ghirlandaio.""", "Kristoffer Zetterstrand", (3, 3)),
    "SUNFLOWERS": PaintingInfo("""sunflowers""", "Sunflowers", """Some potted plants on a table with a two-dimensional sunflower.""", "Kristoffer Zetterstrand", (3, 3)),
    "TIDES": PaintingInfo("""tides""", "Tides", """A person sitting in a fetal position by a shoreline. The naked person from the original painting has been given clothes.""", "Kristoffer Zetterstrand", (3, 3)),
    "DENNIS": PaintingInfo("""dennis""", "Dennis", """A painting of a pale wolf, inspired by a painting depicting Dennis seen in A Minecraft Movie.""", "Sarah Boeving", (3, 3)),
    "BACKYARD": PaintingInfo("""backyard""", "Backyard", """A brick archway with two women sitting in the yard. The scenery is based on the painting The Courtyard of a House in Delft by Pieter de Hooch.""", "Kristoffer Zetterstrand", (3, 4)),
    "POND": PaintingInfo("""pond""", "Pond", """A maiden sitting in a pond, next to a half-submerged skeleton. Death and the Maiden was a common motif in Renaissance art, ultimately derived from the Medieval genre Dance of Death.""", "Kristoffer Zetterstrand", (3, 4)),
    "FIGHTERS": PaintingInfo("""fighters""", "Fighters", """Two men poised to fight. The fighters are from the video game The Way of the Exploding Fist.""", "Kristoffer Zetterstrand", (4, 2)),
    "CHANGING": PaintingInfo("""changing""", "Changing", """A person changing clothes in front of some set pieces, including a contrasting gloomy mountain and a sunny countryside.""", "Kristoffer Zetterstrand", (4, 2)),
    "FINDING": PaintingInfo("""finding""", "Finding", """A person looks into a recently-dug hole with Hellenistic ruins in the background. Studio lights are set up next to them.""", "Kristoffer Zetterstrand", (4, 2)),
    "LOWMIST": PaintingInfo("""lowmist""", "Lowmist", """A digital render of a mountainous landscape. This motif was created using the scenery generator Terragen, with the renderer deliberately crashed during the construction process.""", "Kristoffer Zetterstrand", (4, 2)),
    "PASSAGE": PaintingInfo("""passage""", "Passage", """A surreal, mineshaft-like hallway in front of a scene of a beach, with posed skeletons of a person and an extinct giant ground sloth.""", "Kristoffer Zetterstrand", (4, 2)),
    "SKELETON": PaintingInfo("""skeleton""", "Mortal Coil", """Bruno Martinez from the adventure video game Grim Fandango.""", "Kristoffer Zetterstrand", (4, 3)),
    "DONKEY_KONG": PaintingInfo("""donkey_kong""", "Kong", """A paper-looking screenshot of the level 100m from the arcade video game Donkey Kong.""", "Kristoffer Zetterstrand", (4, 3)),
    "POINTER": PaintingInfo("""pointer""", "Pointer", """The main character of the video game International Karate + in a fighting stance touching a large hand. It could also be interpreted as a play on Michelangelo’s famous painting The Creation of Adam. The hand is the artist’s own. The scenery is based on the painting Winter Landscape with Church by Caspar David Friedrich.""", "Kristoffer Zetterstrand", (4, 4)),
    "PIGSCENE": PaintingInfo("""pigscene""", "Pigscene", """A girl pointing to a pig on a canvas. In the original painting, the canvas shows red, green and blue blocks, representing the three colors of the RGB color model that is typically used by computer displays. This painting is based on the painting The Artist’s Studio by Jacob van Oost.""", "Kristoffer Zetterstrand", (4, 4)),
    "BURNING_SKULL": PaintingInfo("""burning_skull""", "Skull On Fire", """A skull on fire; in the background, there is a moon in a clear night sky. This painting is based on a Minecraft screenshot,.""", "Kristoffer Zetterstrand", (4, 4)),
    "ORB": PaintingInfo("""orb""", "Orb", """An orb of light in the middle of an Italian landscape at night. This painting is based on the painting St. Francis in Ecstasy by Giovanni Bellini.""", "Kristoffer Zetterstrand", (4, 4)),
    "UNPACKED": PaintingInfo("""unpacked""", "Unpacked", """A Minecraft landscape, showing a cliff with a waterfall and a pig floating in water. This painting is based on pack.png.""", "Sarah Boeving", (4, 4)),
    "EARTH": PaintingInfo("""earth""", "Earth", """One of the four classical elements: Earth.""", "Mojang(Unknown Artist)", (2, 2)),
    "WIND": PaintingInfo("""wind""", "Wind", """One of the four classical elements: Air.""", "Mojang(Unknown Artist)", (2, 2)),
    "FIRE": PaintingInfo("""fire""", "Fire", """One of the four classical elements: Fire.""", "Mojang(Unknown Artist)", (2, 2)),
    "WATER": PaintingInfo("""water""", "Water", """One of the four classical elements: Water.""", "Mojang(Unknown Artist)", (2, 2)),
}

for __k in tuple(paintings.keys()):
    v = paintings[__k]
    paintings[v.name] = v
    paintings[v.value] = v


def as_painting(*values: StrOrArg) -> str | Tuple[str, ...]:
    return _as_things(PAINTING_GROUP, __painting_dups, *values)

