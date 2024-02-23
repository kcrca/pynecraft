from collections import namedtuple

DISPLAY_NAME = "displayName"
COLOR = "color"
FRIENDLY_FIRE = "friendlyFire"
SEE_FRIENDLY_INVISIBLES = "seeFriendlyInvisibles"
NAMETAG_VISIBILITY = "nametagVisibility"
DEATH_MESSAGE_VISIBILITY = "deathMessageVisibility"
COLLISION_RULE = "collisionRule"
PREFIX = "prefix"
SUFFIX = "suffix"
TEAM_OPTIONS_GROUP = [
    DISPLAY_NAME, COLOR, FRIENDLY_FIRE, SEE_FRIENDLY_INVISIBLES, NAMETAG_VISIBILITY, DEATH_MESSAGE_VISIBILITY,
    COLLISION_RULE, PREFIX, SUFFIX
]

TeamOption = namedtuple("Advancement", ['name', 'value', 'desc', 'type'])
team_options = {
    "DISPLAY_NAME": TeamOption("Display Name", "displayName", """Set the display name of the team.""", str),
    "COLOR": TeamOption("Color", "color",
                        """Decide the color of the team and players in chat, above their head, on the Tab menu, and on the sidebar. Also changes the color of the outline of the entities caused by the Glowing effect.""",
                        str),
    "FRIENDLY_FIRE": TeamOption("Friendly Fire", "friendlyFire",
                                """Enable/Disable players inflicting damage on each other when on the same team. (Note": players can still inflict status effects on each other.) Does not affect some non-player entities in a team.""",
                                bool),
    "SEE_FRIENDLY_INVISIBLES": TeamOption("See Friendly Invisibles", "seeFriendlyInvisibles",
                                          """Decide players can see invisible players on their team as whether semi-transparent or completely invisible.""",
                                          bool),
    "NAMETAG_VISIBILITY": TeamOption("Nametag Visibility", "nametagVisibility",
                                     """Decide whose name tags above their heads can be seen.""",
                                     ['never', 'hideForOtherTeams', 'hideForOwnTeam', 'always']),
    "DEATH_MESSAGE_VISIBILITY": TeamOption("Death Message Visibility", "deathMessageVisibility",
                                           """Control the visibility of death messages for players.""",
                                           ['never', 'hideForOtherTeams', 'hideForOwnTeam', 'always']),
    "COLLISION_RULE": TeamOption("Collision Rule", "collisionRule",
                                 """Controls the way the entities on the team collide with other entities.""",
                                 ['never', 'pushOtherTeams', 'pushOwnTeam', 'always']),
    "PREFIX": TeamOption("Prefix", "prefix", """Modifies the prefix that displays before players' names.""", str),
    "SUFFIX": TeamOption("Suffix", "suffix", """Modifies the suffix that displays after players' names.""", str),
}


def team_option_spec(enum):
    return {"displayName": str, "color": str, "friendlyFire": bool, "seeFriendlyInvisibles": bool,
            "nametagVisibility": ['never', 'hideForOtherTeams', 'hideForOwnTeam', 'always'],
            "deathMessageVisibility": ['never', 'hideForOtherTeams', 'hideForOwnTeam', 'always'],
            "collisionRule": ['never', 'pushOtherTeams', 'pushOwnTeam', 'always'], "prefix": str, "suffix": str, }[
        enum.value]


# Generated values:

# Patterns
# Derived from https://minecraft.wiki/Banner/Patterns, 2024-02-22T23:57:45-08:00
BASE = "b"
BOTTOM_STRIPE = "bs"
TOP_STRIPE = "ts"
LEFT_STRIPE = "ls"
RIGHT_STRIPE = "rs"
CENTER_STRIPE_VERTICAL = "cs"
MIDDLE_STRIPE_HORIZONTAL = "ms"
DOWN_RIGHT_STRIPE = "drs"
DOWN_LEFT_STRIPE = "dls"
SMALL_VERTICAL_STRIPES = "ss"
DIAGONAL_CROSS = "cr"
SQUARE_CROSS = "sc"
LEFT_OF_DIAGONAL = "ld"
RIGHT_OF_UPSIDEDOWN_DIAGONAL = "rud"
LEFT_OF_UPSIDEDOWN_DIAGONAL = "lud"
RIGHT_OF_DIAGONAL = "rd"
VERTICAL_HALF_LEFT = "vh"
VERTICAL_HALF_RIGHT = "vhr"
HORIZONTAL_HALF_TOP = "hh"
HORIZONTAL_HALF_BOTTOM = "hhb"
BOTTOM_LEFT_CORNER = "bl"
BOTTOM_RIGHT_CORNER = "br"
TOP_LEFT_CORNER = "tl"
TOP_RIGHT_CORNER = "tr"
BOTTOM_TRIANGLE = "bt"
TOP_TRIANGLE = "tt"
BOTTOM_TRIANGLE_SAWTOOTH = "bts"
TOP_TRIANGLE_SAWTOOTH = "tts"
MIDDLE_CIRCLE = "mc"
MIDDLE_RHOMBUS = "mr"
BORDER = "bo"
CURLY_BORDER = "cbo"
BRICK = "bri"
GRADIENT = "gra"
GRADIENT_UPSIDEDOWN = "gru"
CREEPER = "cre"
SKULL = "sku"
FLOWER = "flo"
MOJANG = "moj"
GLOBE = "glb"
PIGLIN = "pig"
PATTERN_GROUP = [
    BASE, BOTTOM_STRIPE, TOP_STRIPE, LEFT_STRIPE, RIGHT_STRIPE, CENTER_STRIPE_VERTICAL, MIDDLE_STRIPE_HORIZONTAL,
    DOWN_RIGHT_STRIPE, DOWN_LEFT_STRIPE, SMALL_VERTICAL_STRIPES, DIAGONAL_CROSS, SQUARE_CROSS, LEFT_OF_DIAGONAL,
    RIGHT_OF_UPSIDEDOWN_DIAGONAL, LEFT_OF_UPSIDEDOWN_DIAGONAL, RIGHT_OF_DIAGONAL, VERTICAL_HALF_LEFT,
    VERTICAL_HALF_RIGHT, HORIZONTAL_HALF_TOP, HORIZONTAL_HALF_BOTTOM, BOTTOM_LEFT_CORNER, BOTTOM_RIGHT_CORNER,
    TOP_LEFT_CORNER, TOP_RIGHT_CORNER, BOTTOM_TRIANGLE, TOP_TRIANGLE, BOTTOM_TRIANGLE_SAWTOOTH, TOP_TRIANGLE_SAWTOOTH,
    MIDDLE_CIRCLE, MIDDLE_RHOMBUS, BORDER, CURLY_BORDER, BRICK, GRADIENT, GRADIENT_UPSIDEDOWN, CREEPER, SKULL, FLOWER,
    MOJANG, GLOBE, PIGLIN
]

Pattern = namedtuple("Pattern", ['name', 'value', 'desc'])
pattern = {
    "BASE": Pattern("""Base""", "b", """Fully color Field."""),
    "BOTTOM_STRIPE": Pattern("""Bottom Stripe""", "bs", """Base."""),
    "TOP_STRIPE": Pattern("""Top Stripe""", "ts", """Chief."""),
    "LEFT_STRIPE": Pattern("""Left Stripe""", "ls", """Pale Dexter."""),
    "RIGHT_STRIPE": Pattern("""Right Stripe""", "rs", """Pale Sinister."""),
    "CENTER_STRIPE_VERTICAL": Pattern("""Center Stripe (Vertical)""", "cs", """Pale."""),
    "MIDDLE_STRIPE_HORIZONTAL": Pattern("""Middle Stripe (Horizontal)""", "ms", """Fess."""),
    "DOWN_RIGHT_STRIPE": Pattern("""Down Right Stripe""", "drs", """Bend."""),
    "DOWN_LEFT_STRIPE": Pattern("""Down Left Stripe""", "dls", """Bend Sinister."""),
    "SMALL_VERTICAL_STRIPES": Pattern("""Small (Vertical) Stripes""", "ss", """Paly."""),
    "DIAGONAL_CROSS": Pattern("""Diagonal Cross""", "cr", """Saltire."""),
    "SQUARE_CROSS": Pattern("""Square Cross""", "sc", """Cross."""),
    "LEFT_OF_DIAGONAL": Pattern("""Left of Diagonal""", "ld", """Per Bend Sinister."""),
    "RIGHT_OF_UPSIDEDOWN_DIAGONAL": Pattern("""Right of upside-down Diagonal""", "rud", """Per Bend."""),
    "LEFT_OF_UPSIDEDOWN_DIAGONAL": Pattern("""Left of upside-down Diagonal""", "lud", """Per Bend Inverted."""),
    "RIGHT_OF_DIAGONAL": Pattern("""Right of Diagonal""", "rd", """Per Bend Sinister Inverted."""),
    "VERTICAL_HALF_LEFT": Pattern("""Vertical Half (left)""", "vh", """Per Pale."""),
    "VERTICAL_HALF_RIGHT": Pattern("""Vertical Half (right)""", "vhr", """Per Pale Inverted."""),
    "HORIZONTAL_HALF_TOP": Pattern("""Horizontal Half (top)""", "hh", """Per Fess."""),
    "HORIZONTAL_HALF_BOTTOM": Pattern("""Horizontal Half (bottom)""", "hhb", """Per Fess Inverted."""),
    "BOTTOM_LEFT_CORNER": Pattern("""Bottom Left Corner""", "bl", """Base Dexter Canton."""),
    "BOTTOM_RIGHT_CORNER": Pattern("""Bottom Right Corner""", "br", """Base Sinister Canton."""),
    "TOP_LEFT_CORNER": Pattern("""Top Left Corner""", "tl", """Chief Dexter Canton."""),
    "TOP_RIGHT_CORNER": Pattern("""Top Right Corner""", "tr", """Chief Sinister Canton."""),
    "BOTTOM_TRIANGLE": Pattern("""Bottom Triangle""", "bt", """Chevron."""),
    "TOP_TRIANGLE": Pattern("""Top Triangle""", "tt", """Inverted Chevron."""),
    "BOTTOM_TRIANGLE_SAWTOOTH": Pattern("""Bottom Triangle Sawtooth""", "bts", """Base Indented."""),
    "TOP_TRIANGLE_SAWTOOTH": Pattern("""Top Triangle Sawtooth""", "tts", """Chief Indented."""),
    "MIDDLE_CIRCLE": Pattern("""Middle Circle""", "mc", """Roundel."""),
    "MIDDLE_RHOMBUS": Pattern("""Middle Rhombus""", "mr", """Lozenge."""),
    "BORDER": Pattern("""Border""", "bo", """Bordure."""),
    "CURLY_BORDER": Pattern("""Curly Border""", "cbo", """Bordure Indented."""),
    "BRICK": Pattern("""Brick""", "bri", """Field Masoned."""),
    "GRADIENT": Pattern("""Gradient""", "gra", """Gradient."""),
    "GRADIENT_UPSIDEDOWN": Pattern("""Gradient upside-down""", "gru", """Base Gradient."""),
    "CREEPER": Pattern("""Creeper""", "cre", """Creeper Charge."""),
    "SKULL": Pattern("""Skull""", "sku", """Skull Charge."""),
    "FLOWER": Pattern("""Flower""", "flo", """Flower Charge."""),
    "MOJANG": Pattern("""Mojang""", "moj", """Thing."""),
    "GLOBE": Pattern("""Globe""", "glb", """Globe."""),
    "PIGLIN": Pattern("""Piglin""", "pig", """Snout."""),
}

for __k in pattern:
    v = pattern[__k]
    pattern[v.name] = v

# Advancements
# Derived from https://minecraft.wiki/Advancement#List_of_advancements, 2024-02-22T23:57:46-08:00
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
NETHER = "nether/root"
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
COUNTRY_LODE_TAKE_ME_HOME = "nether/use_lodestone"
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
THE_END = "end/root"
FREE_THE_END = "end/kill_dragon"
THE_NEXT_GENERATION = "end/dragon_egg"
REMOTE_GETAWAY = "end/enter_end_gateway"
THE_END_AGAIN = "end/respawn_dragon"
YOU_NEED_A_MINT = "end/dragon_breath"
THE_CITY_AT_THE_END_OF_THE_GAME = "end/find_end_city"
SKYS_THE_LIMIT = "end/elytra"
GREAT_VIEW_FROM_UP_HERE = "end/levitate"
ADVENTURE = "adventure/root"
VOLUNTARY_EXILE = "adventure/voluntary_exile"
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
HUSBANDRY = "husbandry/root"
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
ADVANCEMENT_GROUP = [
    MINECRAFT, STONE_AGE, GETTING_AN_UPGRADE, ACQUIRE_HARDWARE, SUIT_UP, HOT_STUFF, ISNT_IT_IRON_PICK,
    NOT_TODAY_THANK_YOU, ICE_BUCKET_CHALLENGE, DIAMONDS, WE_NEED_TO_GO_DEEPER, COVER_ME_WITH_DIAMONDS, ENCHANTER,
    ZOMBIE_DOCTOR, EYE_SPY, ENTER_THE_END, NETHER, RETURN_TO_SENDER, THOSE_WERE_THE_DAYS, HIDDEN_IN_THE_DEPTHS,
    SUBSPACE_BUBBLE, A_TERRIBLE_FORTRESS, WHO_IS_CUTTING_ONIONS, OH_SHINY, THIS_BOAT_HAS_LEGS, UNEASY_ALLIANCE,
    WAR_PIGS, COUNTRY_LODE_TAKE_ME_HOME, COVER_ME_IN_DEBRIS, SPOOKY_SCARY_SKELETON, INTO_FIRE, NOT_QUITE_NINE_LIVES,
    FEELS_LIKE_HOME, HOT_TOURIST_DESTINATIONS, WITHERING_HEIGHTS, LOCAL_BREWERY, BRING_HOME_THE_BEACON,
    A_FURIOUS_COCKTAIL, BEACONATOR, HOW_DID_WE_GET_HERE, THE_END, FREE_THE_END, THE_NEXT_GENERATION, REMOTE_GETAWAY,
    THE_END_AGAIN, YOU_NEED_A_MINT, THE_CITY_AT_THE_END_OF_THE_GAME, SKYS_THE_LIMIT, GREAT_VIEW_FROM_UP_HERE, ADVENTURE,
    VOLUNTARY_EXILE, IS_IT_A_BIRD, MONSTER_HUNTER, THE_POWER_OF_BOOKS, WHAT_A_DEAL, CRAFTING_A_NEW_LOOK,
    STICKY_SITUATION, OL_BETSY, SURGE_PROTECTOR, CAVES__CLIFFS, RESPECTING_THE_REMNANTS, SNEAK_100, SWEET_DREAMS,
    HERO_OF_THE_VILLAGE, IS_IT_A_BALLOON, A_THROWAWAY_JOKE, IT_SPREADS, TAKE_AIM, MONSTERS_HUNTED, POSTMORTAL,
    HIRED_HELP, STAR_TRADER, SMITHING_WITH_STYLE, TWO_BIRDS_ONE_ARROW, WHOS_THE_PILLAGER_NOW, ARBALISTIC,
    CAREFUL_RESTORATION, ADVENTURING_TIME, SOUND_OF_MUSIC, LIGHT_AS_A_RABBIT, IS_IT_A_PLANE, VERY_VERY_FRIGHTENING,
    SNIPER_DUEL, BULLSEYE, HUSBANDRY, BEE_OUR_GUEST, THE_PARROTS_AND_THE_BATS, YOUVE_GOT_A_FRIEND_IN_ME,
    WHATEVER_FLOATS_YOUR_GOAT, BEST_FRIENDS_FOREVER, GLOW_AND_BEHOLD, FISHY_BUSINESS, TOTAL_BEELOCATION, BUKKIT_BUKKIT,
    SMELLS_INTERESTING, A_SEEDY_PLACE, WAX_ON, TWO_BY_TWO, BIRTHDAY_SONG, A_COMPLETE_CATALOGUE, TACTICAL_FISHING,
    WHEN_THE_SQUAD_HOPS_INTO_TOWN, LITTLE_SNIFFS, A_BALANCED_DIET, SERIOUS_DEDICATION, WAX_OFF, THE_CUTEST_PREDATOR,
    WITH_OUR_POWERS_COMBINED, PLANTING_THE_PAST, THE_HEALING_POWER_OF_FRIENDSHIP
]

Advancement = namedtuple("Advancement", ['name', 'value', 'desc'])
advancement = {
    "MINECRAFT": Advancement("""Minecraft""", "story/root", """The heart and story of the game."""),
    "STONE_AGE": Advancement("""Stone Age""", "story/mine_stone", """Mine Stone with your new Pickaxe."""),
    "GETTING_AN_UPGRADE": Advancement("""Getting an Upgrade""", "story/upgrade_tools",
                                      """Construct a better Pickaxe."""),
    "ACQUIRE_HARDWARE": Advancement("""Acquire Hardware""", "story/smelt_iron", """Smelt an Iron Ingot."""),
    "SUIT_UP": Advancement("""Suit Up""", "story/obtain_armor", """Protect yourself with a piece of iron armor."""),
    "HOT_STUFF": Advancement("""Hot Stuff""", "story/lava_bucket", """Fill a Bucket with lava."""),
    "ISNT_IT_IRON_PICK": Advancement("""Isn't It Iron Pick""", "story/iron_tools", """Upgrade your Pickaxe."""),
    "NOT_TODAY_THANK_YOU": Advancement("""Not Today, Thank You""", "story/deflect_arrow",
                                       """Deflect a projectile with a Shield."""),
    "ICE_BUCKET_CHALLENGE": Advancement("""Ice Bucket Challenge""", "story/form_obsidian",
                                        """Obtain a block of Obsidian."""),
    "DIAMONDS": Advancement("""Diamonds!""", "story/mine_diamond", """Acquire diamonds."""),
    "WE_NEED_TO_GO_DEEPER": Advancement("""We Need to Go Deeper""", "story/enter_the_nether",
                                        """Build, light and enter a Nether Portal."""),
    "COVER_ME_WITH_DIAMONDS": Advancement("""Cover Me with Diamonds""", "story/shiny_gear",
                                          """Diamond armor saves lives."""),
    "ENCHANTER": Advancement("""Enchanter""", "story/enchant_item", """Enchant an item at an Enchanting Table."""),
    "ZOMBIE_DOCTOR": Advancement("""Zombie Doctor""", "story/cure_zombie_villager",
                                 """Weaken and then cure a Zombie Villager."""),
    "EYE_SPY": Advancement("""Eye Spy""", "story/follow_ender_eye", """Follow an Eye of Ender."""),
    "ENTER_THE_END": Advancement("""The End?""", "story/enter_the_end", """Enter the End Portal."""),
    "NETHER": Advancement("""Nether""", "nether/root", """Bring summer clothes."""),
    "RETURN_TO_SENDER": Advancement("""Return to Sender""", "nether/return_to_sender",
                                    """Destroy a Ghast with a fireball."""),
    "THOSE_WERE_THE_DAYS": Advancement("""Those Were the Days""", "nether/find_bastion",
                                       """Enter a Bastion Remnant."""),
    "HIDDEN_IN_THE_DEPTHS": Advancement("""Hidden in the Depths""", "nether/obtain_ancient_debris",
                                        """Obtain Ancient Debris."""),
    "SUBSPACE_BUBBLE": Advancement("""Subspace Bubble""", "nether/fast_travel",
                                   """Use the Nether to travel 7 km in the Overworld."""),
    "A_TERRIBLE_FORTRESS": Advancement("""A Terrible Fortress""", "nether/find_fortress",
                                       """Break your way into a Nether Fortress."""),
    "WHO_IS_CUTTING_ONIONS": Advancement("""Who is Cutting Onions?""", "nether/obtain_crying_obsidian",
                                         """Obtain Crying Obsidian."""),
    "OH_SHINY": Advancement("""Oh Shiny""", "nether/distract_piglin", """Distract Piglins with gold."""),
    "THIS_BOAT_HAS_LEGS": Advancement("""This Boat Has Legs""", "nether/ride_strider",
                                      """Ride a Strider with a Warped Fungus on a Stick."""),
    "UNEASY_ALLIANCE": Advancement("""Uneasy Alliance""", "nether/uneasy_alliance",
                                   """Rescue a Ghast from the Nether, bring it safely home to the Overworld... and then kill it."""),
    "WAR_PIGS": Advancement("""War Pigs""", "nether/loot_bastion", """Loot a Chest in a Bastion Remnant."""),
    "COUNTRY_LODE_TAKE_ME_HOME": Advancement("""Country Lode, Take Me Home""", "nether/use_lodestone",
                                             """Use a Compass on a Lodestone."""),
    "COVER_ME_IN_DEBRIS": Advancement("""Cover Me in Debris""", "nether/netherite_armor",
                                      """Get a full suit of Netherite armor."""),
    "SPOOKY_SCARY_SKELETON": Advancement("""Spooky Scary Skeleton""", "nether/get_wither_skull",
                                         """Obtain a Wither Skeleton's skull."""),
    "INTO_FIRE": Advancement("""Into Fire""", "nether/obtain_blaze_rod", """Relieve a Blaze of its rod."""),
    "NOT_QUITE_NINE_LIVES": Advancement("""Not Quite "Nine" Lives""", "nether/charge_respawn_anchor",
                                        """Charge a Respawn Anchor to the maximum."""),
    "FEELS_LIKE_HOME": Advancement("""Feels Like Home""", "nether/ride_strider_in_overworld_lava",
                                   """Take a Strider for a loooong ride on a lava lake in the Overworld."""),
    "HOT_TOURIST_DESTINATIONS": Advancement("""Hot Tourist Destinations""", "nether/explore_nether",
                                            """Explore all Nether biomes."""),
    "WITHERING_HEIGHTS": Advancement("""Withering Heights""", "nether/summon_wither", """Summon the Wither."""),
    "LOCAL_BREWERY": Advancement("""Local Brewery""", "nether/brew_potion", """Brew a Potion."""),
    "BRING_HOME_THE_BEACON": Advancement("""Bring Home the Beacon""", "nether/create_beacon",
                                         """Construct and place a Beacon."""),
    "A_FURIOUS_COCKTAIL": Advancement("""A Furious Cocktail""", "nether/all_potions",
                                      """Have every potion effect applied at the same time."""),
    "BEACONATOR": Advancement("""Beaconator""", "nether/create_full_beacon", """Bring a Beacon to full power."""),
    "HOW_DID_WE_GET_HERE": Advancement("""How Did We Get Here?""", "nether/all_effects",
                                       """Have every effect applied at the same time."""),
    "THE_END": Advancement("""The End""", "end/root", """Or the beginning?"""),
    "FREE_THE_END": Advancement("""Free the End""", "end/kill_dragon", """Good luck."""),
    "THE_NEXT_GENERATION": Advancement("""The Next Generation""", "end/dragon_egg", """Hold the Dragon Egg."""),
    "REMOTE_GETAWAY": Advancement("""Remote Getaway""", "end/enter_end_gateway", """Escape the island."""),
    "THE_END_AGAIN": Advancement("""The End... Again...""", "end/respawn_dragon", """Respawn the Ender Dragon."""),
    "YOU_NEED_A_MINT": Advancement("""You Need a Mint""", "end/dragon_breath",
                                   """Collect Dragon's Breath in a Glass Bottle."""),
    "THE_CITY_AT_THE_END_OF_THE_GAME": Advancement("""The City at the End of the Game""", "end/find_end_city",
                                                   """Go on in, what could happen?"""),
    "SKYS_THE_LIMIT": Advancement("""Sky's the Limit""", "end/elytra", """Find Elytra."""),
    "GREAT_VIEW_FROM_UP_HERE": Advancement("""Great View From Up Here""", "end/levitate",
                                           """Levitate up 50 blocks from the attacks of a Shulker."""),
    "ADVENTURE": Advancement("""Adventure""", "adventure/root", """Adventure, exploration and combat."""),
    "VOLUNTARY_EXILE": Advancement("""Voluntary Exile""", "adventure/voluntary_exile",
                                   """Kill a raid captain.Maybe consider staying away from villages for the time being..."""),
    "IS_IT_A_BIRD": Advancement("""Is It a Bird?""", "adventure/spyglass_at_parrot",
                                """Look at a Parrot through a Spyglass."""),
    "MONSTER_HUNTER": Advancement("""Monster Hunter""", "adventure/kill_a_mob", """Kill any hostile monster."""),
    "THE_POWER_OF_BOOKS": Advancement("""The Power of Books""", "adventure/read_power_of_chiseled_bookshelf",
                                      """Read the power signal of a Chiseled Bookshelf using a Comparator."""),
    "WHAT_A_DEAL": Advancement("""What a Deal!""", "adventure/trade", """Successfully trade with a Villager."""),
    "CRAFTING_A_NEW_LOOK": Advancement("""Crafting a New Look""", "adventure/trim_with_any_armor_pattern",
                                       """Craft a trimmed armor at a Smithing Table."""),
    "STICKY_SITUATION": Advancement("""Sticky Situation""", "adventure/honey_block_slide",
                                    """Jump into a Honey Block to break your fall."""),
    "OL_BETSY": Advancement("""Ol' Betsy""", "adventure/ol_betsy", """Shoot a Crossbow."""),
    "SURGE_PROTECTOR": Advancement("""Surge Protector""", "adventure/lightning_rod_with_villager_no_fire",
                                   """Protect a Villager from an undesired shock without starting a fire."""),
    "CAVES__CLIFFS": Advancement("""Caves & Cliffs""", "adventure/fall_from_world_height",
                                 """Free fall from the top of the world (build limit) to the bottom of the world and survive."""),
    "RESPECTING_THE_REMNANTS": Advancement("""Respecting the Remnants""", "adventure/salvage_sherd",
                                           """Brush a Suspicious block to obtain a Pottery Sherd."""),
    "SNEAK_100": Advancement("""Sneak 100""", "adventure/avoid_vibration",
                             """Sneak near a Sculk Sensor or Warden to prevent it from detecting you."""),
    "SWEET_DREAMS": Advancement("""Sweet Dreams""", "adventure/sleep_in_bed",
                                """Sleep in a Bed to change your respawn point."""),
    "HERO_OF_THE_VILLAGE": Advancement("""Hero of the Village""", "adventure/hero_of_the_village",
                                       """Successfully defend a village from a raid."""),
    "IS_IT_A_BALLOON": Advancement("""Is It a Balloon?""", "adventure/spyglass_at_ghast",
                                   """Look at a Ghast through a Spyglass."""),
    "A_THROWAWAY_JOKE": Advancement("""A Throwaway Joke""", "adventure/throw_trident",
                                    """Throw a Trident at something.Note: Throwing away your only weapon is not a good idea."""),
    "IT_SPREADS": Advancement("""It Spreads""", "adventure/kill_mob_near_sculk_catalyst",
                              """Kill a mob near a Sculk Catalyst."""),
    "TAKE_AIM": Advancement("""Take Aim""", "adventure/shoot_arrow", """Shoot something with an Arrow."""),
    "MONSTERS_HUNTED": Advancement("""Monsters Hunted""", "adventure/kill_all_mobs",
                                   """Kill one of every hostile monster."""),
    "POSTMORTAL": Advancement("""Postmortal""", "adventure/totem_of_undying",
                              """Use a Totem of Undying to cheat death."""),
    "HIRED_HELP": Advancement("""Hired Help""", "adventure/summon_iron_golem",
                              """Summon an Iron Golem to help defend a village."""),
    "STAR_TRADER": Advancement("""Star Trader""", "adventure/trade_at_world_height",
                               """Trade with a Villager at the build height limit."""),
    "SMITHING_WITH_STYLE": Advancement("""Smithing with Style""", "adventure/trim_with_all_exclusive_armor_patterns",
                                       """Apply these smithing templates at least once: Spire, Snout, Rib, Ward, Silence, Vex, Tide, Wayfinder."""),
    "TWO_BIRDS_ONE_ARROW": Advancement("""Two Birds, One Arrow""", "adventure/two_birds_one_arrow",
                                       """Kill two Phantoms with a piercing Arrow."""),
    "WHOS_THE_PILLAGER_NOW": Advancement("""Who's the Pillager Now?""", "adventure/whos_the_pillager_now",
                                         """Give a Pillager a taste of their own medicine."""),
    "ARBALISTIC": Advancement("""Arbalistic""", "adventure/arbalistic",
                              """Kill five unique mobs with one crossbow shot."""),
    "CAREFUL_RESTORATION": Advancement("""Careful Restoration""", "adventure/craft_decorated_pot_using_only_sherds",
                                       """Make a Decorated Pot out of 4 Pottery Sherds."""),
    "ADVENTURING_TIME": Advancement("""Adventuring Time""", "adventure/adventuring_time", """Discover every biome."""),
    "SOUND_OF_MUSIC": Advancement("""Sound of Music""", "adventure/play_jukebox_in_meadows",
                                  """Make the Meadows come alive with the sound of music from a Jukebox."""),
    "LIGHT_AS_A_RABBIT": Advancement("""Light as a Rabbit""", "adventure/walk_on_powder_snow_with_leather_boots",
                                     """Walk on Powder Snow... without sinking in it."""),
    "IS_IT_A_PLANE": Advancement("""Is It a Plane?""", "adventure/spyglass_at_dragon",
                                 """Look at the Ender Dragon through a Spyglass."""),
    "VERY_VERY_FRIGHTENING": Advancement("""Very Very Frightening""", "adventure/very_very_frightening",
                                         """Strike a Villager with lightning."""),
    "SNIPER_DUEL": Advancement("""Sniper Duel""", "adventure/sniper_duel",
                               """Kill a Skeleton from at least 50 meters away."""),
    "BULLSEYE": Advancement("""Bullseye""", "adventure/bullseye",
                            """Hit the bullseye of a Target block from at least 30 meters away."""),
    "HUSBANDRY": Advancement("""Husbandry""", "husbandry/root", """The world is full of friends and food."""),
    "BEE_OUR_GUEST": Advancement("""Bee Our Guest""", "husbandry/safely_harvest_honey",
                                 """Use a Campfire to collect Honey from a Beehive using a Glass Bottle without aggravating the Bees."""),
    "THE_PARROTS_AND_THE_BATS": Advancement("""The Parrots and the Bats""", "husbandry/breed_an_animal",
                                            """Breed two animals together."""),
    "YOUVE_GOT_A_FRIEND_IN_ME": Advancement("""You've Got a Friend in Me""", "husbandry/allay_deliver_item_to_player",
                                            """Have an Allay deliver items to you."""),
    "WHATEVER_FLOATS_YOUR_GOAT": Advancement("""Whatever Floats Your Goat!""", "husbandry/ride_a_boat_with_a_goat",
                                             """Get in a Boat and float with a Goat."""),
    "BEST_FRIENDS_FOREVER": Advancement("""Best Friends Forever""", "husbandry/tame_an_animal", """Tame an animal."""),
    "GLOW_AND_BEHOLD": Advancement("""Glow and Behold!""", "husbandry/make_a_sign_glow",
                                   """Make the text of any kind of sign glow."""),
    "FISHY_BUSINESS": Advancement("""Fishy Business""", "husbandry/fishy_business", """Catch a fish."""),
    "TOTAL_BEELOCATION": Advancement("""Total Beelocation""", "husbandry/silk_touch_nest",
                                     """Move a Bee Nest, with 3 Bees inside, using Silk Touch."""),
    "BUKKIT_BUKKIT": Advancement("""Bukkit Bukkit""", "husbandry/tadpole_in_a_bucket",
                                 """Catch a Tadpole in a Bucket."""),
    "SMELLS_INTERESTING": Advancement("""Smells Interesting""", "husbandry/obtain_sniffer_egg",
                                      """Obtain a Sniffer Egg."""),
    "A_SEEDY_PLACE": Advancement("""A Seedy Place""", "husbandry/plant_seed", """Plant a seed and watch it grow."""),
    "WAX_ON": Advancement("""Wax On""", "husbandry/wax_on", """Apply Honeycomb to a Copper block!"""),
    "TWO_BY_TWO": Advancement("""Two by Two""", "husbandry/bred_all_animals", """Breed all the animals!"""),
    "BIRTHDAY_SONG": Advancement("""Birthday Song""", "husbandry/allay_deliver_cake_to_note_block",
                                 """Have an Allay drop a Cake at a Note Block."""),
    "A_COMPLETE_CATALOGUE": Advancement("""A Complete Catalogue""", "husbandry/complete_catalogue",
                                        """Tame all Cat variants!"""),
    "TACTICAL_FISHING": Advancement("""Tactical Fishing""", "husbandry/tactical_fishing",
                                    """Catch a Fish... without a Fishing Rod!"""),
    "WHEN_THE_SQUAD_HOPS_INTO_TOWN": Advancement("""When the Squad Hops into Town""",
                                                 "husbandry/leash_all_frog_variants",
                                                 """Get each Frog variant on a Lead."""),
    "LITTLE_SNIFFS": Advancement("""Little Sniffs""", "husbandry/feed_snifflet", """Feed a Snifflet."""),
    "A_BALANCED_DIET": Advancement("""A Balanced Diet""", "husbandry/balanced_diet",
                                   """Eat everything that is edible, even if it's not good for you."""),
    "SERIOUS_DEDICATION": Advancement("""Serious Dedication""", "husbandry/obtain_netherite_hoe",
                                      """Use a Netherite Ingot to upgrade a Hoe, and then reevaluate your life choices."""),
    "WAX_OFF": Advancement("""Wax Off""", "husbandry/wax_off", """Scrape Wax off of a Copper block!"""),
    "THE_CUTEST_PREDATOR": Advancement("""The Cutest Predator""", "husbandry/axolotl_in_a_bucket",
                                       """Catch an Axolotl in a Bucket."""),
    "WITH_OUR_POWERS_COMBINED": Advancement("""With Our Powers Combined!""", "husbandry/froglights",
                                            """Have all Froglights in your inventory."""),
    "PLANTING_THE_PAST": Advancement("""Planting the Past""", "husbandry/plant_any_sniffer_seed",
                                     """Plant any Sniffer seed."""),
    "THE_HEALING_POWER_OF_FRIENDSHIP": Advancement("""The Healing Power of Friendship!""",
                                                   "husbandry/kill_axolotl_target",
                                                   """Team up with an axolotl and win a fight."""),
}

for __k in advancement:
    v = advancement[__k]
    advancement[v.name] = v

# BiomeIds
# Derived from https://minecraft.wiki/Biome/ID, 2024-02-22T23:57:46-08:00
THE_VOID = "the_void"
PLAINS = "plains"
SUNFLOWER_PLAINS = "sunflower_plains"
SNOWY_PLAINS = "snowy_plains"
ICE_SPIKES = "ice_spikes"
DESERT = "desert"
SWAMP = "swamp"
MANGROVE_SWAMP = "mangrove_swamp"
FOREST = "forest"
FLOWER_FOREST = "flower_forest"
BIRCH_FOREST = "birch_forest"
DARK_FOREST = "dark_forest"
OLD_GROWTH_BIRCH_FOREST = "old_growth_birch_forest"
OLD_GROWTH_PINE_TAIGA = "old_growth_pine_taiga"
OLD_GROWTH_SPRUCE_TAIGA = "old_growth_spruce_taiga"
TAIGA = "taiga"
SNOWY_TAIGA = "snowy_taiga"
SAVANNA = "savanna"
SAVANNA_PLATEAU = "savanna_plateau"
WINDSWEPT_HILLS = "windswept_hills"
WINDSWEPT_GRAVELLY_HILLS = "windswept_gravelly_hills"
WINDSWEPT_FOREST = "windswept_forest"
WINDSWEPT_SAVANNA = "windswept_savanna"
JUNGLE = "jungle"
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
THE_END = "the_end"
END_HIGHLANDS = "end_highlands"
END_MIDLANDS = "end_midlands"
SMALL_END_ISLANDS = "small_end_islands"
END_BARRENS = "end_barrens"
BIOMEID_GROUP = [
    THE_VOID, PLAINS, SUNFLOWER_PLAINS, SNOWY_PLAINS, ICE_SPIKES, DESERT, SWAMP, MANGROVE_SWAMP, FOREST, FLOWER_FOREST,
    BIRCH_FOREST, DARK_FOREST, OLD_GROWTH_BIRCH_FOREST, OLD_GROWTH_PINE_TAIGA, OLD_GROWTH_SPRUCE_TAIGA, TAIGA,
    SNOWY_TAIGA, SAVANNA, SAVANNA_PLATEAU, WINDSWEPT_HILLS, WINDSWEPT_GRAVELLY_HILLS, WINDSWEPT_FOREST,
    WINDSWEPT_SAVANNA, JUNGLE, SPARSE_JUNGLE, BAMBOO_JUNGLE, BADLANDS, ERODED_BADLANDS, WOODED_BADLANDS, MEADOW,
    CHERRY_GROVE, GROVE, SNOWY_SLOPES, FROZEN_PEAKS, JAGGED_PEAKS, STONY_PEAKS, RIVER, FROZEN_RIVER, BEACH, SNOWY_BEACH,
    STONY_SHORE, WARM_OCEAN, LUKEWARM_OCEAN, DEEP_LUKEWARM_OCEAN, OCEAN, DEEP_OCEAN, COLD_OCEAN, DEEP_COLD_OCEAN,
    FROZEN_OCEAN, DEEP_FROZEN_OCEAN, MUSHROOM_FIELDS, DRIPSTONE_CAVES, LUSH_CAVES, DEEP_DARK, NETHER_WASTES,
    WARPED_FOREST, CRIMSON_FOREST, SOUL_SAND_VALLEY, BASALT_DELTAS, THE_END, END_HIGHLANDS, END_MIDLANDS,
    SMALL_END_ISLANDS, END_BARRENS
]

BiomeId = namedtuple("BiomeId", ['name', 'value', 'desc'])
biomeid = {
    "THE_VOID": BiomeId("""The Void""", "the_void", """The Void."""),
    "PLAINS": BiomeId("""Plains""", "plains", """Plains."""),
    "SUNFLOWER_PLAINS": BiomeId("""Sunflower Plains""", "sunflower_plains", """Sunflower Plains."""),
    "SNOWY_PLAINS": BiomeId("""Snowy Plains""", "snowy_plains", """Snowy Plains."""),
    "ICE_SPIKES": BiomeId("""Ice Spikes""", "ice_spikes", """Ice Spikes."""),
    "DESERT": BiomeId("""Desert""", "desert", """Desert."""),
    "SWAMP": BiomeId("""Swamp""", "swamp", """Swamp."""),
    "MANGROVE_SWAMP": BiomeId("""Mangrove Swamp""", "mangrove_swamp", """Mangrove Swamp."""),
    "FOREST": BiomeId("""Forest""", "forest", """Forest."""),
    "FLOWER_FOREST": BiomeId("""Flower Forest""", "flower_forest", """Flower Forest."""),
    "BIRCH_FOREST": BiomeId("""Birch Forest""", "birch_forest", """Birch Forest."""),
    "DARK_FOREST": BiomeId("""Dark Forest""", "dark_forest", """Dark Forest."""),
    "OLD_GROWTH_BIRCH_FOREST": BiomeId("""Old Growth Birch Forest""", "old_growth_birch_forest",
                                       """Old Growth Birch Forest."""),
    "OLD_GROWTH_PINE_TAIGA": BiomeId("""Old Growth Pine Taiga""", "old_growth_pine_taiga",
                                     """Old Growth Pine Taiga."""),
    "OLD_GROWTH_SPRUCE_TAIGA": BiomeId("""Old Growth Spruce Taiga""", "old_growth_spruce_taiga",
                                       """Old Growth Spruce Taiga."""),
    "TAIGA": BiomeId("""Taiga""", "taiga", """Taiga."""),
    "SNOWY_TAIGA": BiomeId("""Snowy Taiga""", "snowy_taiga", """Snowy Taiga."""),
    "SAVANNA": BiomeId("""Savanna""", "savanna", """Savanna."""),
    "SAVANNA_PLATEAU": BiomeId("""Savanna Plateau""", "savanna_plateau", """Savanna Plateau."""),
    "WINDSWEPT_HILLS": BiomeId("""Windswept Hills""", "windswept_hills", """Windswept Hills."""),
    "WINDSWEPT_GRAVELLY_HILLS": BiomeId("""Windswept Gravelly Hills""", "windswept_gravelly_hills",
                                        """Windswept Gravelly Hills."""),
    "WINDSWEPT_FOREST": BiomeId("""Windswept Forest""", "windswept_forest", """Windswept Forest."""),
    "WINDSWEPT_SAVANNA": BiomeId("""Windswept Savanna""", "windswept_savanna", """Windswept Savanna."""),
    "JUNGLE": BiomeId("""Jungle""", "jungle", """Jungle."""),
    "SPARSE_JUNGLE": BiomeId("""Sparse Jungle""", "sparse_jungle", """Sparse Jungle."""),
    "BAMBOO_JUNGLE": BiomeId("""Bamboo Jungle""", "bamboo_jungle", """Bamboo Jungle."""),
    "BADLANDS": BiomeId("""Badlands""", "badlands", """Badlands."""),
    "ERODED_BADLANDS": BiomeId("""Eroded Badlands""", "eroded_badlands", """Eroded Badlands."""),
    "WOODED_BADLANDS": BiomeId("""Wooded Badlands""", "wooded_badlands", """Wooded Badlands."""),
    "MEADOW": BiomeId("""Meadow""", "meadow", """Meadow."""),
    "CHERRY_GROVE": BiomeId("""Cherry Grove""", "cherry_grove", """Cherry Grove."""),
    "GROVE": BiomeId("""Grove""", "grove", """Grove."""),
    "SNOWY_SLOPES": BiomeId("""Snowy Slopes""", "snowy_slopes", """Snowy Slopes."""),
    "FROZEN_PEAKS": BiomeId("""Frozen Peaks""", "frozen_peaks", """Frozen Peaks."""),
    "JAGGED_PEAKS": BiomeId("""Jagged Peaks""", "jagged_peaks", """Jagged Peaks."""),
    "STONY_PEAKS": BiomeId("""Stony Peaks""", "stony_peaks", """Stony Peaks."""),
    "RIVER": BiomeId("""River""", "river", """River."""),
    "FROZEN_RIVER": BiomeId("""Frozen River""", "frozen_river", """Frozen River."""),
    "BEACH": BiomeId("""Beach""", "beach", """Beach."""),
    "SNOWY_BEACH": BiomeId("""Snowy Beach""", "snowy_beach", """Snowy Beach."""),
    "STONY_SHORE": BiomeId("""Stony Shore""", "stony_shore", """Stony Shore."""),
    "WARM_OCEAN": BiomeId("""Warm Ocean""", "warm_ocean", """Warm Ocean."""),
    "LUKEWARM_OCEAN": BiomeId("""Lukewarm Ocean""", "lukewarm_ocean", """Lukewarm Ocean."""),
    "DEEP_LUKEWARM_OCEAN": BiomeId("""Deep Lukewarm Ocean""", "deep_lukewarm_ocean", """Deep Lukewarm Ocean."""),
    "OCEAN": BiomeId("""Ocean""", "ocean", """Ocean."""),
    "DEEP_OCEAN": BiomeId("""Deep Ocean""", "deep_ocean", """Deep Ocean."""),
    "COLD_OCEAN": BiomeId("""Cold Ocean""", "cold_ocean", """Cold Ocean."""),
    "DEEP_COLD_OCEAN": BiomeId("""Deep Cold Ocean""", "deep_cold_ocean", """Deep Cold Ocean."""),
    "FROZEN_OCEAN": BiomeId("""Frozen Ocean""", "frozen_ocean", """Frozen Ocean."""),
    "DEEP_FROZEN_OCEAN": BiomeId("""Deep Frozen Ocean""", "deep_frozen_ocean", """Deep Frozen Ocean."""),
    "MUSHROOM_FIELDS": BiomeId("""Mushroom Fields""", "mushroom_fields", """Mushroom Fields."""),
    "DRIPSTONE_CAVES": BiomeId("""Dripstone Caves""", "dripstone_caves", """Dripstone Caves."""),
    "LUSH_CAVES": BiomeId("""Lush Caves""", "lush_caves", """Lush Caves."""),
    "DEEP_DARK": BiomeId("""Deep Dark""", "deep_dark", """Deep Dark."""),
    "NETHER_WASTES": BiomeId("""Nether Wastes""", "nether_wastes", """Nether Wastes."""),
    "WARPED_FOREST": BiomeId("""Warped Forest""", "warped_forest", """Warped Forest."""),
    "CRIMSON_FOREST": BiomeId("""Crimson Forest""", "crimson_forest", """Crimson Forest."""),
    "SOUL_SAND_VALLEY": BiomeId("""Soul Sand Valley""", "soul_sand_valley", """Soul Sand Valley."""),
    "BASALT_DELTAS": BiomeId("""Basalt Deltas""", "basalt_deltas", """Basalt Deltas."""),
    "THE_END": BiomeId("""The End""", "the_end", """The End."""),
    "END_HIGHLANDS": BiomeId("""End Highlands""", "end_highlands", """End Highlands."""),
    "END_MIDLANDS": BiomeId("""End Midlands""", "end_midlands", """End Midlands."""),
    "SMALL_END_ISLANDS": BiomeId("""Small End Islands""", "small_end_islands", """Small End Islands."""),
    "END_BARRENS": BiomeId("""End Barrens""", "end_barrens", """End Barrens."""),
}

for __k in biomeid:
    v = biomeid[__k]
    biomeid[v.name] = v

# Effects
# Derived from https://minecraft.wiki/Effect?so=search#Effect_list, 2024-02-22T23:57:46-08:00
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
HERO_OF_THE_VILLAGE = "hero_of_the_village"
DARKNESS = "darkness"
EFFECT_GROUP = [
    SPEED, SLOWNESS, HASTE, MINING_FATIGUE, STRENGTH, INSTANT_HEALTH, INSTANT_DAMAGE, JUMP_BOOST, NAUSEA, REGENERATION,
    RESISTANCE, FIRE_RESISTANCE, WATER_BREATHING, INVISIBILITY, BLINDNESS, NIGHT_VISION, HUNGER, WEAKNESS, POISON,
    WITHER, HEALTH_BOOST, ABSORPTION, SATURATION, GLOWING, LEVITATION, LUCK, BAD_LUCK, SLOW_FALLING, CONDUIT_POWER,
    DOLPHINS_GRACE, BAD_OMEN, HERO_OF_THE_VILLAGE, DARKNESS
]

Effect = namedtuple("Effect", ['name', 'value', 'desc', 'positive', 'id'])
effect = {
    "SPEED": Effect("""Speed""", "speed",
                    """Increases walking speed; higher levels make the affected entity faster and increases the player's field of view when affected.""",
                    "True", "1"),
    "SLOWNESS": Effect("""Slowness""", "slowness",
                       """Decreases walking speed; higher levels make the affected entity slower and decreases the player's field of view when affected.""",
                       "False", "2"),
    "HASTE": Effect("""Haste""", "haste",
                    """Increases mining and attack speed, higher levels increase the player's mining and attack speed.""",
                    "True", "3"),
    "MINING_FATIGUE": Effect("""Mining Fatigue""", "mining_fatigue",
                             """Decreases mining and attack speed, higher levels decrease the player's mining and attack speed.""",
                             "False", "4"),
    "STRENGTH": Effect("""Strength""", "strength",
                       """Increases melee damage, higher levels make the affected entity do more melee damage.""",
                       "True", "5"),
    "INSTANT_HEALTH": Effect("""Instant Health""", "instant_health",
                             """Heals living entities, damages undead, higher levels heal more health and do more damage.""",
                             "True", "6"),
    "INSTANT_DAMAGE": Effect("""Instant Damage""", "instant_damage",
                             """Damages living entities, heals undead, higher levels do more damage and heal more health.""",
                             "False", "7"),
    "JUMP_BOOST": Effect("""Jump Boost""", "jump_boost",
                         """Increases jump height and reduces fall damage, higher levels make the affected entity jump higher and reduces more fall damage.""",
                         "True", "8"),
    "NAUSEA": Effect("""Nausea""", "nausea", """Wobbles and warps the screen.""", "False", "9"),
    "REGENERATION": Effect("""Regeneration""", "regeneration",
                           """Regenerates health over time, higher levels make health regenerate quicker.""", "True",
                           "10"),
    "RESISTANCE": Effect("""Resistance""", "resistance", """Reduces damage, higher levels reduce more damage.""",
                         "True", "11"),
    "FIRE_RESISTANCE": Effect("""Fire Resistance""", "fire_resistance",
                              """Prevents the affected entity from taking damage due to Fire, lava and other sources of fire damage.""",
                              "True", "12"),
    "WATER_BREATHING": Effect("""Water Breathing""", "water_breathing",
                              """Prevents drowning and lets the affected entity breathe underwater.""", "True", "13"),
    "INVISIBILITY": Effect("""Invisibility""", "invisibility",
                           """Grants invisibility, making the affected entity invisible (but not the item they hold or the armor they wear), and reduces other mobs' detection range for the affected entity, higher levels reduce other mobs' detection range more.""",
                           "True", "14"),
    "BLINDNESS": Effect("""Blindness""", "blindness",
                        """Impairs vision and disables the ability to sprint and critical hit.""", "False", "15"),
    "NIGHT_VISION": Effect("""Night Vision""", "night_vision",
                           """Lets the player see well in darkness and underwater.""", "True", "16"),
    "HUNGER": Effect("""Hunger""", "hunger",
                     """Increases food exhaustion, higher levels cause the player to starve quicker.""", "False", "17"),
    "WEAKNESS": Effect("""Weakness""", "weakness",
                       """Decreases melee damage, higher levels decrease more melee damage.""", "False", "18"),
    "POISON": Effect("""Poison""", "poison",
                     """Inflicts damage over time (but can't kill), higher levels do more damage per second, doesn't affect undead.""",
                     "False", "19"),
    "WITHER": Effect("""Wither""", "wither",
                     """Inflicts damage over time (can kill), higher levels do more damage per second.""", "False",
                     "20"),
    "HEALTH_BOOST": Effect("""Health Boost""", "health_boost",
                           """Increases maximum health, higher levels give the affected entity more maximum health.""",
                           "True", "21"),
    "ABSORPTION": Effect("""Absorption""", "absorption",
                         """Adds damage absorption (additional hearts that can't be regenerated), higher levels give more absorption.""",
                         "True", "22"),
    "SATURATION": Effect("""Saturation""", "saturation", """Restores hunger and saturation.""", "True", "23"),
    "GLOWING": Effect("""Glowing""", "glowing", """Outlines the affected entity (can be seen through blocks).""",
                      "None", "24"),
    "LEVITATION": Effect("""Levitation""", "levitation", """Floats the affected entity upward.""", "None", "25"),
    "LUCK": Effect("""Luck""", "luck",
                   """Can increase chances of high-quality and more loot, higher levels increase the chances of better loot.""",
                   "True", "26"),
    "BAD_LUCK": Effect("""Bad Luck""", "unluck",
                       """Can reduce chances of high-quality and more loot, higher levels reduce the chance of good loot.""",
                       "False", "27"),
    "SLOW_FALLING": Effect("""Slow Falling""", "slow_falling", """Decreases falling speed and negates fall damage.""",
                           "True", "28"),
    "CONDUIT_POWER": Effect("""Conduit Power""", "conduit_power",
                            """Increases underwater visibility and mining speed, prevents drowning.""", "True", "29"),
    "DOLPHINS_GRACE": Effect("""Dolphin's Grace""", "dolphins_grace",
                             """Increases swimming speed (only obtainable from dolphins).""", "True", "30"),
    "BAD_OMEN": Effect("""Bad Omen""", "bad_omen",
                       """Causes an illager raid to start upon entering a village (only received from an Illager captain upon its death), higher levels cause a more difficult raid.""",
                       "None", "31"),
    "HERO_OF_THE_VILLAGE": Effect("""Hero of the Village""", "hero_of_the_village",
                                  """Gives discounts on trades with villagers, and makes villagers throw items at the player depending on their profession.""",
                                  "True", "32"),
    "DARKNESS": Effect("""Darkness""", "darkness", """Darkens the players screen.""", "False", "33"),
}

for __k in effect:
    v = effect[__k]
    effect[v.name] = v

# Enchantments
# Derived from https://minecraft.wiki/Enchanting#Summary_of_enchantments, 2024-02-22T23:57:46-08:00
AQUA_AFFINITY = "aqua_affinity"
BANE_OF_ARTHROPODS = "bane_of_arthropods"
BLAST_PROTECTION = "blast_protection"
CHANNELING = "channeling"
CLEAVING = "cleaving"
CURSE_OF_BINDING = "curse_of_binding"
CURSE_OF_VANISHING = "curse_of_vanishing"
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
ENCHANTMENT_GROUP = [
    AQUA_AFFINITY, BANE_OF_ARTHROPODS, BLAST_PROTECTION, CHANNELING, CLEAVING, CURSE_OF_BINDING, CURSE_OF_VANISHING,
    DEPTH_STRIDER, EFFICIENCY, FEATHER_FALLING, FIRE_ASPECT, FIRE_PROTECTION, FLAME, FORTUNE, FROST_WALKER, IMPALING,
    INFINITY, KNOCKBACK, LOOTING, LOYALTY, LUCK_OF_THE_SEA, LURE, MENDING, MULTISHOT, PIERCING, POWER,
    PROJECTILE_PROTECTION, PROTECTION, PUNCH, QUICK_CHARGE, RESPIRATION, RIPTIDE, SHARPNESS, SILK_TOUCH, SMITE,
    SOUL_SPEED, SWEEPING_EDGE, SWIFT_SNEAK, THORNS, UNBREAKING
]

Enchantment = namedtuple("Enchantment", ['name', 'value', 'desc', 'max_level'])
enchantment = {
    "AQUA_AFFINITY": Enchantment("""Aqua Affinity""", "aqua_affinity", """Increases underwater mining speed.""", 1),
    "BANE_OF_ARTHROPODS": Enchantment("""Bane of Arthropods""", "bane_of_arthropods",
                                      """Increases damage and applies Slowness IV to arthropod mobs (spiders, cave spiders, silverfish, endermites and bees).""",
                                      5),
    "BLAST_PROTECTION": Enchantment("""Blast Protection""", "blast_protection",
                                    """Reduces explosion damage and knockback.""", 4),
    "CHANNELING": Enchantment("""Channeling""", "channeling",
                              """During thunderstorms, trident summons a lightning bolt on the target when hitting it.""",
                              1),
    "CLEAVING": Enchantment("""Cleaving""", "cleaving", """Increases damage and shield stun time.""", 3),
    "CURSE_OF_BINDING": Enchantment("""Curse of Binding""", "curse_of_binding",
                                    """Items cannot be removed from armor slots.""", 1),
    "CURSE_OF_VANISHING": Enchantment("""Curse of Vanishing""", "curse_of_vanishing", """Item disappears on death.""",
                                      1),
    "DEPTH_STRIDER": Enchantment("""Depth Strider""", "depth_strider", """Increases underwater movement speed.""", 3),
    "EFFICIENCY": Enchantment("""Efficiency""", "efficiency", """Increases mining speed.""", 5),
    "FEATHER_FALLING": Enchantment("""Feather Falling""", "feather_falling", """Reduces fall damage.""", 4),
    "FIRE_ASPECT": Enchantment("""Fire Aspect""", "fire_aspect", """Sets target on fire.""", 2),
    "FIRE_PROTECTION": Enchantment("""Fire Protection""", "fire_protection", """Reduces fire damage and burn time.""",
                                   4),
    "FLAME": Enchantment("""Flame""", "flame", """Arrows shot are ignited and deal fire damage to the target.""", 1),
    "FORTUNE": Enchantment("""Fortune""", "fortune", """Increases the amount of block drops.""", 3),
    "FROST_WALKER": Enchantment("""Frost Walker""", "frost_walker",
                                """Freezes the water under the player's feet, allowing them to walk over water.""", 2),
    "IMPALING": Enchantment("""Impaling""", "impaling",
                            """Increases damage against aquatic mobs. In Bedrock Edition, increases damage against mobs in water or rain.""",
                            5),
    "INFINITY": Enchantment("""Infinity""", "infinity", """Prevents consumption of arrows.""", 1),
    "KNOCKBACK": Enchantment("""Knockback""", "knockback", """Increases melee knockback.""", 2),
    "LOOTING": Enchantment("""Looting""", "looting", """Increases mob loot.""", 3),
    "LOYALTY": Enchantment("""Loyalty""", "loyalty", """Trident returns after being thrown.""", 3),
    "LUCK_OF_THE_SEA": Enchantment("""Luck of the Sea""", "luck_of_the_sea",
                                   """Increases rate of treasure bites (enchanting books, etc.).""", 3),
    "LURE": Enchantment("""Lure""", "lure", """Decreases time for bites.""", 3),
    "MENDING": Enchantment("""Mending""", "mending", """Repairs the item using experience.""", 1),
    "MULTISHOT": Enchantment("""Multishot""", "multishot", """Fires 3 arrows at the same time.""", 1),
    "PIERCING": Enchantment("""Piercing""", "piercing",
                            """Arrows pierce entities, allowing for arrows to pierce through stacks of mobs.""", 4),
    "POWER": Enchantment("""Power""", "power", """Increases arrow damage.""", 5),
    "PROJECTILE_PROTECTION": Enchantment("""Projectile Protection""", "projectile_protection",
                                         """Reduces damage from projectiles.""", 4),
    "PROTECTION": Enchantment("""Protection""", "protection", """Reduces most forms of damage.""", 4),
    "PUNCH": Enchantment("""Punch""", "punch", """Increases arrow knockback.""", 2),
    "QUICK_CHARGE": Enchantment("""Quick Charge""", "quick_charge", """Decreases crossbow charging time.""", 3),
    "RESPIRATION": Enchantment("""Respiration""", "respiration", """Extends underwater breathing time.""", 3),
    "RIPTIDE": Enchantment("""Riptide""", "riptide",
                           """Trident launches player with itself when thrown while in water or rain.""", 3),
    "SHARPNESS": Enchantment("""Sharpness""", "sharpness", """Increases melee damage.""", 5),
    "SILK_TOUCH": Enchantment("""Silk Touch""", "silk_touch", """Mined blocks drop themselves.""", 1),
    "SMITE": Enchantment("""Smite""", "smite", """Increases damage to the undead.""", 5),
    "SOUL_SPEED": Enchantment("""Soul Speed""", "soul_speed",
                              """Increases movement speed on soul sand and soul soil.""", 3),
    "SWEEPING_EDGE": Enchantment("""Sweeping Edge""", "sweeping_edge", """Increases sweeping attack damage.""", 3),
    "SWIFT_SNEAK": Enchantment("""Swift Sneak""", "swift_sneak", """Increases sneaking speed.""", 3),
    "THORNS": Enchantment("""Thorns""", "thorns", """Taking damage causes the attacker to also take damage.""", 3),
    "UNBREAKING": Enchantment("""Unbreaking""", "unbreaking", """Reduces durability damage.""", 3),
}

for __k in enchantment:
    v = enchantment[__k]
    enchantment[v.name] = v

# GameRules
# Derived from https://minecraft.wiki/Game_rule?so=search#List_of_game_rules, 2024-02-22T23:57:46-08:00
ANNOUNCE_ADVANCEMENTS = "announceAdvancements"
BLOCK_EXPLOSION_DROP_DECAY = "blockExplosionDropDecay"
COMMAND_BLOCK_OUTPUT = "commandBlockOutput"
COMMAND_MODIFICATION_BLOCK_LIMIT = "commandModificationBlockLimit"
DISABLE_ELYTRA_MOVEMENT_CHECK = "disableElytraMovementCheck"
DISABLE_RAIDS = "disableRaids"
DO_DAYLIGHT_CYCLE = "doDaylightCycle"
DO_ENTITY_DROPS = "doEntityDrops"
DO_FIRE_TICK = "doFireTick"
DO_INSOMNIA = "doInsomnia"
DO_IMMEDIATE_RESPAWN = "doImmediateRespawn"
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
LOG_ADMIN_COMMANDS = "logAdminCommands"
MAX_COMMAND_CHAIN_LENGTH = "maxCommandChainLength"
MAX_COMMAND_FORK_COUNT = "maxCommandForkCount"
MAX_ENTITY_CRAMMING = "maxEntityCramming"
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
SPAWN_RADIUS = "spawnRadius"
SPECTATORS_GENERATE_CHUNKS = "spectatorsGenerateChunks"
TNT_EXPLOSION_DROP_DECAY = "tntExplosionDropDecay"
UNIVERSAL_ANGER = "universalAnger"
WATER_SOURCE_CONVERSION = "waterSourceConversion"
GAMERULE_GROUP = [
    ANNOUNCE_ADVANCEMENTS, BLOCK_EXPLOSION_DROP_DECAY, COMMAND_BLOCK_OUTPUT, COMMAND_MODIFICATION_BLOCK_LIMIT,
    DISABLE_ELYTRA_MOVEMENT_CHECK, DISABLE_RAIDS, DO_DAYLIGHT_CYCLE, DO_ENTITY_DROPS, DO_FIRE_TICK, DO_INSOMNIA,
    DO_IMMEDIATE_RESPAWN, DO_LIMITED_CRAFTING, DO_MOB_LOOT, DO_MOB_SPAWNING, DO_PATROL_SPAWNING, DO_TILE_DROPS,
    DO_TRADER_SPAWNING, DO_VINES_SPREAD, DO_WEATHER_CYCLE, DO_WARDEN_SPAWNING, DROWNING_DAMAGE,
    ENDER_PEARLS_VANISH_ON_DEATH, FALL_DAMAGE, FIRE_DAMAGE, FORGIVE_DEAD_PLAYERS, FREEZE_DAMAGE, GLOBAL_SOUND_EVENTS,
    KEEP_INVENTORY, LAVA_SOURCE_CONVERSION, LOG_ADMIN_COMMANDS, MAX_COMMAND_CHAIN_LENGTH, MAX_COMMAND_FORK_COUNT,
    MAX_ENTITY_CRAMMING, MOB_EXPLOSION_DROP_DECAY, MOB_GRIEFING, NATURAL_REGENERATION,
    PLAYERS_NETHER_PORTAL_CREATIVE_DELAY, PLAYERS_NETHER_PORTAL_DEFAULT_DELAY, PLAYERS_SLEEPING_PERCENTAGE,
    PROJECTILES_CAN_BREAK_BLOCKS, RANDOM_TICK_SPEED, REDUCED_DEBUG_INFO, SEND_COMMAND_FEEDBACK, SHOW_DEATH_MESSAGES,
    SNOW_ACCUMULATION_HEIGHT, SPAWN_RADIUS, SPECTATORS_GENERATE_CHUNKS, TNT_EXPLOSION_DROP_DECAY, UNIVERSAL_ANGER,
    WATER_SOURCE_CONVERSION
]

GameRule = namedtuple("GameRule", ['name', 'value', 'desc', 'rule_type'])
gamerule = {
    "ANNOUNCE_ADVANCEMENTS": GameRule("""announce Advancements""", "announceAdvancements",
                                      """Whether advancements should be announced in chat.""", bool),
    "BLOCK_EXPLOSION_DROP_DECAY": GameRule("""block Explosion Drop Decay""", "blockExplosionDropDecay",
                                           """Whether block loot is dropped by all blocks (false) or randomly (true) depending on how far the block is from the center of a block explosion (e.g. clicking a bed in dimensions other than the Overworld).""",
                                           bool),
    "COMMAND_BLOCK_OUTPUT": GameRule("""command Block Output""", "commandBlockOutput",
                                     """Whether command blocks should notify admins when they perform commands.""",
                                     bool),
    "COMMAND_MODIFICATION_BLOCK_LIMIT": GameRule("""command Modification Block Limit""",
                                                 "commandModificationBlockLimit",
                                                 """Controls the maximum number of blocks changed when using /clone, /fill, or /fillbiome.""",
                                                 int),
    "DISABLE_ELYTRA_MOVEMENT_CHECK": GameRule("""disable Elytra Movement Check""", "disableElytraMovementCheck",
                                              """Whether the server should skip checking player speed when the player is wearing elytra. Often helps with jittering due to lag in multiplayer.""",
                                              bool),
    "DISABLE_RAIDS": GameRule("""disable Raids""", "disableRaids", """Whether raids are disabled.""", bool),
    "DO_DAYLIGHT_CYCLE": GameRule("""do Daylight Cycle""", "doDaylightCycle",
                                  """Whether the daylight cycle and moon phases progress.""", bool),
    "DO_ENTITY_DROPS": GameRule("""do Entity Drops""", "doEntityDrops",
                                """Whether entities that are not mobs should have drops.""", bool),
    "DO_FIRE_TICK": GameRule("""do Fire Tick""", "doFireTick",
                             """Whether fire should spread and naturally extinguish.""", bool),
    "DO_INSOMNIA": GameRule("""do Insomnia""", "doInsomnia", """Whether phantoms can spawn in the nighttime.""", bool),
    "DO_IMMEDIATE_RESPAWN": GameRule("""do Immediate Respawn""", "doImmediateRespawn",
                                     """Players respawn immediately without showing the death screen.""", bool),
    "DO_LIMITED_CRAFTING": GameRule("""do Limited Crafting""", "doLimitedCrafting",
                                    """Whether players can craft only those recipes that they have unlocked.""", bool),
    "DO_MOB_LOOT": GameRule("""do Mob Loot""", "doMobLoot", """Whether mobs should drop items and experience orbs.""",
                            bool),
    "DO_MOB_SPAWNING": GameRule("""do Mob Spawning""", "doMobSpawning",
                                """Whether mobs should spawn naturally, or via global spawning logic, such as for cats, phantoms, patrols, wandering traders, or zombie sieges. Does not affect special spawning attempts, like monster spawners, raids, or iron golems.""",
                                bool),
    "DO_PATROL_SPAWNING": GameRule("""do Patrol Spawning""", "doPatrolSpawning", """Whether patrols can spawn.""",
                                   bool),
    "DO_TILE_DROPS": GameRule("""do Tile Drops""", "doTileDrops", """Whether blocks should have drops.""", bool),
    "DO_TRADER_SPAWNING": GameRule("""do Trader Spawning""", "doTraderSpawning",
                                   """Whether wandering traders can spawn.""", bool),
    "DO_VINES_SPREAD": GameRule("""do Vines Spread""", "doVinesSpread",
                                """Whether vines can spread to other blocks. Cave vines, weeping vines, and twisting vines are not affected.""",
                                bool),
    "DO_WEATHER_CYCLE": GameRule("""do Weather Cycle""", "doWeatherCycle",
                                 """Whether the weather can change naturally. The /weather command can still change weather.""",
                                 bool),
    "DO_WARDEN_SPAWNING": GameRule("""do Warden Spawning""", "doWardenSpawning", """Whether wardens can spawn.""",
                                   bool),
    "DROWNING_DAMAGE": GameRule("""drowning Damage""", "drowningDamage",
                                """Whether the player should take damage when drowning.""", bool),
    "ENDER_PEARLS_VANISH_ON_DEATH": GameRule("""ender Pearls Vanish On Death""", "enderPearlsVanishOnDeath",
                                             """Controls whether thrown ender pearls vanish when the player dies.""",
                                             bool),
    "FALL_DAMAGE": GameRule("""fall Damage""", "fallDamage", """Whether the player should take fall damage.""", bool),
    "FIRE_DAMAGE": GameRule("""fire Damage""", "fireDamage",
                            """Whether the player should take damage in fire, lava, campfires, or on magma blocks.""",
                            bool),
    "FORGIVE_DEAD_PLAYERS": GameRule("""forgive Dead Players""", "forgiveDeadPlayers",
                                     """Makes angered neutral mobs stop being angry when the targeted player dies nearby.""",
                                     bool),
    "FREEZE_DAMAGE": GameRule("""freeze Damage""", "freezeDamage",
                              """Whether the player should take damage when inside powder snow.""", bool),
    "GLOBAL_SOUND_EVENTS": GameRule("""global Sound Events""", "globalSoundEvents",
                                    """Whether certain sound events are heard by all players regardless of location.""",
                                    bool),
    "KEEP_INVENTORY": GameRule("""keep Inventory""", "keepInventory",
                               """Whether the player should keep items and experience in their inventory after death.""",
                               bool),
    "LAVA_SOURCE_CONVERSION": GameRule("""lava Source Conversion""", "lavaSourceConversion",
                                       """Whether new sources of lava are allowed to form.""", bool),
    "LOG_ADMIN_COMMANDS": GameRule("""log Admin Commands""", "logAdminCommands",
                                   """Whether to log admin commands to server log.""", bool),
    "MAX_COMMAND_CHAIN_LENGTH": GameRule("""max Command Chain Length""", "maxCommandChainLength",
                                         """The maximum length of a chain of commands that can be executed during one tick. Applies to command blocks and functions.""",
                                         int),
    "MAX_COMMAND_FORK_COUNT": GameRule("""max Command Fork Count""", "maxCommandForkCount",
                                       """The maximum number of forks (contexts) that can be created during one tick. Applies to command blocks and functions.""",
                                       int),
    "MAX_ENTITY_CRAMMING": GameRule("""max Entity Cramming""", "maxEntityCramming",
                                    """The maximum number of pushable entities a mob or player can push, before taking 6 entity cramming damage per half-second. Setting to 0 or lower disables the rule. Damage affects Survival-mode or Adventure-mode players, and all mobs but bats. Pushable entities include non-Spectator-mode players, any mob except bats, as well as boats and minecarts.""",
                                    int),
    "MOB_EXPLOSION_DROP_DECAY": GameRule("""mob Explosion Drop Decay""", "mobExplosionDropDecay",
                                         """Whether block loot is dropped by all blocks (false) or randomly (true) depending on how far the block is from the center of a mob explosion (e.g. Creeper explosion).""",
                                         bool),
    "MOB_GRIEFING": GameRule("""mob Griefing""", "mobGriefing",
                             """Whether creepers, zombies, endermen, ghasts, withers, ender dragons, rabbits, sheep, villagers, silverfish, snow golems, and end crystals.""",
                             bool),
    "NATURAL_REGENERATION": GameRule("""natural Regeneration""", "naturalRegeneration",
                                     """Whether the player can regenerate health naturally if their hunger is full enough (doesn't affect external healing, such as golden apples, the Regeneration effect, etc.).""",
                                     bool),
    "PLAYERS_NETHER_PORTAL_CREATIVE_DELAY": GameRule("""players Nether Portal Creative Delay""",
                                                     "playersNetherPortalCreativeDelay",
                                                     """Controls the time that a creative player needs to stand in a nether portal before changing dimensions.""",
                                                     int),
    "PLAYERS_NETHER_PORTAL_DEFAULT_DELAY": GameRule("""players Nether Portal Default Delay""",
                                                    "playersNetherPortalDefaultDelay",
                                                    """Controls the time that a non-creative player needs to stand in a nether portal before changing dimensions.""",
                                                    int),
    "PLAYERS_SLEEPING_PERCENTAGE": GameRule("""players Sleeping Percentage""", "playersSleepingPercentage",
                                            """What percentage of players in the Overworld must sleep to skip the night. A percentage value of 0 or less allows the night to be skipped by just 1 player, and a percentage value more than 100 prevents players from skipping the night.""",
                                            int),
    "PROJECTILES_CAN_BREAK_BLOCKS": GameRule("""projectiles Can Break Blocks""", "projectilesCanBreakBlocks",
                                             """Whether impact projectiles destroy blocks that are destructible by them, i.e. chorus flowers, pointed dripstone, and decorated pots.""",
                                             bool),
    "RANDOM_TICK_SPEED": GameRule("""random Tick Speed""", "randomTickSpeed",
                                  """How often a random block tick occurs (such as plant growth, leaf decay, etc.) per chunk section per game tick. 0 and negative values disables random ticks, higher numbers increase random ticks. Setting to a high integer results in high speeds of decay and growth. Numbers over 4096 make plant growth or leaf decay instantaneous.""",
                                  int),
    "REDUCED_DEBUG_INFO": GameRule("""reduced Debug Info""", "reducedDebugInfo",
                                   """Whether the debug screen shows all or reduced information; and whether the effects of F3 + B (entity hitboxes) and F3 + G (chunk boundaries) are shown.""",
                                   bool),
    "SEND_COMMAND_FEEDBACK": GameRule("""send Command Feedback""", "sendCommandFeedback",
                                      """Whether the feedback from commands executed by a player should show up in chat. Also affects the default behavior of whether command blocks store their output text.""",
                                      bool),
    "SHOW_DEATH_MESSAGES": GameRule("""show Death Messages""", "showDeathMessages",
                                    """Whether death messages are put into chat when a player dies. Also affects whether a message is sent to the pet's owner when the pet dies.""",
                                    bool),
    "SNOW_ACCUMULATION_HEIGHT": GameRule("""snow Accumulation Height""", "snowAccumulationHeight",
                                         """The maximum number of snow layers that can be accumulated on each block.""",
                                         int),
    "SPAWN_RADIUS": GameRule("""spawn Radius""", "spawnRadius",
                             """The number of blocks outward from the world spawn coordinates that a player spawns in when first joining a server or when dying without a personal spawnpoint. Has no effect on servers where the default game mode is Adventure.""",
                             int),
    "SPECTATORS_GENERATE_CHUNKS": GameRule("""spectators Generate Chunks""", "spectatorsGenerateChunks",
                                           """Whether players in Spectator mode can generate chunks.""", bool),
    "TNT_EXPLOSION_DROP_DECAY": GameRule("""tnt Explosion Drop Decay""", "tntExplosionDropDecay",
                                         """Whether block loot is dropped by all blocks (false) or randomly (true) depending on how far the block is from the center of a TNT explosion.""",
                                         bool),
    "UNIVERSAL_ANGER": GameRule("""universal Anger""", "universalAnger",
                                """Makes angered neutral mobs attack any nearby player, not just the player that angered them. Works best if forgiveDeadPlayers is disabled.""",
                                bool),
    "WATER_SOURCE_CONVERSION": GameRule("""water Source Conversion""", "waterSourceConversion",
                                        """Whether new sources of water are allowed to form.""", bool),
}

for __k in gamerule:
    v = gamerule[__k]
    gamerule[v.name] = v

# ScoreCriterias
# Derived from https://minecraft.wiki/Scoreboard#Criteria, 2024-02-22T23:57:46-08:00
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
SCORECRITERIA_GROUP = [
    DUMMY, TRIGGER, DEATH_COUNT, PLAYER_KILL_COUNT, TOTAL_KILL_COUNT, HEALTH, XP, LEVEL, FOOD, AIR, ARMOR
]

ScoreCriteria = namedtuple("ScoreCriteria", ['name', 'value', 'desc'])
scorecriteria = {
    "DUMMY": ScoreCriteria("""dummy""", "dummy",
                           """Score is changed only by commands, and not by game events such as death. This is useful for event flags, state mappings, currencies,..."""),
    "TRIGGER": ScoreCriteria("""trigger""", "trigger",
                             """Score is changed only by commands, and not by game events such as death. The /trigger command can be used by a player to set or increment/decrement their own score in an objective with this criterion. The /trigger command fails if the objective has not been "enabled" for the player using it, and the objective is disabled for the player after using the /trigger command on it. Note that the /trigger command can be used by ordinary players even if Cheats are off and they are not an Operator. This is useful for player input via /tellraw interfaces."""),
    "DEATH_COUNT": ScoreCriteria("""death Count""", "deathCount",
                                 """Score increments automatically for a player when they die."""),
    "PLAYER_KILL_COUNT": ScoreCriteria("""player Kill Count""", "playerKillCount",
                                       """Score increments automatically for a player when they kill another player."""),
    "TOTAL_KILL_COUNT": ScoreCriteria("""total Kill Count""", "totalKillCount",
                                      """Score increments automatically for a player when they kill another player or a mob."""),
    "HEALTH": ScoreCriteria("""health""", "health",
                            """Ranges from 0 to 20 on a normal player; represents the amount of half-hearts the player has. May appear as 0 for players before their health has changed for the first time. Extra hearts and absorption hearts also count to the health score, meaning that with Attributes/Modifiers or the Health Boost or Absorption status effects, health can far surpass 20."""),
    "XP": ScoreCriteria("""xp""", "xp",
                        """Matches the total amount of experience the player has collected since their last death (or in other words, their score)."""),
    "LEVEL": ScoreCriteria("""level""", "level", """Matches the current experience level of the player."""),
    "FOOD": ScoreCriteria("""food""", "food",
                          """Ranges from 0 to 20; represents the amount of hunger points the player has. May appear as 0 for players before their foodLevel has changed for the first time."""),
    "AIR": ScoreCriteria("""air""", "air",
                         """Ranges from 0 to 300; represents the amount of air the player has left from swimming under water, matches the air nbt tag of the player."""),
    "ARMOR": ScoreCriteria("""armor""", "armor",
                           """Ranges from 0 to 20; represents the amount of armor points the player has. May appear as 0 for players before their armor has changed for the first time."""),
}

for __k in scorecriteria:
    v = scorecriteria[__k]
    scorecriteria[v.name] = v

# Particles
# Derived from https://minecraft.wiki/Particles_(Java_Edition)#Types_of_particles, 2024-02-22T23:57:46-08:00
AMBIENT_ENTITY_EFFECT = "ambient_entity_effect"
ANGRY_VILLAGER = "angry_villager"
ASH = "ash"
BLOCK = "block"
BLOCK_MARKER = "block_marker"
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
FALLING_DUST = "falling_dust"
FALLING_HONEY = "falling_honey"
FALLING_LAVA = "falling_lava"
FALLING_NECTAR = "falling_nectar"
FALLING_OBSIDIAN_TEAR = "falling_obsidian_tear"
FALLING_SPORE_BLOSSOM = "falling_spore_blossom"
FALLING_WATER = "falling_water"
FIREWORK = "firework"
FISHING = "fishing"
FLAME = "flame"
FLASH = "flash"
GLOW = "glow"
GLOW_SQUID_INK = "glow_squid_ink"
GUST = "gust"
GUST_EMITTER = "gust_emitter"
GUST_DUST = "gust_dust"
HAPPY_VILLAGER = "happy_villager"
HEART = "heart"
INSTANT_EFFECT = "instant_effect"
ITEM = "item"
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
POOF = "poof"
PORTAL = "portal"
RAIN = "rain"
REVERSE_PORTAL = "reverse_portal"
SCRAPE = "scrape"
SCULK_CHARGE = "sculk_charge"
SCULK_CHARGE_POP = "sculk_charge_pop"
SCULK_SOUL = "sculk_soul"
SHRIEK = "shriek"
SMALL_FLAME = "small_flame"
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
TOTEM_OF_UNDYING = "totem_of_undying"
TRIAL_SPAWNER_DETECTION = "trial_spawner_detection"
UNDERWATER = "underwater"
VAULT_CONNECTION = "vault_connection"
VIBRATION = "vibration"
WARPED_SPORE = "warped_spore"
WAX_OFF = "wax_off"
WAX_ON = "wax_on"
WHITE_ASH = "white_ash"
WITCH = "witch"
PARTICLE_GROUP = [
    AMBIENT_ENTITY_EFFECT, ANGRY_VILLAGER, ASH, BLOCK, BLOCK_MARKER, BUBBLE, BUBBLE_COLUMN_UP, BUBBLE_POP,
    CAMPFIRE_COSY_SMOKE, CAMPFIRE_SIGNAL_SMOKE, CHERRY_LEAVES, CLOUD, COMPOSTER, CRIMSON_SPORE, CRIT, CURRENT_DOWN,
    DAMAGE_INDICATOR, DOLPHIN, DRAGON_BREATH, DRIPPING_DRIPSTONE_LAVA, DRIPPING_DRIPSTONE_WATER, DRIPPING_HONEY,
    DRIPPING_LAVA, DRIPPING_OBSIDIAN_TEAR, DRIPPING_WATER, DUST, DUST_COLOR_TRANSITION, DUST_PLUME, EFFECT, EGG_CRACK,
    ELDER_GUARDIAN, ELECTRIC_SPARK, ENCHANT, ENCHANTED_HIT, END_ROD, ENTITY_EFFECT, EXPLOSION, EXPLOSION_EMITTER,
    FALLING_DRIPSTONE_LAVA, FALLING_DRIPSTONE_WATER, FALLING_DUST, FALLING_HONEY, FALLING_LAVA, FALLING_NECTAR,
    FALLING_OBSIDIAN_TEAR, FALLING_SPORE_BLOSSOM, FALLING_WATER, FIREWORK, FISHING, FLAME, FLASH, GLOW, GLOW_SQUID_INK,
    GUST, GUST_EMITTER, GUST_DUST, HAPPY_VILLAGER, HEART, INSTANT_EFFECT, ITEM, ITEM_SLIME, ITEM_SNOWBALL,
    LANDING_HONEY, LANDING_LAVA, LANDING_OBSIDIAN_TEAR, LARGE_SMOKE, LAVA, MYCELIUM, NAUTILUS, NOTE, POOF, PORTAL, RAIN,
    REVERSE_PORTAL, SCRAPE, SCULK_CHARGE, SCULK_CHARGE_POP, SCULK_SOUL, SHRIEK, SMALL_FLAME, SMOKE, SNEEZE, SNOWFLAKE,
    SONIC_BOOM, SOUL, SOUL_FIRE_FLAME, SPIT, SPLASH, SPORE_BLOSSOM_AIR, SQUID_INK, SWEEP_ATTACK, TOTEM_OF_UNDYING,
    TRIAL_SPAWNER_DETECTION, UNDERWATER, VAULT_CONNECTION, VIBRATION, WARPED_SPORE, WAX_OFF, WAX_ON, WHITE_ASH, WITCH
]

Particle = namedtuple("Particle", ['name', 'value', 'desc'])
particle = {
    "AMBIENT_ENTITY_EFFECT": Particle("""Ambient Entity Effect""", "ambient_entity_effect",
                                      """Emitted by entities with effects from a beacon or a conduit."""),
    "ANGRY_VILLAGER": Particle("""Angry Villager""", "angry_villager",
                               """Produced when hitting villagers or when villagers fail to breed."""),
    "ASH": Particle("""Ash""", "ash", """Floats throughout the atmosphere in the soul sand valley biome."""),
    "BLOCK": Particle("""Block""", "block",
                      """Produced when blocks are broken, flakes off blocks being brushed, produced when iron golems walk, produced when entities fall a long distance, produced when players sprint, displayed when armor stands are broken, appears when sheep eat grass."""),
    "BLOCK_MARKER": Particle("""Block Marker""", "block_marker",
                             """Marks the position of barriers and light blocks when they are held in the main hand."""),
    "BUBBLE": Particle("""Bubble""", "bubble",
                       """Appears around entities splashing in water, emitted by guardian lasers, produced by guardians moving, appears by the fishing bobber and along the path of a fish, trails behind projectiles and eyes of ender underwater."""),
    "BUBBLE_COLUMN_UP": Particle("""Bubble Column Up""", "bubble_column_up", """Represents upwards bubble columns."""),
    "BUBBLE_POP": Particle("""Bubble Pop""", "bubble_pop", """Unused."""),
    "CAMPFIRE_COSY_SMOKE": Particle("""Campfire Cosy Smoke""", "campfire_cosy_smoke",
                                    """Floats off the top of campfires and soul campfires."""),
    "CAMPFIRE_SIGNAL_SMOKE": Particle("""Campfire Signal Smoke""", "campfire_signal_smoke",
                                      """Floats off the top of campfires and soul campfires above hay bales."""),
    "CHERRY_LEAVES": Particle("""Cherry Leaves""", "cherry_leaves", """Falls off the bottom of cherry leaves."""),
    "CLOUD": Particle("""Cloud""", "cloud",
                      """Appears when placing wet sponges in the Nether, shown when entering a village with the Bad Omen effect."""),
    "COMPOSTER": Particle("""Composter""", "composter", """Produced when placing items in a composter."""),
    "CRIMSON_SPORE": Particle("""Crimson Spore""", "crimson_spore",
                              """Floats throughout the atmosphere in the crimson forest biome."""),
    "CRIT": Particle("""Crit""", "crit",
                     """Trails behind crossbow shots and fully charged bow shots, produced by evoker fangs, appears when landing a critical hit on an entity."""),
    "CURRENT_DOWN": Particle("""Current Down""", "current_down", """Represents downwards bubble columns."""),
    "DAMAGE_INDICATOR": Particle("""Damage Indicator""", "damage_indicator",
                                 """Appears when a melee attack damages an entity."""),
    "DOLPHIN": Particle("""Dolphin""", "dolphin", """Trails behind dolphins."""),
    "DRAGON_BREATH": Particle("""Dragon Breath""", "dragon_breath",
                              """Spit out by the ender dragon, trails behind dragon fireballs, emitted by clouds of dragon's breath, produced when dragon fireballs explode."""),
    "DRIPPING_DRIPSTONE_LAVA": Particle("""Dripping Dripstone Lava""", "dripping_dripstone_lava",
                                        """Represents lava drips collected on pointed dripstone with lava above that have not yet dripped down."""),
    "DRIPPING_DRIPSTONE_WATER": Particle("""Dripping Dripstone Water""", "dripping_dripstone_water",
                                         """Represents water drips collected on pointed dripstone with water or nothing above that have not yet dripped down."""),
    "DRIPPING_HONEY": Particle("""Dripping Honey""", "dripping_honey",
                               """Represents honey drips collected on the bottom of full bee nests or beehives that have not yet dripped down."""),
    "DRIPPING_LAVA": Particle("""Dripping Lava""", "dripping_lava",
                              """Represents lava drips collected on the bottom of blocks with lava above that have not yet dripped down."""),
    "DRIPPING_OBSIDIAN_TEAR": Particle("""Dripping Obsidian Tear""", "dripping_obsidian_tear",
                                       """Represents tears collected on the sides or bottom of crying obsidian that have not yet dripped down."""),
    "DRIPPING_WATER": Particle("""Dripping Water""", "dripping_water",
                               """Represents water drips collected on the bottom of leaves in rain and blocks with water above or the bottom and sides of wet sponges that have not yet dripped down."""),
    "DUST": Particle("""Dust""", "dust",
                     """Emitted by powered redstone torches, powered levers, redstone ore, powered redstone dust, and powered redstone repeaters."""),
    "DUST_COLOR_TRANSITION": Particle("""Dust Color Transition""", "dust_color_transition",
                                      """Emitted by activated sculk sensors."""),
    "DUST_PLUME": Particle("""Dust Plume""", "dust_plume", """Shown when adding items to decorated pots."""),
    "EFFECT": Particle("""Effect""", "effect", """Produced by splash potions."""),
    "EGG_CRACK": Particle("""Egg Crack""", "egg_crack",
                          """Appears when sniffer eggs are placed on moss blocks, appears when sniffer eggs crack."""),
    "ELDER_GUARDIAN": Particle("""Elder Guardian""", "elder_guardian",
                               """Displayed when elder guardians inflict Mining Fatigue."""),
    "ELECTRIC_SPARK": Particle("""Electric Spark""", "electric_spark",
                               """Emitted by lightning rods during thunderstorms, produced when lightning hits copper."""),
    "ENCHANT": Particle("""Enchant""", "enchant", """Floats from bookshelves to enchanting tables."""),
    "ENCHANTED_HIT": Particle("""Enchanted Hit""", "enchanted_hit",
                              """Appears when hitting entities with a sword or an axe enchanted with Sharpness, Bane of Arthropods, or Smite."""),
    "END_ROD": Particle("""End Rod""", "end_rod", """Emitted by end rods, trails behind shulker bullets."""),
    "ENTITY_EFFECT": Particle("""Entity Effect""", "entity_effect",
                              """Emitted by tipped arrows, produced by ravagers when stunned, produced when lingering potions break open, emitted by area effect clouds, produced when evokers cast spells, emitted by the wither as it charges up and when its health is below half, produced by entities with effects from sources other than conduits or beacons."""),
    "EXPLOSION": Particle("""Explosion""", "explosion",
                          """Produced by explosion_emitter particles, shown when shearing mooshrooms, appears when shulker bullets hit the ground, emitted by the ender dragon as it dies, shown when the ender dragon breaks blocks."""),
    "EXPLOSION_EMITTER": Particle("""Explosion Emitter""", "explosion_emitter", """Produced by explosions."""),
    "FALLING_DRIPSTONE_LAVA": Particle("""Falling Dripstone Lava""", "falling_dripstone_lava",
                                       """Drips off pointed dripstone with lava above."""),
    "FALLING_DRIPSTONE_WATER": Particle("""Falling Dripstone Water""", "falling_dripstone_water",
                                        """Drips off pointed dripstone with nothing or water above."""),
    "FALLING_DUST": Particle("""Falling Dust""", "falling_dust",
                             """Falls off the bottom of floating blocks affected by gravity."""),
    "FALLING_HONEY": Particle("""Falling Honey""", "falling_honey",
                              """Drips off beehives and bee nests that are full of honey."""),
    "FALLING_LAVA": Particle("""Falling Lava""", "falling_lava", """Drips off the bottom of blocks with lava above."""),
    "FALLING_NECTAR": Particle("""Falling Nectar""", "falling_nectar",
                               """Falls off bees that have collected pollen."""),
    "FALLING_OBSIDIAN_TEAR": Particle("""Falling Obsidian Tear""", "falling_obsidian_tear",
                                      """Drips off crying obsidian."""),
    "FALLING_SPORE_BLOSSOM": Particle("""Falling Spore Blossom""", "falling_spore_blossom",
                                      """Drips off of spore blossoms."""),
    "FALLING_WATER": Particle("""Falling Water""", "falling_water",
                              """Drips off of the bottom of blocks with water above, drips off the bottom of leaves during rain, drips off of wet sponges."""),
    "FIREWORK": Particle("""Firework""", "firework",
                         """Trails behind fireworks, produced when fireworks crafted with firework stars explode."""),
    "FISHING": Particle("""Fishing""", "fishing", """Represents the fish trail when fishing."""),
    "FLAME": Particle("""Flame""", "flame",
                      """Appears inside of monster spawners, produced by magma cubes, represents the flame of torches, emitted by furnaces."""),
    "FLASH": Particle("""Flash""", "flash", """Shown when fireworks with crafted with firework stars explode."""),
    "GLOW": Particle("""Glow""", "glow", """Emitted by glow squid."""),
    "GLOW_SQUID_INK": Particle("""Glow Squid Ink""", "glow_squid_ink", """Produced by glow squid when hit."""),
    "GUST": Particle("""Gust""", "gust", """Created when a wind charge hits a block."""),
    "GUST_EMITTER": Particle("""Gust Emitter""", "gust_emitter",
                             """Created when a wind charge hits a block. Spawns a number of gust particles."""),
    "GUST_DUST": Particle("""Gust Dust""", "gust_dust", """Unknown."""),
    "HAPPY_VILLAGER": Particle("""Happy Villager""", "happy_villager",
                               """Shown when using bonemeal on plants, appears when trading with villagers, appears when feeding baby animals or dolphins, emitted by villagers upon claiming a job site block or a bed, shown when bees pollinate crops, appears when turtle eggs are placed on sand, appears when turtle eggs hatch."""),
    "HEART": Particle("""Heart""", "heart",
                      """Appears when taming mobs, emitted by breeding mobs, feeding mobs, appears when allays duplicate."""),
    "INSTANT_EFFECT": Particle("""Instant Effect""", "instant_effect",
                               """Produced when splash potions or lingering potions of Instant Health or Instant Damage break."""),
    "ITEM": Particle("""Item""", "item",
                     """Produced when tools break, produced when eating food, produced when splash potions or lingering potions break, shown when eyes of ender break."""),
    "ITEM_SLIME": Particle("""Item Slime""", "item_slime", """Shown when slimes jump."""),
    "ITEM_SNOWBALL": Particle("""Item Snowball""", "item_snowball", """Produced when thrown snowballs break."""),
    "LANDING_HONEY": Particle("""Landing Honey""", "landing_honey",
                              """Created when falling_honey particles hit the ground."""),
    "LANDING_LAVA": Particle("""Landing Lava""", "landing_lava",
                             """Created when falling_lava or falling_dripstone_lava particles hit the ground."""),
    "LANDING_OBSIDIAN_TEAR": Particle("""Landing Obsidian Tear""", "landing_obsidian_tear",
                                      """Created when falling_obsidian_tear particles hit the ground."""),
    "LARGE_SMOKE": Particle("""Large Smoke""", "large_smoke",
                            """Floats off the top of fire, produced by blazes, appears when trying to place water in the Nether, appears when obsidian, stone, or cobblestone is created by lava and water."""),
    "LAVA": Particle("""Lava""", "lava", """Produced by campfires, produced by lava."""),
    "MYCELIUM": Particle("""Mycelium""", "mycelium",
                         """Appears above mycelium, trails behind the wings of phantoms."""),
    "NAUTILUS": Particle("""Nautilus""", "nautilus",
                         """Appears and floats toward conduits, appears and floats towards mobs being attacked by a conduit."""),
    "NOTE": Particle("""Note""", "note", """Produced by jukeboxes, produced by note blocks."""),
    "POOF": Particle("""Poof""", "poof",
                     """Appears when mobs die, shown when ravagers roar after being stunned, produced when silverfish enter stone, appear around mobs spawned by spawners, shown when zombies trample turtle eggs, created when fireworks crafted without stars expire."""),
    "PORTAL": Particle("""Portal""", "portal",
                       """Trails behind eyes of ender, shown when eyes of ender break, floats toward where ender pearls break, points toward where dragon eggs teleport, floats toward where players teleport with chorus fruit, appears and floats toward nether portals, appears and floats toward end gateway portals, appears and floats toward ender chests, emitted by endermen, appears and floats toward endermites."""),
    "RAIN": Particle("""Rain""", "rain", """Appears on the ground during rain."""),
    "REVERSE_PORTAL": Particle("""Reverse Portal""", "reverse_portal", """Floats off the top of respawn anchors."""),
    "SCRAPE": Particle("""Scrape""", "scrape", """Shown when scraping oxidization off copper."""),
    "SCULK_CHARGE": Particle("""Sculk Charge""", "sculk_charge", """Marks the path of a sculk charge."""),
    "SCULK_CHARGE_POP": Particle("""Sculk Charge Pop""", "sculk_charge_pop", """Appears when a sculk charge ends."""),
    "SCULK_SOUL": Particle("""Sculk Soul""", "sculk_soul", """Appears above sculk catalysts when activated."""),
    "SHRIEK": Particle("""Shriek""", "shriek", """Emitted by activated sculk shriekers."""),
    "SMALL_FLAME": Particle("""Small Flame""", "small_flame", """Represents the flame of candles."""),
    "SMOKE": Particle("""Smoke""", "smoke",
                      """Floats off the top of monster spawners, represents the smoke from candles, appears when tnt is primed, floats off the top of wither roses, floats off the top of brewing stands, represents the smoke of torches and soul torches, trails behind ghast fireballs, emitted by withers, trails behind wither skulls, produced when dispensers or droppers fire, trails behind blaze fireballs, emitted by lava and campfires during rain, emitted by furnaces, emitted by blast furnaces, emitted by smokers, produced when placing eyes of ender in an end portal frame, emitted by end portals, produced when redstone torches burn out, floats off the top of food placed on a campfire, shown when campfires and soul campfires are extinguished, shown when failing to tame a mob, trails behind lava particles."""),
    "SNEEZE": Particle("""Sneeze""", "sneeze", """Sneezed out by pandas."""),
    "SNOWFLAKE": Particle("""Snowflake""", "snowflake", """Created by entities in powder snow."""),
    "SONIC_BOOM": Particle("""Sonic Boom""", "sonic_boom", """Produced by the warden during its sonic boom attack."""),
    "SOUL": Particle("""Soul""", "soul",
                     """Created by players with Soul Speed boots running on soul sand or soul soil."""),
    "SOUL_FIRE_FLAME": Particle("""Soul Fire Flame""", "soul_fire_flame", """Represents the flame of soul torches."""),
    "SPIT": Particle("""Spit""", "spit", """Spit out by llamas."""),
    "SPLASH": Particle("""Splash""", "splash",
                       """Produced by entities splashing in water, produced by villagers sweating during a raid, appears above the surface of the water when fishing, created when falling_water or falling_dripstone_water particles hit the ground, shaken off by wolves after exiting water."""),
    "SPORE_BLOSSOM_AIR": Particle("""Spore Blossom Air""", "spore_blossom_air",
                                  """Floats in the atmosphere around spore blossoms."""),
    "SQUID_INK": Particle("""Squid Ink""", "squid_ink", """Produced by squid when hit."""),
    "SWEEP_ATTACK": Particle("""Sweep Attack""", "sweep_attack", """Appears when a sweeping attack is performed."""),
    "TOTEM_OF_UNDYING": Particle("""Totem Of Undying""", "totem_of_undying",
                                 """Produced when a totem of undying is used."""),
    "TRIAL_SPAWNER_DETECTION": Particle("""Trial Spawner Detection""", "trial_spawner_detection",
                                        """Produced when a Trial Spawner is activated."""),
    "UNDERWATER": Particle("""Underwater""", "underwater", """Floats in the atmosphere underwater."""),
    "VAULT_CONNECTION": Particle("""Vault Connection""", "vault_connection",
                                 """Produced when a player is near a vault."""),
    "VIBRATION": Particle("""Vibration""", "vibration",
                          """Moves from sounds to the warden or a sculk sensor, moves froms note blocks to allays."""),
    "WARPED_SPORE": Particle("""Warped Spore""", "warped_spore",
                             """Floats in the atmosphere in warped forest biomes."""),
    "WAX_OFF": Particle("""Wax Off""", "wax_off", """Produced when scraping wax off copper."""),
    "WAX_ON": Particle("""Wax On""", "wax_on", """Produced when using honeycomb on copper."""),
    "WHITE_ASH": Particle("""White Ash""", "white_ash", """Floats in the atmosphere in basalt delta biomes."""),
    "WITCH": Particle("""Witch""", "witch", """Emitted by witches."""),
}

for __k in particle:
    v = particle[__k]
    particle[v.name] = v

# PotterySherds
# Derived from https://minecraft.wiki/Pottery_Sherd, 2024-02-22T23:57:46-08:00
ANGLER_POTTERY_SHERD = "angler_pottery_sherd"
ARCHER_POTTERY_SHERD = "archer_pottery_sherd"
ARMS_UP_POTTERY_SHERD = "arms_up_pottery_sherd"
BLADE_POTTERY_SHERD = "blade_pottery_sherd"
BREWER_POTTERY_SHERD = "brewer_pottery_sherd"
BURN_POTTERY_SHERD = "burn_pottery_sherd"
DANGER_POTTERY_SHERD = "danger_pottery_sherd"
EXPLORER_POTTERY_SHERD = "explorer_pottery_sherd"
FRIEND_POTTERY_SHERD = "friend_pottery_sherd"
HEART_POTTERY_SHERD = "heart_pottery_sherd"
HEARTBREAK_POTTERY_SHERD = "heartbreak_pottery_sherd"
HOWL_POTTERY_SHERD = "howl_pottery_sherd"
MINER_POTTERY_SHERD = "miner_pottery_sherd"
MOURNER_POTTERY_SHERD = "mourner_pottery_sherd"
PLENTY_POTTERY_SHERD = "plenty_pottery_sherd"
PRIZE_POTTERY_SHERD = "prize_pottery_sherd"
SHEAF_POTTERY_SHERD = "sheaf_pottery_sherd"
SHELTER_POTTERY_SHERD = "shelter_pottery_sherd"
SKULL_POTTERY_SHERD = "skull_pottery_sherd"
SNORT_POTTERY_SHERD = "snort_pottery_sherd"
POTTERYSHERD_GROUP = [
    ANGLER_POTTERY_SHERD, ARCHER_POTTERY_SHERD, ARMS_UP_POTTERY_SHERD, BLADE_POTTERY_SHERD, BREWER_POTTERY_SHERD,
    BURN_POTTERY_SHERD, DANGER_POTTERY_SHERD, EXPLORER_POTTERY_SHERD, FRIEND_POTTERY_SHERD, HEART_POTTERY_SHERD,
    HEARTBREAK_POTTERY_SHERD, HOWL_POTTERY_SHERD, MINER_POTTERY_SHERD, MOURNER_POTTERY_SHERD, PLENTY_POTTERY_SHERD,
    PRIZE_POTTERY_SHERD, SHEAF_POTTERY_SHERD, SHELTER_POTTERY_SHERD, SKULL_POTTERY_SHERD, SNORT_POTTERY_SHERD
]

PotterySherd = namedtuple("PotterySherd", ['name', 'value', 'desc'])
potterysherd = {
    "ANGLER_POTTERY_SHERD": PotterySherd("""Angler Pottery Sherd""", "angler_pottery_sherd", """"""),
    "ARCHER_POTTERY_SHERD": PotterySherd("""Archer Pottery Sherd""", "archer_pottery_sherd", """"""),
    "ARMS_UP_POTTERY_SHERD": PotterySherd("""Arms Up Pottery Sherd""", "arms_up_pottery_sherd", """"""),
    "BLADE_POTTERY_SHERD": PotterySherd("""Blade Pottery Sherd""", "blade_pottery_sherd", """"""),
    "BREWER_POTTERY_SHERD": PotterySherd("""Brewer Pottery Sherd""", "brewer_pottery_sherd", """"""),
    "BURN_POTTERY_SHERD": PotterySherd("""Burn Pottery Sherd""", "burn_pottery_sherd", """"""),
    "DANGER_POTTERY_SHERD": PotterySherd("""Danger Pottery Sherd""", "danger_pottery_sherd", """"""),
    "EXPLORER_POTTERY_SHERD": PotterySherd("""Explorer Pottery Sherd""", "explorer_pottery_sherd", """"""),
    "FRIEND_POTTERY_SHERD": PotterySherd("""Friend Pottery Sherd""", "friend_pottery_sherd", """"""),
    "HEART_POTTERY_SHERD": PotterySherd("""Heart Pottery Sherd""", "heart_pottery_sherd", """"""),
    "HEARTBREAK_POTTERY_SHERD": PotterySherd("""Heartbreak Pottery Sherd""", "heartbreak_pottery_sherd", """"""),
    "HOWL_POTTERY_SHERD": PotterySherd("""Howl Pottery Sherd""", "howl_pottery_sherd", """"""),
    "MINER_POTTERY_SHERD": PotterySherd("""Miner Pottery Sherd""", "miner_pottery_sherd", """"""),
    "MOURNER_POTTERY_SHERD": PotterySherd("""Mourner Pottery Sherd""", "mourner_pottery_sherd", """"""),
    "PLENTY_POTTERY_SHERD": PotterySherd("""Plenty Pottery Sherd""", "plenty_pottery_sherd", """"""),
    "PRIZE_POTTERY_SHERD": PotterySherd("""Prize Pottery Sherd""", "prize_pottery_sherd", """"""),
    "SHEAF_POTTERY_SHERD": PotterySherd("""Sheaf Pottery Sherd""", "sheaf_pottery_sherd", """"""),
    "SHELTER_POTTERY_SHERD": PotterySherd("""Shelter Pottery Sherd""", "shelter_pottery_sherd", """"""),
    "SKULL_POTTERY_SHERD": PotterySherd("""Skull Pottery Sherd""", "skull_pottery_sherd", """"""),
    "SNORT_POTTERY_SHERD": PotterySherd("""Snort Pottery Sherd""", "snort_pottery_sherd", """"""),
}

for __k in potterysherd:
    v = potterysherd[__k]
    potterysherd[v.name] = v
