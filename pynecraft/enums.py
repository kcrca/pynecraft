"""Various enums for various groups of constants. Most are generated automatically from the web pages at
minecraft.fandom.com."""
import enum
from enum import Enum
from typing import Tuple


class ValueEnum(Enum):
    def __str__(self):
        return self.value

    def __lt__(self, other):
        return self.value < other.value


# noinspection SpellCheckingInspection
@enum.unique
class TeamOption(ValueEnum):
    DISPLAY_NAME = "displayName"
    """Set the display name of the team."""
    COLOR = "color"
    """Decide the color of the team and players in chat, above their head, on the Tab menu, and on the sidebar. Also changes the color of the outline of the entities caused by the Glowing effect."""
    FRIENDLY_FIRE = "friendlyFire"
    """Enable/Disable players inflicting damage on each other when on the same team. (Note: players can still inflict status effects on each other.) Does not affect some non-player entities in a team."""
    SEE_FRIENDLY_INVISIBLES = "seeFriendlyInvisibles"
    """Decide players can see invisible players on their team as whether semi-transparent or completely invisible."""
    NAMETAG_VISIBILITY = "nametagVisibility"
    """Decide whose name tags above their heads can be seen."""
    DEATH_MESSAGE_VISIBILITY = "deathMessageVisibility"
    """Control the visibility of death messages for players."""
    COLLISION_RULE = "collisionRule"
    """Controls the way the entities on the team collide with other entities."""
    PREFIX = "prefix"
    """Modifies the prefix that displays before players' names."""
    SUFFIX = "suffix"
    """Modifies the suffix that displays after players' names."""

    @staticmethod
    def value_spec(enum):
        return {"displayName": str, "color": str, "friendlyFire": bool, "seeFriendlyInvisibles": bool,
                "nametagVisibility": ['never', 'hideForOtherTeams', 'hideForOwnTeam', 'always'],
                "deathMessageVisibility": ['never', 'hideForOtherTeams', 'hideForOwnTeam', 'always'],
                "collisionRule": ['never', 'pushOtherTeams', 'pushOwnTeam', 'always'], "prefix": str, "suffix": str, }[
            enum.value]


# noinspection SpellCheckingInspection
@enum.unique
class Pattern(ValueEnum):
    NONE = ''
    DOWN_RIGHT_STRIPE = 'drs'
    DOWN_LEFT_STRIPE = 'dls'
    CROSS = 'cr'
    BOTTOM_STRIPE = 'bs'
    MIDDLE_STRIPE = 'ms'
    TOP_STRIPE = 'ts'
    SQUARE_CROSS = 'sc'
    LEFT_STRIPE = 'ls'
    CENTER_STRIPE = 'cs'
    RIGHT_STRIPE = 'rs'
    SMALL_STRIPES = 'ss'
    LEFT_DIAGONAL = 'ld'
    RIGHT_UPSIDE_DOWN_DIAGONAL = 'rud'
    LEFT_UPSIDE_DOWN_DIAGONAL = 'lud'
    RIGHT_DIAGONAL = 'rd'
    VERTICAL_HALF_LEFT = 'vh'
    VERTICAL_HALF_RIGHT = 'vhr'
    HORIZONTAL_HALF_BOTTOM = 'hhb'
    HORIZONTAL_HALF_TOP = 'hh'
    BOTTOM_LEFT_CORNER = 'bl'
    BOTTOM_RIGHT_CORNER = 'br'
    TOP_LEFT_CORNER = 'tl'
    TOP_RIGHT_CORNER = 'tr'
    BOTTOM_TRIANGLE = 'bt'
    TOP_TRIANGLE = 'tt'
    BOTTOM_TRIANGLE_SAWTOOTH = 'bts'
    TOP_TRIANGLE_SAWTOOTH = 'tts'
    MIDDLE_CIRCLE = 'mc'
    MIDDLE_RHOMBUS = 'mr'
    BORDER = 'bo'
    CURLY_BORDER = 'cbo'
    GRADIENT = 'gra'
    GRADIENT_UPSIDE_DOWN = 'gru'
    CREEPER = 'cre'
    BRICK = 'bri'
    SKULL = 'sku'
    FLOWER = 'flo'
    MOJANG = 'moj'
    GLOBE = 'glb'
    PIG = 'pig'

    @staticmethod
    def sign_text(pattern) -> Tuple[str]:
        return {'': ('Blank',), 'drs': ('Down Right Stripe',), 'dls': ('Down Left Stripe',), 'cr': ('Cross',),
                'bs': ('Bottom Stripe',), 'ms': ('Middle Stripe',), 'ts': ('Top Stripe',), 'sc': ('Square Cross',),
                'ls': ('Left Stripe',), 'cs': ('Center Stripe',), 'rs': ('Right Stripe',), 'ss': ('Small Stripes',),
                'ld': ('Left Diagonal',), 'rud': ('Right Upside-Down', 'Diagonal',),
                'lud': ('Left Upside-Down', 'Diagonal',), 'rd': ('Right Diagonal',), 'vh': ('Vertical Half', '(Left)',),
                'vhr': ('Vertical Half', '(Right)',), 'hhb': ('Horizontal Half', '(Bottom)',),
                'hh': ('Horizontal Half', '(Top)',), 'bl': ('Bottom Left', 'Corner',),
                'br': ('Bottom Right', 'Corner',), 'tl': ('Top Left', 'Corner',), 'tr': ('Top Right', 'Corner',),
                'bt': ('Bottom Triangle',), 'tt': ('Top Triangle',), 'bts': ('Bottom Triangle', 'Sawtooth',),
                'tts': ('Top Triangle', 'Sawtooth',), 'mc': ('Middle Circle',), 'mr': ('Middle Rhombus',),
                'bo': ('Border',), 'cbo': ('Curly Border',), 'gra': ('Gradient',), 'gru': ('Gradient', 'Upside-Down',),
                'cre': ('Creeper',), 'bri': ('Brick',), 'sku': ('Skull',), 'flo': ('Flower',), 'moj': ('Mojang',),
                'glb': ('Globe',), 'pig': ('Pig',), }[pattern.value]


# Generated enums:


# noinspection SpellCheckingInspection,GrazieInspection
@enum.unique
class Advancement(ValueEnum):
    MINECRAFT = "story/root"
    """The heart and story of the game."""
    STONE_AGE = "story/mine_stone"
    """Mine Stone with your new Pickaxe."""
    GETTING_AN_UPGRADE = "story/upgrade_tools"
    """Construct a better Pickaxe."""
    ACQUIRE_HARDWARE = "story/smelt_iron"
    """Smelt an Iron Ingot."""
    SUIT_UP = "story/obtain_armor"
    """Protect yourself with a piece of iron armor."""
    HOT_STUFF = "story/lava_bucket"
    """Fill a Bucket with lava."""
    ISNT_IT_IRON_PICK = "story/iron_tools"
    """Upgrade your Pickaxe."""
    NOT_TODAY_THANK_YOU = "story/deflect_arrow"
    """Deflect a projectile with a Shield."""
    ICE_BUCKET_CHALLENGE = "story/form_obsidian"
    """Obtain a block of Obsidian."""
    DIAMONDS = "story/mine_diamond"
    """Acquire diamonds."""
    WE_NEED_TO_GO_DEEPER = "story/enter_the_nether"
    """Build, light and enter a Nether Portal."""
    COVER_ME_WITH_DIAMONDS = "story/shiny_gear"
    """Diamond armor saves lives."""
    ENCHANTER = "story/enchant_item"
    """Enchant an item at an Enchanting Table."""
    ZOMBIE_DOCTOR = "story/cure_zombie_villager"
    """Weaken and then cure a Zombie Villager."""
    EYE_SPY = "story/follow_ender_eye"
    """Follow an Eye of Ender."""
    ENTER_THE_END = "story/enter_the_end"
    """Enter the End Portal."""
    NETHER = "nether/root"
    """Bring summer clothes."""
    RETURN_TO_SENDER = "nether/return_to_sender"
    """Destroy a Ghast with a fireball."""
    THOSE_WERE_THE_DAYS = "nether/find_bastion"
    """Enter a Bastion Remnant."""
    HIDDEN_IN_THE_DEPTHS = "nether/obtain_ancient_debris"
    """Obtain Ancient Debris."""
    SUBSPACE_BUBBLE = "nether/fast_travel"
    """Use the Nether to travel 7 km in the Overworld."""
    A_TERRIBLE_FORTRESS = "nether/find_fortress"
    """Break your way into a Nether Fortress."""
    WHO_IS_CUTTING_ONIONS = "nether/obtain_crying_obsidian"
    """Obtain Crying Obsidian."""
    OH_SHINY = "nether/distract_piglin"
    """Distract Piglins with gold."""
    THIS_BOAT_HAS_LEGS = "nether/ride_strider"
    """Ride a Strider with a Warped Fungus on a Stick."""
    UNEASY_ALLIANCE = "nether/uneasy_alliance"
    """Rescue a Ghast from the Nether, bring it safely home to the Overworld... and then kill it."""
    WAR_PIGS = "nether/loot_bastion"
    """Loot a Chest in a Bastion Remnant."""
    COUNTRY_LODE_TAKE_ME_HOME = "nether/use_lodestone"
    """Use a Compass on a Lodestone."""
    COVER_ME_IN_DEBRIS = "nether/netherite_armor"
    """Get a full suit of Netherite armor."""
    SPOOKY_SCARY_SKELETON = "nether/get_wither_skull"
    """Obtain a Wither Skeleton's skull."""
    INTO_FIRE = "nether/obtain_blaze_rod"
    """Relieve a Blaze of its rod."""
    NOT_QUITE_NINE_LIVES = "nether/charge_respawn_anchor"
    """Charge a Respawn Anchor to the maximum."""
    FEELS_LIKE_HOME = "nether/ride_strider_in_overworld_lava"
    """Take a Strider for a loooong ride on a lava lake in the Overworld."""
    HOT_TOURIST_DESTINATIONS = "nether/explore_nether"
    """Explore all Nether biomes."""
    WITHERING_HEIGHTS = "nether/summon_wither"
    """Summon the Wither."""
    LOCAL_BREWERY = "nether/brew_potion"
    """Brew a Potion."""
    BRING_HOME_THE_BEACON = "nether/create_beacon"
    """Construct and place a Beacon."""
    A_FURIOUS_COCKTAIL = "nether/all_potions"
    """Have every potion effect applied at the same time."""
    BEACONATOR = "nether/create_full_beacon"
    """Bring a Beacon to full power."""
    HOW_DID_WE_GET_HERE = "nether/all_effects"
    """Have every effect applied at the same time."""
    THE_END = "end/root"
    """Or the beginning?"""
    FREE_THE_END = "end/kill_dragon"
    """Good luck."""
    THE_NEXT_GENERATION = "end/dragon_egg"
    """Hold the Dragon Egg."""
    REMOTE_GETAWAY = "end/enter_end_gateway"
    """Escape the island."""
    THE_END_AGAIN = "end/respawn_dragon"
    """Respawn the Ender Dragon."""
    YOU_NEED_A_MINT = "end/dragon_breath"
    """Collect Dragon's Breath in a Glass Bottle."""
    THE_CITY_AT_THE_END_OF_THE_GAME = "end/find_end_city"
    """Go on in, what could happen?"""
    SKYS_THE_LIMIT = "end/elytra"
    """Find Elytra."""
    GREAT_VIEW_FROM_UP_HERE = "end/levitate"
    """Levitate up 50 blocks from the attacks of a Shulker."""
    ADVENTURE = "adventure/root"
    """Adventure, exploration and combat."""
    VOLUNTARY_EXILE = "adventure/voluntary_exile"
    """Kill a raid captain.Maybe consider staying away from villages for the time being..."""
    IS_IT_A_BIRD = "adventure/spyglass_at_parrot"
    """Look at a Parrot through a Spyglass."""
    MONSTER_HUNTER = "adventure/kill_a_mob"
    """Kill any hostile monster."""
    THE_POWER_OF_BOOKS = "adventure/read_power_of_chiseled_bookshelf"
    """Read the power signal of a Chiseled Bookshelf using a Comparator."""
    WHAT_A_DEAL = "adventure/trade"
    """Successfully trade with a Villager."""
    CRAFTING_A_NEW_LOOK = "adventure/trim_with_any_armor_pattern"
    """Craft a trimmed armor at a Smithing Table."""
    STICKY_SITUATION = "adventure/honey_block_slide"
    """Jump into a Honey Block to break your fall."""
    OL_BETSY = "adventure/ol_betsy"
    """Shoot a Crossbow."""
    SURGE_PROTECTOR = "adventure/lightning_rod_with_villager_no_fire"
    """Protect a Villager from an undesired shock without starting a fire."""
    CAVES__CLIFFS = "adventure/fall_from_world_height"
    """Free fall from the top of the world (build limit) to the bottom of the world and survive."""
    RESPECTING_THE_REMNANTS = "adventure/salvage_sherd"
    """Brush a Suspicious block to obtain a Pottery Sherd."""
    SNEAK_100 = "adventure/avoid_vibration"
    """Sneak near a Sculk Sensor or Warden to prevent it from detecting you."""
    SWEET_DREAMS = "adventure/sleep_in_bed"
    """Sleep in a Bed to change your respawn point."""
    HERO_OF_THE_VILLAGE = "adventure/hero_of_the_village"
    """Successfully defend a village from a raid."""
    IS_IT_A_BALLOON = "adventure/spyglass_at_ghast"
    """Look at a Ghast through a Spyglass."""
    A_THROWAWAY_JOKE = "adventure/throw_trident"
    """Throw a Trident at something.Note: Throwing away your only weapon is not a good idea."""
    IT_SPREADS = "adventure/kill_mob_near_sculk_catalyst"
    """Kill a mob near a Sculk Catalyst."""
    TAKE_AIM = "adventure/shoot_arrow"
    """Shoot something with an Arrow."""
    MONSTERS_HUNTED = "adventure/kill_all_mobs"
    """Kill one of every hostile monster."""
    POSTMORTAL = "adventure/totem_of_undying"
    """Use a Totem of Undying to cheat death."""
    HIRED_HELP = "adventure/summon_iron_golem"
    """Summon an Iron Golem to help defend a village."""
    STAR_TRADER = "adventure/trade_at_world_height"
    """Trade with a Villager at the build height limit."""
    SMITHING_WITH_STYLE = "adventure/trim_with_all_exclusive_armor_patterns"
    """Apply these smithing templates at least once: Spire, Snout, Rib, Ward, Silence, Vex, Tide, Wayfinder."""
    TWO_BIRDS_ONE_ARROW = "adventure/two_birds_one_arrow"
    """Kill two Phantoms with a piercing Arrow."""
    WHOS_THE_PILLAGER_NOW = "adventure/whos_the_pillager_now"
    """Give a Pillager a taste of their own medicine."""
    ARBALISTIC = "adventure/arbalistic"
    """Kill five unique mobs with one crossbow shot."""
    CAREFUL_RESTORATION = "adventure/craft_decorated_pot_using_only_sherds"
    """Make a Decorated Pot out of 4 Pottery Sherds."""
    ADVENTURING_TIME = "adventure/adventuring_time"
    """Discover every biome."""
    SOUND_OF_MUSIC = "adventure/play_jukebox_in_meadows"
    """Make the Meadows come alive with the sound of music from a Jukebox."""
    LIGHT_AS_A_RABBIT = "adventure/walk_on_powder_snow_with_leather_boots"
    """Walk on Powder Snow... without sinking in it."""
    IS_IT_A_PLANE = "adventure/spyglass_at_dragon"
    """Look at the Ender Dragon through a Spyglass."""
    VERY_VERY_FRIGHTENING = "adventure/very_very_frightening"
    """Strike a Villager with lightning."""
    SNIPER_DUEL = "adventure/sniper_duel"
    """Kill a Skeleton from at least 50 meters away."""
    BULLSEYE = "adventure/bullseye"
    """Hit the bullseye of a Target block from at least 30 meters away."""
    HUSBANDRY = "husbandry/root"
    """The world is full of friends and food."""
    BEE_OUR_GUEST = "husbandry/safely_harvest_honey"
    """Use a Campfire to collect Honey from a Beehive using a Glass Bottle without aggravating the Bees."""
    THE_PARROTS_AND_THE_BATS = "husbandry/breed_an_animal"
    """Breed two animals together."""
    YOUVE_GOT_A_FRIEND_IN_ME = "husbandry/allay_deliver_item_to_player"
    """Have an Allay deliver items to you."""
    WHATEVER_FLOATS_YOUR_GOAT = "husbandry/ride_a_boat_with_a_goat"
    """Get in a Boat and float with a Goat."""
    BEST_FRIENDS_FOREVER = "husbandry/tame_an_animal"
    """Tame an animal."""
    GLOW_AND_BEHOLD = "husbandry/make_a_sign_glow"
    """Make the text of any kind of sign glow."""
    FISHY_BUSINESS = "husbandry/fishy_business"
    """Catch a fish."""
    TOTAL_BEELOCATION = "husbandry/silk_touch_nest"
    """Move a Bee Nest, with 3 Bees inside, using Silk Touch."""
    BUKKIT_BUKKIT = "husbandry/tadpole_in_a_bucket"
    """Catch a Tadpole in a Bucket."""
    SMELLS_INTERESTING = "husbandry/obtain_sniffer_egg"
    """Obtain a Sniffer Egg."""
    A_SEEDY_PLACE = "husbandry/plant_seed"
    """Plant a seed and watch it grow."""
    WAX_ON = "husbandry/wax_on"
    """Apply Honeycomb to a Copper block!"""
    TWO_BY_TWO = "husbandry/bred_all_animals"
    """Breed all the animals!"""
    BIRTHDAY_SONG = "husbandry/allay_deliver_cake_to_note_block"
    """Have an Allay drop a Cake at a Note Block."""
    A_COMPLETE_CATALOGUE = "husbandry/complete_catalogue"
    """Tame all Cat variants!"""
    TACTICAL_FISHING = "husbandry/tactical_fishing"
    """Catch a Fish... without a Fishing Rod!"""
    WHEN_THE_SQUAD_HOPS_INTO_TOWN = "husbandry/leash_all_frog_variants"
    """Get each Frog variant on a Lead."""
    LITTLE_SNIFFS = "husbandry/feed_snifflet"
    """Feed a Snifflet."""
    A_BALANCED_DIET = "husbandry/balanced_diet"
    """Eat everything that is edible, even if it's not good for you."""
    SERIOUS_DEDICATION = "husbandry/obtain_netherite_hoe"
    """Use a Netherite Ingot to upgrade a Hoe, and then reevaluate your life choices."""
    WAX_OFF = "husbandry/wax_off"
    """Scrape Wax off of a Copper block!"""
    THE_CUTEST_PREDATOR = "husbandry/axolotl_in_a_bucket"
    """Catch an Axolotl in a Bucket."""
    WITH_OUR_POWERS_COMBINED = "husbandry/froglights"
    """Have all Froglights in your inventory."""
    PLANTING_THE_PAST = "husbandry/plant_any_sniffer_seed"
    """Plant any Sniffer seed."""
    THE_HEALING_POWER_OF_FRIENDSHIP = "husbandry/kill_axolotl_target"
    """Team up with an axolotl and win a fight."""

    def display_name(self) -> str:
        return _advancement_display[self]


# noinspection SpellCheckingInspection,GrazieInspection
_advancement_display = {Advancement.MINECRAFT: "Minecraft", Advancement.STONE_AGE: "Stone Age",
                        Advancement.GETTING_AN_UPGRADE: "Getting an Upgrade",
                        Advancement.ACQUIRE_HARDWARE: "Acquire Hardware", Advancement.SUIT_UP: "Suit Up",
                        Advancement.HOT_STUFF: "Hot Stuff", Advancement.ISNT_IT_IRON_PICK: "Isn't It Iron Pick",
                        Advancement.NOT_TODAY_THANK_YOU: "Not Today, Thank You",
                        Advancement.ICE_BUCKET_CHALLENGE: "Ice Bucket Challenge", Advancement.DIAMONDS: "Diamonds!",
                        Advancement.WE_NEED_TO_GO_DEEPER: "We Need to Go Deeper",
                        Advancement.COVER_ME_WITH_DIAMONDS: "Cover Me with Diamonds",
                        Advancement.ENCHANTER: "Enchanter", Advancement.ZOMBIE_DOCTOR: "Zombie Doctor",
                        Advancement.EYE_SPY: "Eye Spy", Advancement.ENTER_THE_END: "The End?",
                        Advancement.NETHER: "Nether", Advancement.RETURN_TO_SENDER: "Return to Sender",
                        Advancement.THOSE_WERE_THE_DAYS: "Those Were the Days",
                        Advancement.HIDDEN_IN_THE_DEPTHS: "Hidden in the Depths",
                        Advancement.SUBSPACE_BUBBLE: "Subspace Bubble",
                        Advancement.A_TERRIBLE_FORTRESS: "A Terrible Fortress",
                        Advancement.WHO_IS_CUTTING_ONIONS: "Who is Cutting Onions?", Advancement.OH_SHINY: "Oh Shiny",
                        Advancement.THIS_BOAT_HAS_LEGS: "This Boat Has Legs",
                        Advancement.UNEASY_ALLIANCE: "Uneasy Alliance", Advancement.WAR_PIGS: "War Pigs",
                        Advancement.COUNTRY_LODE_TAKE_ME_HOME: "Country Lode, Take Me Home",
                        Advancement.COVER_ME_IN_DEBRIS: "Cover Me in Debris",
                        Advancement.SPOOKY_SCARY_SKELETON: "Spooky Scary Skeleton", Advancement.INTO_FIRE: "Into Fire",
                        Advancement.NOT_QUITE_NINE_LIVES: "Not Quite \"Nine\" Lives",
                        Advancement.FEELS_LIKE_HOME: "Feels Like Home",
                        Advancement.HOT_TOURIST_DESTINATIONS: "Hot Tourist Destinations",
                        Advancement.WITHERING_HEIGHTS: "Withering Heights", Advancement.LOCAL_BREWERY: "Local Brewery",
                        Advancement.BRING_HOME_THE_BEACON: "Bring Home the Beacon",
                        Advancement.A_FURIOUS_COCKTAIL: "A Furious Cocktail", Advancement.BEACONATOR: "Beaconator",
                        Advancement.HOW_DID_WE_GET_HERE: "How Did We Get Here?", Advancement.THE_END: "The End",
                        Advancement.FREE_THE_END: "Free the End",
                        Advancement.THE_NEXT_GENERATION: "The Next Generation",
                        Advancement.REMOTE_GETAWAY: "Remote Getaway", Advancement.THE_END_AGAIN: "The End... Again...",
                        Advancement.YOU_NEED_A_MINT: "You Need a Mint",
                        Advancement.THE_CITY_AT_THE_END_OF_THE_GAME: "The City at the End of the Game",
                        Advancement.SKYS_THE_LIMIT: "Sky's the Limit",
                        Advancement.GREAT_VIEW_FROM_UP_HERE: "Great View From Up Here",
                        Advancement.ADVENTURE: "Adventure", Advancement.VOLUNTARY_EXILE: "Voluntary Exile",
                        Advancement.IS_IT_A_BIRD: "Is It a Bird?", Advancement.MONSTER_HUNTER: "Monster Hunter",
                        Advancement.THE_POWER_OF_BOOKS: "The Power of Books", Advancement.WHAT_A_DEAL: "What a Deal!",
                        Advancement.CRAFTING_A_NEW_LOOK: "Crafting a New Look",
                        Advancement.STICKY_SITUATION: "Sticky Situation", Advancement.OL_BETSY: "Ol' Betsy",
                        Advancement.SURGE_PROTECTOR: "Surge Protector", Advancement.CAVES__CLIFFS: "Caves & Cliffs",
                        Advancement.RESPECTING_THE_REMNANTS: "Respecting the Remnants",
                        Advancement.SNEAK_100: "Sneak 100", Advancement.SWEET_DREAMS: "Sweet Dreams",
                        Advancement.HERO_OF_THE_VILLAGE: "Hero of the Village",
                        Advancement.IS_IT_A_BALLOON: "Is It a Balloon?",
                        Advancement.A_THROWAWAY_JOKE: "A Throwaway Joke", Advancement.IT_SPREADS: "It Spreads",
                        Advancement.TAKE_AIM: "Take Aim", Advancement.MONSTERS_HUNTED: "Monsters Hunted",
                        Advancement.POSTMORTAL: "Postmortal", Advancement.HIRED_HELP: "Hired Help",
                        Advancement.STAR_TRADER: "Star Trader", Advancement.SMITHING_WITH_STYLE: "Smithing with Style",
                        Advancement.TWO_BIRDS_ONE_ARROW: "Two Birds, One Arrow",
                        Advancement.WHOS_THE_PILLAGER_NOW: "Who's the Pillager Now?",
                        Advancement.ARBALISTIC: "Arbalistic", Advancement.CAREFUL_RESTORATION: "Careful Restoration",
                        Advancement.ADVENTURING_TIME: "Adventuring Time", Advancement.SOUND_OF_MUSIC: "Sound of Music",
                        Advancement.LIGHT_AS_A_RABBIT: "Light as a Rabbit", Advancement.IS_IT_A_PLANE: "Is It a Plane?",
                        Advancement.VERY_VERY_FRIGHTENING: "Very Very Frightening",
                        Advancement.SNIPER_DUEL: "Sniper Duel", Advancement.BULLSEYE: "Bullseye",
                        Advancement.HUSBANDRY: "Husbandry", Advancement.BEE_OUR_GUEST: "Bee Our Guest",
                        Advancement.THE_PARROTS_AND_THE_BATS: "The Parrots and the Bats",
                        Advancement.YOUVE_GOT_A_FRIEND_IN_ME: "You've Got a Friend in Me",
                        Advancement.WHATEVER_FLOATS_YOUR_GOAT: "Whatever Floats Your Goat!",
                        Advancement.BEST_FRIENDS_FOREVER: "Best Friends Forever",
                        Advancement.GLOW_AND_BEHOLD: "Glow and Behold!", Advancement.FISHY_BUSINESS: "Fishy Business",
                        Advancement.TOTAL_BEELOCATION: "Total Beelocation", Advancement.BUKKIT_BUKKIT: "Bukkit Bukkit",
                        Advancement.SMELLS_INTERESTING: "Smells Interesting",
                        Advancement.A_SEEDY_PLACE: "A Seedy Place", Advancement.WAX_ON: "Wax On",
                        Advancement.TWO_BY_TWO: "Two by Two", Advancement.BIRTHDAY_SONG: "Birthday Song",
                        Advancement.A_COMPLETE_CATALOGUE: "A Complete Catalogue",
                        Advancement.TACTICAL_FISHING: "Tactical Fishing",
                        Advancement.WHEN_THE_SQUAD_HOPS_INTO_TOWN: "When the Squad Hops into Town",
                        Advancement.LITTLE_SNIFFS: "Little Sniffs", Advancement.A_BALANCED_DIET: "A Balanced Diet",
                        Advancement.SERIOUS_DEDICATION: "Serious Dedication", Advancement.WAX_OFF: "Wax Off",
                        Advancement.THE_CUTEST_PREDATOR: "The Cutest Predator",
                        Advancement.WITH_OUR_POWERS_COMBINED: "With Our Powers Combined!",
                        Advancement.PLANTING_THE_PAST: "Planting the Past",
                        Advancement.THE_HEALING_POWER_OF_FRIENDSHIP: "The Healing Power of Friendship!"}


# noinspection SpellCheckingInspection,GrazieInspection
@enum.unique
class BiomeId(ValueEnum):
    THE_VOID = "the_void"
    """The Void."""
    PLAINS = "plains"
    """Plains."""
    SUNFLOWER_PLAINS = "sunflower_plains"
    """Sunflower Plains."""
    SNOWY_PLAINS = "snowy_plains"
    """Snowy Plains."""
    ICE_SPIKES = "ice_spikes"
    """Ice Spikes."""
    DESERT = "desert"
    """Desert."""
    SWAMP = "swamp"
    """Swamp."""
    MANGROVE_SWAMP = "mangrove_swamp"
    """Mangrove Swamp."""
    FOREST = "forest"
    """Forest."""
    FLOWER_FOREST = "flower_forest"
    """Flower Forest."""
    BIRCH_FOREST = "birch_forest"
    """Birch Forest."""
    DARK_FOREST = "dark_forest"
    """Dark Forest."""
    OLD_GROWTH_BIRCH_FOREST = "old_growth_birch_forest"
    """Old Growth Birch Forest."""
    OLD_GROWTH_PINE_TAIGA = "old_growth_pine_taiga"
    """Old Growth Pine Taiga."""
    OLD_GROWTH_SPRUCE_TAIGA = "old_growth_spruce_taiga"
    """Old Growth Spruce Taiga."""
    TAIGA = "taiga"
    """Taiga."""
    SNOWY_TAIGA = "snowy_taiga"
    """Snowy Taiga."""
    SAVANNA = "savanna"
    """Savanna."""
    SAVANNA_PLATEAU = "savanna_plateau"
    """Savanna Plateau."""
    WINDSWEPT_HILLS = "windswept_hills"
    """Windswept Hills."""
    WINDSWEPT_GRAVELLY_HILLS = "windswept_gravelly_hills"
    """Windswept Gravelly Hills."""
    WINDSWEPT_FOREST = "windswept_forest"
    """Windswept Forest."""
    WINDSWEPT_SAVANNA = "windswept_savanna"
    """Windswept Savanna."""
    JUNGLE = "jungle"
    """Jungle."""
    SPARSE_JUNGLE = "sparse_jungle"
    """Sparse Jungle."""
    BAMBOO_JUNGLE = "bamboo_jungle"
    """Bamboo Jungle."""
    BADLANDS = "badlands"
    """Badlands."""
    ERODED_BADLANDS = "eroded_badlands"
    """Eroded Badlands."""
    WOODED_BADLANDS = "wooded_badlands"
    """Wooded Badlands."""
    MEADOW = "meadow"
    """Meadow."""
    CHERRY_GROVE = "cherry_grove"
    """Cherry Grove."""
    GROVE = "grove"
    """Grove."""
    SNOWY_SLOPES = "snowy_slopes"
    """Snowy Slopes."""
    FROZEN_PEAKS = "frozen_peaks"
    """Frozen Peaks."""
    JAGGED_PEAKS = "jagged_peaks"
    """Jagged Peaks."""
    STONY_PEAKS = "stony_peaks"
    """Stony Peaks."""
    RIVER = "river"
    """River."""
    FROZEN_RIVER = "frozen_river"
    """Frozen River."""
    BEACH = "beach"
    """Beach."""
    SNOWY_BEACH = "snowy_beach"
    """Snowy Beach."""
    STONY_SHORE = "stony_shore"
    """Stony Shore."""
    WARM_OCEAN = "warm_ocean"
    """Warm Ocean."""
    LUKEWARM_OCEAN = "lukewarm_ocean"
    """Lukewarm Ocean."""
    DEEP_LUKEWARM_OCEAN = "deep_lukewarm_ocean"
    """Deep Lukewarm Ocean."""
    OCEAN = "ocean"
    """Ocean."""
    DEEP_OCEAN = "deep_ocean"
    """Deep Ocean."""
    COLD_OCEAN = "cold_ocean"
    """Cold Ocean."""
    DEEP_COLD_OCEAN = "deep_cold_ocean"
    """Deep Cold Ocean."""
    FROZEN_OCEAN = "frozen_ocean"
    """Frozen Ocean."""
    DEEP_FROZEN_OCEAN = "deep_frozen_ocean"
    """Deep Frozen Ocean."""
    MUSHROOM_FIELDS = "mushroom_fields"
    """Mushroom Fields."""
    DRIPSTONE_CAVES = "dripstone_caves"
    """Dripstone Caves."""
    LUSH_CAVES = "lush_caves"
    """Lush Caves."""
    DEEP_DARK = "deep_dark"
    """Deep Dark."""
    NETHER_WASTES = "nether_wastes"
    """Nether Wastes."""
    WARPED_FOREST = "warped_forest"
    """Warped Forest."""
    CRIMSON_FOREST = "crimson_forest"
    """Crimson Forest."""
    SOUL_SAND_VALLEY = "soul_sand_valley"
    """Soul Sand Valley."""
    BASALT_DELTAS = "basalt_deltas"
    """Basalt Deltas."""
    THE_END = "the_end"
    """The End."""
    END_HIGHLANDS = "end_highlands"
    """End Highlands."""
    END_MIDLANDS = "end_midlands"
    """End Midlands."""
    SMALL_END_ISLANDS = "small_end_islands"
    """Small End Islands."""
    END_BARRENS = "end_barrens"
    """End Barrens."""

    def display_name(self) -> str:
        return _biomeid_display[self]


# noinspection SpellCheckingInspection,GrazieInspection
_biomeid_display = {BiomeId.THE_VOID: "The Void", BiomeId.PLAINS: "Plains",
                    BiomeId.SUNFLOWER_PLAINS: "Sunflower Plains", BiomeId.SNOWY_PLAINS: "Snowy Plains",
                    BiomeId.ICE_SPIKES: "Ice Spikes", BiomeId.DESERT: "Desert", BiomeId.SWAMP: "Swamp",
                    BiomeId.MANGROVE_SWAMP: "Mangrove Swamp", BiomeId.FOREST: "Forest",
                    BiomeId.FLOWER_FOREST: "Flower Forest", BiomeId.BIRCH_FOREST: "Birch Forest",
                    BiomeId.DARK_FOREST: "Dark Forest", BiomeId.OLD_GROWTH_BIRCH_FOREST: "Old Growth Birch Forest",
                    BiomeId.OLD_GROWTH_PINE_TAIGA: "Old Growth Pine Taiga",
                    BiomeId.OLD_GROWTH_SPRUCE_TAIGA: "Old Growth Spruce Taiga", BiomeId.TAIGA: "Taiga",
                    BiomeId.SNOWY_TAIGA: "Snowy Taiga", BiomeId.SAVANNA: "Savanna",
                    BiomeId.SAVANNA_PLATEAU: "Savanna Plateau", BiomeId.WINDSWEPT_HILLS: "Windswept Hills",
                    BiomeId.WINDSWEPT_GRAVELLY_HILLS: "Windswept Gravelly Hills",
                    BiomeId.WINDSWEPT_FOREST: "Windswept Forest", BiomeId.WINDSWEPT_SAVANNA: "Windswept Savanna",
                    BiomeId.JUNGLE: "Jungle", BiomeId.SPARSE_JUNGLE: "Sparse Jungle",
                    BiomeId.BAMBOO_JUNGLE: "Bamboo Jungle", BiomeId.BADLANDS: "Badlands",
                    BiomeId.ERODED_BADLANDS: "Eroded Badlands", BiomeId.WOODED_BADLANDS: "Wooded Badlands",
                    BiomeId.MEADOW: "Meadow", BiomeId.CHERRY_GROVE: "Cherry Grove", BiomeId.GROVE: "Grove",
                    BiomeId.SNOWY_SLOPES: "Snowy Slopes", BiomeId.FROZEN_PEAKS: "Frozen Peaks",
                    BiomeId.JAGGED_PEAKS: "Jagged Peaks", BiomeId.STONY_PEAKS: "Stony Peaks", BiomeId.RIVER: "River",
                    BiomeId.FROZEN_RIVER: "Frozen River", BiomeId.BEACH: "Beach", BiomeId.SNOWY_BEACH: "Snowy Beach",
                    BiomeId.STONY_SHORE: "Stony Shore", BiomeId.WARM_OCEAN: "Warm Ocean",
                    BiomeId.LUKEWARM_OCEAN: "Lukewarm Ocean", BiomeId.DEEP_LUKEWARM_OCEAN: "Deep Lukewarm Ocean",
                    BiomeId.OCEAN: "Ocean", BiomeId.DEEP_OCEAN: "Deep Ocean", BiomeId.COLD_OCEAN: "Cold Ocean",
                    BiomeId.DEEP_COLD_OCEAN: "Deep Cold Ocean", BiomeId.FROZEN_OCEAN: "Frozen Ocean",
                    BiomeId.DEEP_FROZEN_OCEAN: "Deep Frozen Ocean", BiomeId.MUSHROOM_FIELDS: "Mushroom Fields",
                    BiomeId.DRIPSTONE_CAVES: "Dripstone Caves", BiomeId.LUSH_CAVES: "Lush Caves",
                    BiomeId.DEEP_DARK: "Deep Dark", BiomeId.NETHER_WASTES: "Nether Wastes",
                    BiomeId.WARPED_FOREST: "Warped Forest", BiomeId.CRIMSON_FOREST: "Crimson Forest",
                    BiomeId.SOUL_SAND_VALLEY: "Soul Sand Valley", BiomeId.BASALT_DELTAS: "Basalt Deltas",
                    BiomeId.THE_END: "The End", BiomeId.END_HIGHLANDS: "End Highlands",
                    BiomeId.END_MIDLANDS: "End Midlands", BiomeId.SMALL_END_ISLANDS: "Small End Islands",
                    BiomeId.END_BARRENS: "End Barrens"}


# noinspection SpellCheckingInspection,GrazieInspection
@enum.unique
class Effect(ValueEnum):
    SPEED = "speed"
    """Increases walking speed; higher levels make the affected entity faster and increases the player's field of view when affected."""
    SLOWNESS = "slowness"
    """Decreases walking speed; higher levels make the affected entity slower and decreases the player's field of view when affected."""
    HASTE = "haste"
    """Increases mining and attack speed, higher levels increase the player's mining and attack speed."""
    MINING_FATIGUE = "mining_fatigue"
    """Decreases mining and attack speed, higher levels decrease the player's mining and attack speed."""
    STRENGTH = "strength"
    """Increases melee damage, higher levels make the affected entity do more melee damage."""
    INSTANT_HEALTH = "instant_health"
    """Heals living entities, damages undead, higher levels heal more health and do more damage."""
    INSTANT_DAMAGE = "instant_damage"
    """Damages living entities, heals undead, higher levels do more damage and heal more health."""
    JUMP_BOOST = "jump_boost"
    """Increases jump height and reduces fall damage, higher levels make the affected entity jump higher and reduces more fall damage."""
    NAUSEA = "nausea"
    """Wobbles and warps the screen."""
    REGENERATION = "regeneration"
    """Regenerates health over time, higher levels make health regenerate quicker."""
    RESISTANCE = "resistance"
    """Reduces damage, higher levels reduce more damage."""
    FIRE_RESISTANCE = "fire_resistance"
    """Prevents the affected entity from taking damage due to Fire, lava and other sources of fire damage."""
    WATER_BREATHING = "water_breathing"
    """Prevents drowning and lets the affected entity breathe underwater."""
    INVISIBILITY = "invisibility"
    """Grants invisibility, making the affected entity invisible (but not the item they hold or the armor they wear), and reduces other mobs' detection range for the affected entity, higher levels reduce other mobs' detection range more."""
    BLINDNESS = "blindness"
    """Impairs vision and disables the ability to sprint and critical hit."""
    NIGHT_VISION = "night_vision"
    """Lets the player see well in darkness and underwater."""
    HUNGER = "hunger"
    """Increases food exhaustion, higher levels cause the player to starve quicker."""
    WEAKNESS = "weakness"
    """Decreases melee damage, higher levels decrease more melee damage."""
    POISON = "poison"
    """Inflicts damage over time (but can't kill), higher levels do more damage per second, doesn't affect undead."""
    WITHER = "wither"
    """Inflicts damage over time (can kill), higher levels do more damage per second."""
    HEALTH_BOOST = "health_boost"
    """Increases maximum health, higher levels give the affected entity more maximum health."""
    ABSORPTION = "absorption"
    """Adds damage absorption (additional hearts that can't be regenerated), higher levels give more absorption."""
    SATURATION = "saturation"
    """Restores hunger and saturation."""
    GLOWING = "glowing"
    """Outlines the affected entity (can be seen through blocks)."""
    LEVITATION = "levitation"
    """Floats the affected entity upward."""
    LUCK = "luck"
    """Can increase chances of high-quality and more loot, higher levels increase the chances of better loot."""
    BAD_LUCK = "unluck"
    """Can reduce chances of high-quality and more loot, higher levels reduce the chance of good loot."""
    SLOW_FALLING = "slow_falling"
    """Decreases falling speed and negates fall damage."""
    CONDUIT_POWER = "conduit_power"
    """Increases underwater visibility and mining speed, prevents drowning."""
    DOLPHINS_GRACE = "dolphins_grace"
    """Increases swimming speed (only obtainable from dolphins)."""
    BAD_OMEN = "bad_omen"
    """Causes an illager raid to start upon entering a village (only received from an Illager captain upon its death), higher levels cause a more difficult raid."""
    HERO_OF_THE_VILLAGE = "hero_of_the_village"
    """Gives discounts on trades with villagers, and makes villagers throw items at the player depending on their profession."""
    DARKNESS = "darkness"
    """Darkens the players screen."""

    def display_name(self) -> str:
        return _effect_display[self]

    def positive(self):
        return _effect_positive[self.value]

    def id(self):
        return _effect_ids[self.value]


# noinspection SpellCheckingInspection,GrazieInspection
_effect_positive = {'speed': True, 'slowness': False, 'haste': True, 'mining_fatigue': False, 'strength': True,
                    'instant_health': True, 'instant_damage': False, 'jump_boost': True, 'nausea': False,
                    'regeneration': True, 'resistance': True, 'fire_resistance': True, 'water_breathing': True,
                    'invisibility': True, 'blindness': False, 'night_vision': True, 'hunger': False, 'weakness': False,
                    'poison': False, 'wither': False, 'health_boost': True, 'absorption': True, 'saturation': True,
                    'glowing': None, 'levitation': False, 'luck': True, 'unluck': False, 'slow_falling': True,
                    'conduit_power': True, 'dolphins_grace': True, 'bad_omen': None, 'hero_of_the_village': True,
                    'darkness': False}

# noinspection SpellCheckingInspection,GrazieInspection
_effect_ids = {'speed': 1, 'slowness': 2, 'haste': 3, 'mining_fatigue': 4, 'strength': 5, 'instant_health': 6,
               'instant_damage': 7, 'jump_boost': 8, 'nausea': 9, 'regeneration': 10, 'resistance': 11,
               'fire_resistance': 12, 'water_breathing': 13, 'invisibility': 14, 'blindness': 15, 'night_vision': 16,
               'hunger': 17, 'weakness': 18, 'poison': 19, 'wither': 20, 'health_boost': 21, 'absorption': 22,
               'saturation': 23, 'glowing': 24, 'levitation': 25, 'luck': 26, 'unluck': 27, 'slow_falling': 28,
               'conduit_power': 29, 'dolphins_grace': 30, 'bad_omen': 31, 'hero_of_the_village': 32, 'darkness': 33}

# noinspection SpellCheckingInspection,GrazieInspection
_effect_display = {Effect.SPEED: "Speed", Effect.SLOWNESS: "Slowness", Effect.HASTE: "Haste",
                   Effect.MINING_FATIGUE: "Mining Fatigue", Effect.STRENGTH: "Strength",
                   Effect.INSTANT_HEALTH: "Instant Health", Effect.INSTANT_DAMAGE: "Instant Damage",
                   Effect.JUMP_BOOST: "Jump Boost", Effect.NAUSEA: "Nausea", Effect.REGENERATION: "Regeneration",
                   Effect.RESISTANCE: "Resistance", Effect.FIRE_RESISTANCE: "Fire Resistance",
                   Effect.WATER_BREATHING: "Water Breathing", Effect.INVISIBILITY: "Invisibility",
                   Effect.BLINDNESS: "Blindness", Effect.NIGHT_VISION: "Night Vision", Effect.HUNGER: "Hunger",
                   Effect.WEAKNESS: "Weakness", Effect.POISON: "Poison", Effect.WITHER: "Wither",
                   Effect.HEALTH_BOOST: "Health Boost", Effect.ABSORPTION: "Absorption",
                   Effect.SATURATION: "Saturation", Effect.GLOWING: "Glowing", Effect.LEVITATION: "Levitation",
                   Effect.LUCK: "Luck", Effect.BAD_LUCK: "Bad Luck", Effect.SLOW_FALLING: "Slow Falling",
                   Effect.CONDUIT_POWER: "Conduit Power", Effect.DOLPHINS_GRACE: "Dolphin's Grace",
                   Effect.BAD_OMEN: "Bad Omen", Effect.HERO_OF_THE_VILLAGE: "Hero of the Village",
                   Effect.DARKNESS: "Darkness"}


# noinspection SpellCheckingInspection,GrazieInspection
@enum.unique
class Enchantment(ValueEnum):
    AQUA_AFFINITY = "aqua_affinity"
    """Increases underwater mining speed."""
    BANE_OF_ARTHROPODS = "bane_of_arthropods"
    """Increases damage and applies Slowness IV to arthropod mobs (spiders, cave spiders, silverfish, endermites and bees)."""
    BLAST_PROTECTION = "blast_protection"
    """Reduces explosion damage and knockback."""
    CHANNELING = "channeling"
    """During thunderstorms, trident summons a lightning bolt on the target when hitting it."""
    CLEAVING = "cleaving"
    """Increases damage and shield stunning."""
    CURSE_OF_BINDING = "curse_of_binding"
    """Items cannot be removed from armor slots."""
    CURSE_OF_VANISHING = "curse_of_vanishing"
    """Item disappears on death."""
    DEPTH_STRIDER = "depth_strider"
    """Increases underwater movement speed."""
    EFFICIENCY = "efficiency"
    """Increases tool speed, as well as the chance for axes to disable shields."""
    FEATHER_FALLING = "feather_falling"
    """Reduces fall damage."""
    FIRE_ASPECT = "fire_aspect"
    """Sets target on fire."""
    FIRE_PROTECTION = "fire_protection"
    """Reduces fire damage and burn time.Mutually exclusive with other protections."""
    FLAME = "flame"
    """Arrows shot are ignited and deal fire damage to the target."""
    FORTUNE = "fortune"
    """Increases the amount of block drops."""
    FROST_WALKER = "frost_walker"
    """Allows the player to walk on water by freezing the water under their feet."""
    IMPALING = "impaling"
    """Increases damage against aquatic mobs. In Bedrock Edition, increases damage against mobs in water or rain."""
    INFINITY = "infinity"
    """Prevents consumption of arrows."""
    KNOCKBACK = "knockback"
    """Increases knockback."""
    LOOTING = "looting"
    """Increases mob loot."""
    LOYALTY = "loyalty"
    """Trident returns after being thrown."""
    LUCK_OF_THE_SEA = "luck_of_the_sea"
    """Increases rate of good loot (enchanting books, etc.)."""
    LURE = "lure"
    """Decreases time for bites."""
    MENDING = "mending"
    """Repairs the item using experience."""
    MULTISHOT = "multishot"
    """Fires 3 arrows at the same time."""
    PIERCING = "piercing"
    """Arrows pierce entities, allowing for arrows to pierce through stacks of mobs."""
    POWER = "power"
    """Increases arrow damage."""
    PROJECTILE_PROTECTION = "projectile_protection"
    """Reduces damage from projectiles."""
    PROTECTION = "protection"
    """Reduces generic damage."""
    PUNCH = "punch"
    """Increases arrow knockback."""
    QUICK_CHARGE = "quick_charge"
    """Decreases crossbow charging time."""
    RESPIRATION = "respiration"
    """Extends underwater breathing time."""
    RIPTIDE = "riptide"
    """Trident launches player with itself when thrown while in water or rain."""
    SHARPNESS = "sharpness"
    """Increases melee damage."""
    SILK_TOUCH = "silk_touch"
    """Mined blocks drop themselves."""
    SMITE = "smite"
    """Increases damage to the undead."""
    SOUL_SPEED = "soul_speed"
    """Increases movement speed on soul sand and soul soil."""
    SWEEPING_EDGE = "sweeping_edge"
    """Increases sweeping attack damage."""
    SWIFT_SNEAK = "swift_sneak"
    """Increases sneaking speed."""
    THORNS = "thorns"
    """Taking damage causes the attacker to also take damage."""
    UNBREAKING = "unbreaking"
    """Reduces durability damage."""

    def display_name(self) -> str:
        return _enchantment_display[self]

    def max_level(self):
        return _enchantment_maxes[self.value]


# noinspection SpellCheckingInspection,GrazieInspection
_enchantment_maxes = {'aqua_affinity': 1, 'bane_of_arthropods': 5, 'blast_protection': 4, 'channeling': 1,
                      'cleaving': 3, 'curse_of_binding': 1, 'curse_of_vanishing': 1, 'depth_strider': 3,
                      'efficiency': 5, 'feather_falling': 4, 'fire_aspect': 2, 'fire_protection': 4, 'flame': 1,
                      'fortune': 3, 'frost_walker': 2, 'impaling': 5, 'infinity': 1, 'knockback': 2, 'looting': 3,
                      'loyalty': 3, 'luck_of_the_sea': 3, 'lure': 3, 'mending': 1, 'multishot': 1, 'piercing': 4,
                      'power': 5, 'projectile_protection': 4, 'protection': 4, 'punch': 2, 'quick_charge': 3,
                      'respiration': 3, 'riptide': 3, 'sharpness': 5, 'silk_touch': 1, 'smite': 5, 'soul_speed': 3,
                      'sweeping_edge': 3, 'swift_sneak': 3, 'thorns': 3, 'unbreaking': 3}

# noinspection SpellCheckingInspection,GrazieInspection
_enchantment_display = {Enchantment.AQUA_AFFINITY: "Aqua Affinity",
                        Enchantment.BANE_OF_ARTHROPODS: "Bane of Arthropods",
                        Enchantment.BLAST_PROTECTION: "Blast Protection", Enchantment.CHANNELING: "Channeling",
                        Enchantment.CLEAVING: "Cleaving", Enchantment.CURSE_OF_BINDING: "Curse of Binding",
                        Enchantment.CURSE_OF_VANISHING: "Curse of Vanishing",
                        Enchantment.DEPTH_STRIDER: "Depth Strider", Enchantment.EFFICIENCY: "Efficiency",
                        Enchantment.FEATHER_FALLING: "Feather Falling", Enchantment.FIRE_ASPECT: "Fire Aspect",
                        Enchantment.FIRE_PROTECTION: "Fire Protection", Enchantment.FLAME: "Flame",
                        Enchantment.FORTUNE: "Fortune", Enchantment.FROST_WALKER: "Frost Walker",
                        Enchantment.IMPALING: "Impaling", Enchantment.INFINITY: "Infinity",
                        Enchantment.KNOCKBACK: "Knockback", Enchantment.LOOTING: "Looting",
                        Enchantment.LOYALTY: "Loyalty", Enchantment.LUCK_OF_THE_SEA: "Luck of the Sea",
                        Enchantment.LURE: "Lure", Enchantment.MENDING: "Mending", Enchantment.MULTISHOT: "Multishot",
                        Enchantment.PIERCING: "Piercing", Enchantment.POWER: "Power",
                        Enchantment.PROJECTILE_PROTECTION: "Projectile Protection",
                        Enchantment.PROTECTION: "Protection", Enchantment.PUNCH: "Punch",
                        Enchantment.QUICK_CHARGE: "Quick Charge", Enchantment.RESPIRATION: "Respiration",
                        Enchantment.RIPTIDE: "Riptide", Enchantment.SHARPNESS: "Sharpness",
                        Enchantment.SILK_TOUCH: "Silk Touch", Enchantment.SMITE: "Smite",
                        Enchantment.SOUL_SPEED: "Soul Speed", Enchantment.SWEEPING_EDGE: "Sweeping Edge",
                        Enchantment.SWIFT_SNEAK: "Swift Sneak", Enchantment.THORNS: "Thorns",
                        Enchantment.UNBREAKING: "Unbreaking"}


# noinspection SpellCheckingInspection,GrazieInspection
@enum.unique
class GameRule(ValueEnum):
    ANNOUNCE_ADVANCEMENTS = "announceAdvancements"
    """Whether advancements should be announced in chat."""
    BLOCK_EXPLOSION_DROP_DECAY = "blockExplosionDropDecay"
    """Whether block loot is dropped by all blocks (false) or randomly (true) depending on how far the block is from the center of a block explosion (e.g. clicking a bed in dimensions other than the Overworld)."""
    COMMAND_BLOCK_OUTPUT = "commandBlockOutput"
    """Whether command blocks should notify admins when they perform commands."""
    COMMAND_MODIFICATION_BLOCK_LIMIT = "commandModificationBlockLimit"
    """Controls the maximum number of blocks changed when using /clone, /fill, or /fillbiome."""
    DISABLE_ELYTRA_MOVEMENT_CHECK = "disableElytraMovementCheck"
    """Whether the server should skip checking player speed when the player is wearing elytra. Often helps with jittering due to lag in multiplayer."""
    DISABLE_RAIDS = "disableRaids"
    """Whether raids are disabled."""
    DO_DAYLIGHT_CYCLE = "doDaylightCycle"
    """Whether the daylight cycle and moon phases progress."""
    DO_ENTITY_DROPS = "doEntityDrops"
    """Whether entities that are not mobs should have drops."""
    DO_FIRE_TICK = "doFireTick"
    """Whether fire should spread and naturally extinguish."""
    DO_INSOMNIA = "doInsomnia"
    """Whether phantoms can spawn in the nighttime."""
    DO_IMMEDIATE_RESPAWN = "doImmediateRespawn"
    """Players respawn immediately without showing the death screen."""
    DO_LIMITED_CRAFTING = "doLimitedCrafting"
    """Whether players can craft only those recipes that they have unlocked."""
    DO_MOB_LOOT = "doMobLoot"
    """Whether mobs should drop items and experience orbs."""
    DO_MOB_SPAWNING = "doMobSpawning"
    """Whether mobs should naturally spawn. Does not affect monster spawners."""
    DO_PATROL_SPAWNING = "doPatrolSpawning"
    """Whether patrols can spawn."""
    DO_TILE_DROPS = "doTileDrops"
    """Whether blocks should have drops."""
    DO_TRADER_SPAWNING = "doTraderSpawning"
    """Whether wandering traders can spawn."""
    DO_VINES_SPREAD = "doVinesSpread"
    """Whether vines can spread to other blocks. Cave vines, weeping vines, and twisting vines are not affected."""
    DO_WEATHER_CYCLE = "doWeatherCycle"
    """Whether the weather can change naturally. The /weather command can still change weather."""
    DO_WARDEN_SPAWNING = "doWardenSpawning"
    """Whether wardens can spawn."""
    DROWNING_DAMAGE = "drowningDamage"
    """Whether the player should take damage when drowning."""
    ENDER_PEARLS_VANISH_ON_DEATH = "enderPearlsVanishOnDeath"
    """Controls whether thrown ender pearls vanish when the player dies."""
    FALL_DAMAGE = "fallDamage"
    """Whether the player should take fall damage."""
    FIRE_DAMAGE = "fireDamage"
    """Whether the player should take damage in fire, lava, campfires, or on magma blocks."""
    FORGIVE_DEAD_PLAYERS = "forgiveDeadPlayers"
    """Makes angered neutral mobs stop being angry when the targeted player dies nearby."""
    FREEZE_DAMAGE = "freezeDamage"
    """Whether the player should take damage when inside powder snow."""
    GLOBAL_SOUND_EVENTS = "globalSoundEvents"
    """Whether certain sound events are heard by all players regardless of location."""
    KEEP_INVENTORY = "keepInventory"
    """Whether the player should keep items and experience in their inventory after death."""
    LAVA_SOURCE_CONVERSION = "lavaSourceConversion"
    """Whether new sources of lava are allowed to form."""
    LOG_ADMIN_COMMANDS = "logAdminCommands"
    """Whether to log admin commands to server log."""
    MAX_COMMAND_CHAIN_LENGTH = "maxCommandChainLength"
    """The maximum length of a chain of commands that can be executed during one tick. Applies to command blocks and functions."""
    MAX_ENTITY_CRAMMING = "maxEntityCramming"
    """The maximum number of pushable entities a mob or player can push, before taking 6 entity cramming damage per half-second. Setting to 0 or lower disables the rule. Damage affects Survival-mode or Adventure-mode players, and all mobs but bats. Pushable entities include non-Spectator-mode players, any mob except bats, as well as boats and minecarts."""
    MOB_EXPLOSION_DROP_DECAY = "mobExplosionDropDecay"
    """Whether block loot is dropped by all blocks (false) or randomly (true) depending on how far the block is from the center of a mob explosion (e.g. Creeper explosion)."""
    MOB_GRIEFING = "mobGriefing"
    """Whether creepers, zombies, endermen, ghasts, withers, ender dragons, rabbits, sheep, villagers, silverfish, snow golems, and end crystals."""
    NATURAL_REGENERATION = "naturalRegeneration"
    """Whether the player can regenerate health naturally if their hunger is full enough (doesn't affect external healing, such as golden apples, the Regeneration effect, etc.)."""
    PLAYERS_SLEEPING_PERCENTAGE = "playersSleepingPercentage"
    """What percentage of players in the Overworld must sleep to skip the night. A percentage value of 0 or less will allow the night to be skipped by just 1 player, and a percentage value more than 100 will prevent players from ever skipping the night."""
    RANDOM_TICK_SPEED = "randomTickSpeed"
    """How often a random block tick occurs (such as plant growth, leaf decay, etc.) per chunk section per game tick. 0 and negative values disables random ticks, higher numbers increase random ticks. Setting to a high integer results in high speeds of decay and growth. Numbers over 4096 make plant growth or leaf decay instantaneous."""
    REDUCED_DEBUG_INFO = "reducedDebugInfo"
    """Whether the debug screen shows all or reduced information; and whether the effects of F3 + B (entity hitboxes) and F3 + G (chunk boundaries) are shown."""
    SEND_COMMAND_FEEDBACK = "sendCommandFeedback"
    """Whether the feedback from commands executed by a player should show up in chat. Also affects the default behavior of whether command blocks store their output text."""
    SHOW_DEATH_MESSAGES = "showDeathMessages"
    """Whether death messages are put into chat when a player dies. Also affects whether a message is sent to the pet's owner when the pet dies."""
    SNOW_ACCUMULATION_HEIGHT = "snowAccumulationHeight"
    """The maximum number of snow layers that can be accumulated on each block."""
    SPAWN_RADIUS = "spawnRadius"
    """The number of blocks outward from the world spawn coordinates that a player spawns in when first joining a server or when dying without a personal spawnpoint. Has no effect on servers where the default game mode is Adventure."""
    SPECTATORS_GENERATE_CHUNKS = "spectatorsGenerateChunks"
    """Whether players in Spectator mode can generate chunks."""
    TNT_EXPLOSION_DROP_DECAY = "tntExplosionDropDecay"
    """Whether block loot is dropped by all blocks (false) or randomly (true) depending on how far the block is from the center of a TNT explosion."""
    UNIVERSAL_ANGER = "universalAnger"
    """Makes angered neutral mobs attack any nearby player, not just the player that angered them. Works best if forgiveDeadPlayers is disabled."""
    WATER_SOURCE_CONVERSION = "waterSourceConversion"
    """Whether new sources of water are allowed to form."""

    def display_name(self) -> str:
        return _gamerule_display[self]

    def rule_type(self):
        return _gamerule_types[self.value]


# noinspection SpellCheckingInspection,GrazieInspection
_gamerule_types = {'announceAdvancements': 'bool', 'blockExplosionDropDecay': 'bool', 'commandBlockOutput': 'bool',
                   'commandModificationBlockLimit': 'int', 'disableElytraMovementCheck': 'bool', 'disableRaids': 'bool',
                   'doDaylightCycle': 'bool', 'doEntityDrops': 'bool', 'doFireTick': 'bool', 'doInsomnia': 'bool',
                   'doImmediateRespawn': 'bool', 'doLimitedCrafting': 'bool', 'doMobLoot': 'bool',
                   'doMobSpawning': 'bool', 'doPatrolSpawning': 'bool', 'doTileDrops': 'bool',
                   'doTraderSpawning': 'bool', 'doVinesSpread': 'bool', 'doWeatherCycle': 'bool',
                   'doWardenSpawning': 'bool', 'drowningDamage': 'bool', 'enderPearlsVanishOnDeath': 'bool',
                   'fallDamage': 'bool', 'fireDamage': 'bool', 'forgiveDeadPlayers': 'bool', 'freezeDamage': 'bool',
                   'globalSoundEvents': 'bool', 'keepInventory': 'bool', 'lavaSourceConversion': 'bool',
                   'logAdminCommands': 'bool', 'maxCommandChainLength': 'int', 'maxEntityCramming': 'int',
                   'mobExplosionDropDecay': 'bool', 'mobGriefing': 'bool', 'naturalRegeneration': 'bool',
                   'playersSleepingPercentage': 'int', 'randomTickSpeed': 'int', 'reducedDebugInfo': 'bool',
                   'sendCommandFeedback': 'bool', 'showDeathMessages': 'bool', 'snowAccumulationHeight': 'int',
                   'spawnRadius': 'int', 'spectatorsGenerateChunks': 'bool', 'tntExplosionDropDecay': 'bool',
                   'universalAnger': 'bool', 'waterSourceConversion': 'bool'}

# noinspection SpellCheckingInspection,GrazieInspection
_gamerule_display = {GameRule.ANNOUNCE_ADVANCEMENTS: "announce Advancements",
                     GameRule.BLOCK_EXPLOSION_DROP_DECAY: "block Explosion Drop Decay",
                     GameRule.COMMAND_BLOCK_OUTPUT: "command Block Output",
                     GameRule.COMMAND_MODIFICATION_BLOCK_LIMIT: "command Modification Block Limit",
                     GameRule.DISABLE_ELYTRA_MOVEMENT_CHECK: "disable Elytra Movement Check",
                     GameRule.DISABLE_RAIDS: "disable Raids", GameRule.DO_DAYLIGHT_CYCLE: "do Daylight Cycle",
                     GameRule.DO_ENTITY_DROPS: "do Entity Drops", GameRule.DO_FIRE_TICK: "do Fire Tick",
                     GameRule.DO_INSOMNIA: "do Insomnia", GameRule.DO_IMMEDIATE_RESPAWN: "do Immediate Respawn",
                     GameRule.DO_LIMITED_CRAFTING: "do Limited Crafting", GameRule.DO_MOB_LOOT: "do Mob Loot",
                     GameRule.DO_MOB_SPAWNING: "do Mob Spawning", GameRule.DO_PATROL_SPAWNING: "do Patrol Spawning",
                     GameRule.DO_TILE_DROPS: "do Tile Drops", GameRule.DO_TRADER_SPAWNING: "do Trader Spawning",
                     GameRule.DO_VINES_SPREAD: "do Vines Spread", GameRule.DO_WEATHER_CYCLE: "do Weather Cycle",
                     GameRule.DO_WARDEN_SPAWNING: "do Warden Spawning", GameRule.DROWNING_DAMAGE: "drowning Damage",
                     GameRule.ENDER_PEARLS_VANISH_ON_DEATH: "ender Pearls Vanish On Death",
                     GameRule.FALL_DAMAGE: "fall Damage", GameRule.FIRE_DAMAGE: "fire Damage",
                     GameRule.FORGIVE_DEAD_PLAYERS: "forgive Dead Players", GameRule.FREEZE_DAMAGE: "freeze Damage",
                     GameRule.GLOBAL_SOUND_EVENTS: "global Sound Events", GameRule.KEEP_INVENTORY: "keep Inventory",
                     GameRule.LAVA_SOURCE_CONVERSION: "lava Source Conversion",
                     GameRule.LOG_ADMIN_COMMANDS: "log Admin Commands",
                     GameRule.MAX_COMMAND_CHAIN_LENGTH: "max Command Chain Length",
                     GameRule.MAX_ENTITY_CRAMMING: "max Entity Cramming",
                     GameRule.MOB_EXPLOSION_DROP_DECAY: "mob Explosion Drop Decay",
                     GameRule.MOB_GRIEFING: "mob Griefing", GameRule.NATURAL_REGENERATION: "natural Regeneration",
                     GameRule.PLAYERS_SLEEPING_PERCENTAGE: "players Sleeping Percentage",
                     GameRule.RANDOM_TICK_SPEED: "random Tick Speed", GameRule.REDUCED_DEBUG_INFO: "reduced Debug Info",
                     GameRule.SEND_COMMAND_FEEDBACK: "send Command Feedback",
                     GameRule.SHOW_DEATH_MESSAGES: "show Death Messages",
                     GameRule.SNOW_ACCUMULATION_HEIGHT: "snow Accumulation Height",
                     GameRule.SPAWN_RADIUS: "spawn Radius",
                     GameRule.SPECTATORS_GENERATE_CHUNKS: "spectators Generate Chunks",
                     GameRule.TNT_EXPLOSION_DROP_DECAY: "tnt Explosion Drop Decay",
                     GameRule.UNIVERSAL_ANGER: "universal Anger",
                     GameRule.WATER_SOURCE_CONVERSION: "water Source Conversion"}


# noinspection SpellCheckingInspection,GrazieInspection
@enum.unique
class ScoreCriteria(ValueEnum):
    DUMMY = "dummy"
    """Score is only changed by commands, and not by game events such as death. This is useful for event flags, state mappings, currencies,..."""
    TRIGGER = "trigger"
    """Score is only changed by commands, and not by game events such as death. The /trigger command can be used by a player to set or increment/decrement their own score in an objective with this criterion. The /trigger command fails if the objective has not been "enabled" for the player using it, and the objective is disabled for the player after using the /trigger command on it. Note that the /trigger command can be used by ordinary players even if Cheats are off and they are not an Operator. This is useful for player input via /tellraw interfaces."""
    DEATH_COUNT = "deathCount"
    """Score increments automatically for a player when they die."""
    PLAYER_KILL_COUNT = "playerKillCount"
    """Score increments automatically for a player when they kill another player."""
    TOTAL_KILL_COUNT = "totalKillCount"
    """Score increments automatically for a player when they kill another player or a mob."""
    HEALTH = "health"
    """Ranges from 0 to 20 on a normal player; represents the amount of half-hearts the player has. May appear as 0 for players before their health has changed for the first time. Extra hearts and absorption hearts also count to the health score, meaning that with Attributes/Modifiers or the Health Boost or Absorption status effects, health can far surpass 20."""
    XP = "xp"
    """Matches the total amount of experience the player has collected since their last death (or in other words, their score)."""
    LEVEL = "level"
    """Matches the current experience level of the player."""
    FOOD = "food"
    """Ranges from 0 to 20; represents the amount of hunger points the player has. May appear as 0 for players before their foodLevel has changed for the first time."""
    AIR = "air"
    """Ranges from 0 to 300; represents the amount of air the player has left from swimming under water, matches the air nbt tag of the player."""
    ARMOR = "armor"
    """Ranges from 0 to 20; represents the amount of armor points the player has. May appear as 0 for players before their armor has changed for the first time."""

    def display_name(self) -> str:
        return _scorecriteria_display[self]


# noinspection SpellCheckingInspection,GrazieInspection
_scorecriteria_display = {ScoreCriteria.DUMMY: "dummy", ScoreCriteria.TRIGGER: "trigger",
                          ScoreCriteria.DEATH_COUNT: "death Count",
                          ScoreCriteria.PLAYER_KILL_COUNT: "player Kill Count",
                          ScoreCriteria.TOTAL_KILL_COUNT: "total Kill Count", ScoreCriteria.HEALTH: "health",
                          ScoreCriteria.XP: "xp", ScoreCriteria.LEVEL: "level", ScoreCriteria.FOOD: "food",
                          ScoreCriteria.AIR: "air", ScoreCriteria.ARMOR: "armor"}


# noinspection SpellCheckingInspection,GrazieInspection
@enum.unique
class Particle(ValueEnum):
    AMBIENT_ENTITY_EFFECT = "ambient_entity_effect"
    """Beacon effects."""
    ANGRY_VILLAGER = "angry_villager"
    """Attacking a villager in a village; when villagers can't breed because there aren't enough beds nearby or when a panda is attacked by a player on the village."""
    ASH = "ash"
    """Naturally generated in soul sand valley biome environment."""
    BLOCK = "block"
    """Breaking blocks, sprinting, iron golems walking."""
    BLOCK_MARKER = "block_marker"
    """Barriers and light when their corresponding item is held."""
    BUBBLE = "bubble"
    """Entities in water, guardian laser beams, fishing."""
    BUBBLE_COLUMN_UP = "bubble_column_up"
    """Upward bubble columns made by soul sand under water."""
    BUBBLE_POP = "bubble_pop"
    """Unused."""
    CAMPFIRE_COSY_SMOKE = "campfire_cosy_smoke"
    """Smoke produced by campfires and soul campfires."""
    CAMPFIRE_SIGNAL_SMOKE = "campfire_signal_smoke"
    """Smoke produced by campfires and soul campfires when above a hay bale."""
    CHERRY_LEAVES = "cherry_leaves"
    """Falling petals from the cherry leaves."""
    CLOUD = "cloud"
    """After jumping into water while on fire in Bedrock Edition or an entity dies in Java Edition."""
    COMPOSTER = "composter"
    """Filling a composter."""
    CRIMSON_SPORE = "crimson_spore"
    """A crimson particle generated in crimson forest biome environment."""
    CRIT = "crit"
    """Critical hits, fully charged bow shots, crossbows, evoker fangs."""
    CURRENT_DOWN = "current_down"
    """Bubble column whirlpools made by magma blocks underwater."""
    DAMAGE_INDICATOR = "damage_indicator"
    """From mobs and players when hurt by a melee attack."""
    DOLPHIN = "dolphin"
    """Trails behind swimming dolphins."""
    DRAGON_BREATH = "dragon_breath"
    """An ender dragon's breath and dragon fireballs."""
    DRIPPING_DRIPSTONE_LAVA = "dripping_dripstone_lava"
    """Dripping lava from the pointed dripstone."""
    DRIPPING_DRIPSTONE_WATER = "dripping_dripstone_water"
    """Dripping water from the pointed dripstone."""
    DRIPPING_HONEY = "dripping_honey"
    """Dripping honey through blocks that haven't dripped down yet."""
    DRIPPING_LAVA = "dripping_lava"
    """Dripping lava through blocks that haven't dripped down yet."""
    DRIPPING_OBSIDIAN_TEAR = "dripping_obsidian_tear"
    """Dripping crying obsidian's particles through blocks that haven't dripped down yet."""
    DRIPPING_WATER = "dripping_water"
    """Dripping water through blocks, wet sponges, leaves when raining that haven't dripped down yet."""
    DUST = "dust"
    """Redstone ore, powered redstone dust, redstone torches, powered redstone repeaters."""
    DUST_COLOR_TRANSITION = "dust_color_transition"
    """Sculk sensor gets triggered."""
    EFFECT = "effect"
    """Splash potions, lingering potions, bottles o' enchanting, evokers."""
    ELDER_GUARDIAN = "elder_guardian"
    """Elder guardians."""
    ELECTRIC_SPARK = "electric_spark"
    """Appears when a lightning bolt hits copper blocks."""
    ENCHANT = "enchant"
    """From bookshelves near an enchanting table."""
    ENCHANTED_HIT = "enchanted_hit"
    """Attacking with a sword or axe enchanted with Sharpness, Smite, or Bane of Arthropods."""
    END_ROD = "end_rod"
    """End rods, shulker bullets."""
    ENTITY_EFFECT = "entity_effect"
    """Status effects, lingering potions, tipped arrows, trading, withered armor (linger potion particles decrease when the "minimal" particle setting is used)."""
    EXPLOSION = "explosion"
    """Explosions, ghast fireballs, wither skulls, ender dragon death, shearing mooshrooms."""
    EXPLOSION_EMITTER = "explosion_emitter"
    """Explosions, ender dragon death."""
    FALLING_DRIPSTONE_LAVA = "falling_dripstone_lava"
    """Falling lava particles from the pointed dripstone."""
    FALLING_DRIPSTONE_WATER = "falling_dripstone_water"
    """Falling water particles from the pointed dripstone."""
    FALLING_DUST = "falling_dust"
    """Floating sand, gravel, concrete powder, and anvils."""
    FALLING_HONEY = "falling_honey"
    """Dripping honey through blocks that is dripping down in air."""
    FALLING_LAVA = "falling_lava"
    """Dripping lava through blocks that is dripping down in air."""
    FALLING_NECTAR = "falling_nectar"
    """Nectar on the pollen-loaded bees."""
    FALLING_OBSIDIAN_TEAR = "falling_obsidian_tear"
    """Dripping crying obsidian's particles through blocks that is dripping down in air and has fallen to the ground."""
    FALLING_SPORE_BLOSSOM = "falling_spore_blossom"
    """Dripping green particle from the spore blossom."""
    FALLING_WATER = "falling_water"
    """Dripping water through blocks that is dripping down in air and has fallen to the ground."""
    FIREWORK = "firework"
    """Firework rocket trail and explosion (trail is not shown when the "minimal" particle setting is used), when dolphins track shipwrecks and underwater ruins."""
    FISHING = "fishing"
    """Fishing."""
    FLAME = "flame"
    """Torches, furnaces, magma cubes, spawners."""
    FLASH = "flash"
    """Flash light when firework rocket explodes."""
    GLOW = "glow"
    """Glow squid."""
    GLOW_SQUID_INK = "glow_squid_ink"
    """Glow squid getting hurt."""
    HAPPY_VILLAGER = "happy_villager"
    """Applying bone meal to a crop, trading with villagers, feeding baby animals, walking or jumping on turtle eggs."""
    HEART = "heart"
    """Breeding and taming animals."""
    INSTANT_EFFECT = "instant_effect"
    """Instant health/damage splash and lingering potions, spectral arrows."""
    ITEM = "item"
    """Eating, thrown eggs, splash potions, eyes of ender, breaking tools."""
    ITEM_SLIME = "item_slime"
    """Jumping slimes."""
    ITEM_SNOWBALL = "item_snowball"
    """Thrown snowballs, creating withers, creating iron golems."""
    LANDING_HONEY = "landing_honey"
    """Dripping honey through blocks that has fallen to the ground."""
    LANDING_LAVA = "landing_lava"
    """Dripping lava through blocks that has fallen to the ground."""
    LANDING_OBSIDIAN_TEAR = "landing_obsidian_tear"
    """Dripping crying obsidian's particles through blocks that has fallen to the ground."""
    LARGE_SMOKE = "large_smoke"
    """Fire, minecart with furnace, blazes, water flowing into lava, lava flowing into water."""
    LAVA = "lava"
    """Lava bubble."""
    MYCELIUM = "mycelium"
    """Mycelium blocks."""
    NAUTILUS = "nautilus"
    """Activated conduits."""
    NOTE = "note"
    """Emitted from note blocks and jukeboxes."""
    POOF = "poof"
    """Explosions, death of mobs, mobs spawned from a spawner, silverfish infesting blocks."""
    PORTAL = "portal"
    """Nether portals, endermen, endermites, ender pearls, eyes of ender, ender chests, dragon eggs, teleporting from eating chorus fruits, end gateway portals."""
    RAIN = "rain"
    """Rain splashes on the ground."""
    SCRAPE = "scrape"
    """Scraping oxidation off a copper block with an axe."""
    SCULK_CHARGE = "sculk_charge"
    """Shown as sculk spreads through other blocks."""
    SCULK_CHARGE_POP = "sculk_charge_pop"
    """Sculk charge ends by popping."""
    SCULK_SOUL = "sculk_soul"
    """When a mob dies near a sculk catalyst these particles are shown."""
    SHRIEK = "shriek"
    """Shown when a sculk shrieker triggers."""
    SMOKE = "smoke"
    """Torches, primed TNT, droppers, dispensers, end portals, brewing stands, spawners, furnaces, ghast fireballs, wither skulls, taming, withers, lava (when raining), placing an eye of ender in an end portal frame, redstone torches burning out, food items on campfire."""
    SNEEZE = "sneeze"
    """Baby pandas sneezing."""
    SNOWFLAKE = "snowflake"
    """Appears when sinking in powder snow."""
    SONIC_BOOM = "sonic_boom"
    """Wardens casting sonic boom."""
    SOUL = "soul"
    """Appears when walking on soul sand or soul soil with the Soul Speed Enchantment, when a mob dies near a sculk catalyst."""
    SOUL_FIRE_FLAME = "soul_fire_flame"
    """Appears on top of soul torches as a flame."""
    SPIT = "spit"
    """Llamas spitting at a player or mob."""
    SPORE_BLOSSOM_AIR = "spore_blossom_air"
    """Emits around a spore blossom."""
    SPLASH = "splash"
    """Entities in water, wolves shaking off after swimming, boats."""
    SQUID_INK = "squid_ink"
    """Produced by squid when attacked."""
    SWEEP_ATTACK = "sweep_attack"
    """A sword's sweep attack."""
    TOTEM_OF_UNDYING = "totem_of_undying"
    """Activated totem of undying."""
    UNDERWATER = "underwater"
    """Seen while underwater."""
    VIBRATION = "vibration"
    """Sculk sensor gets triggered."""
    WARPED_SPORE = "warped_spore"
    """A warped particle generated in warped forest biome environment."""
    WAX_OFF = "wax_off"
    """Appears when removing wax from a copper block."""
    WAX_ON = "wax_on"
    """Appears when waxing a copper block with honeycomb."""
    WHITE_ASH = "white_ash"
    """Naturally generated in basalt deltas biome environment."""
    WITCH = "witch"
    """Witches."""

    def display_name(self) -> str:
        return _particle_display[self]


# noinspection SpellCheckingInspection,GrazieInspection
_particle_display = {Particle.AMBIENT_ENTITY_EFFECT: "Ambient Entity Effect", Particle.ANGRY_VILLAGER: "Angry Villager",
                     Particle.ASH: "Ash", Particle.BLOCK: "Block", Particle.BLOCK_MARKER: "Block Marker",
                     Particle.BUBBLE: "Bubble", Particle.BUBBLE_COLUMN_UP: "Bubble Column Up",
                     Particle.BUBBLE_POP: "Bubble Pop", Particle.CAMPFIRE_COSY_SMOKE: "Campfire Cosy Smoke",
                     Particle.CAMPFIRE_SIGNAL_SMOKE: "Campfire Signal Smoke", Particle.CHERRY_LEAVES: "Cherry Leaves",
                     Particle.CLOUD: "Cloud", Particle.COMPOSTER: "Composter", Particle.CRIMSON_SPORE: "Crimson Spore",
                     Particle.CRIT: "Crit", Particle.CURRENT_DOWN: "Current Down",
                     Particle.DAMAGE_INDICATOR: "Damage Indicator", Particle.DOLPHIN: "Dolphin",
                     Particle.DRAGON_BREATH: "Dragon Breath",
                     Particle.DRIPPING_DRIPSTONE_LAVA: "Dripping Dripstone Lava",
                     Particle.DRIPPING_DRIPSTONE_WATER: "Dripping Dripstone Water",
                     Particle.DRIPPING_HONEY: "Dripping Honey", Particle.DRIPPING_LAVA: "Dripping Lava",
                     Particle.DRIPPING_OBSIDIAN_TEAR: "Dripping Obsidian Tear",
                     Particle.DRIPPING_WATER: "Dripping Water", Particle.DUST: "Dust",
                     Particle.DUST_COLOR_TRANSITION: "Dust Color Transition", Particle.EFFECT: "Effect",
                     Particle.ELDER_GUARDIAN: "Elder Guardian", Particle.ELECTRIC_SPARK: "Electric Spark",
                     Particle.ENCHANT: "Enchant", Particle.ENCHANTED_HIT: "Enchanted Hit", Particle.END_ROD: "End Rod",
                     Particle.ENTITY_EFFECT: "Entity Effect", Particle.EXPLOSION: "Explosion",
                     Particle.EXPLOSION_EMITTER: "Explosion Emitter",
                     Particle.FALLING_DRIPSTONE_LAVA: "Falling Dripstone Lava",
                     Particle.FALLING_DRIPSTONE_WATER: "Falling Dripstone Water", Particle.FALLING_DUST: "Falling Dust",
                     Particle.FALLING_HONEY: "Falling Honey", Particle.FALLING_LAVA: "Falling Lava",
                     Particle.FALLING_NECTAR: "Falling Nectar", Particle.FALLING_OBSIDIAN_TEAR: "Falling Obsidian Tear",
                     Particle.FALLING_SPORE_BLOSSOM: "Falling Spore Blossom", Particle.FALLING_WATER: "Falling Water",
                     Particle.FIREWORK: "Firework", Particle.FISHING: "Fishing", Particle.FLAME: "Flame",
                     Particle.FLASH: "Flash", Particle.GLOW: "Glow", Particle.GLOW_SQUID_INK: "Glow Squid Ink",
                     Particle.HAPPY_VILLAGER: "Happy Villager", Particle.HEART: "Heart",
                     Particle.INSTANT_EFFECT: "Instant Effect", Particle.ITEM: "Item",
                     Particle.ITEM_SLIME: "Item Slime", Particle.ITEM_SNOWBALL: "Item Snowball",
                     Particle.LANDING_HONEY: "Landing Honey", Particle.LANDING_LAVA: "Landing Lava",
                     Particle.LANDING_OBSIDIAN_TEAR: "Landing Obsidian Tear", Particle.LARGE_SMOKE: "Large Smoke",
                     Particle.LAVA: "Lava", Particle.MYCELIUM: "Mycelium", Particle.NAUTILUS: "Nautilus",
                     Particle.NOTE: "Note", Particle.POOF: "Poof", Particle.PORTAL: "Portal", Particle.RAIN: "Rain",
                     Particle.SCRAPE: "Scrape", Particle.SCULK_CHARGE: "Sculk Charge",
                     Particle.SCULK_CHARGE_POP: "Sculk Charge Pop", Particle.SCULK_SOUL: "Sculk Soul",
                     Particle.SHRIEK: "Shriek", Particle.SMOKE: "Smoke", Particle.SNEEZE: "Sneeze",
                     Particle.SNOWFLAKE: "Snowflake", Particle.SONIC_BOOM: "Sonic Boom", Particle.SOUL: "Soul",
                     Particle.SOUL_FIRE_FLAME: "Soul Fire Flame", Particle.SPIT: "Spit",
                     Particle.SPORE_BLOSSOM_AIR: "Spore Blossom Air", Particle.SPLASH: "Splash",
                     Particle.SQUID_INK: "Squid Ink", Particle.SWEEP_ATTACK: "Sweep Attack",
                     Particle.TOTEM_OF_UNDYING: "Totem Of Undying", Particle.UNDERWATER: "Underwater",
                     Particle.VIBRATION: "Vibration", Particle.WARPED_SPORE: "Warped Spore",
                     Particle.WAX_OFF: "Wax Off", Particle.WAX_ON: "Wax On", Particle.WHITE_ASH: "White Ash",
                     Particle.WITCH: "Witch"}


# noinspection SpellCheckingInspection,GrazieInspection
@enum.unique
class PotterySherd(ValueEnum):
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

    def display_name(self) -> str:
        return _potterysherd_display[self]


# noinspection SpellCheckingInspection,GrazieInspection
_potterysherd_display = {PotterySherd.ANGLER_POTTERY_SHERD: "Angler Pottery Sherd",
                         PotterySherd.ARCHER_POTTERY_SHERD: "Archer Pottery Sherd",
                         PotterySherd.ARMS_UP_POTTERY_SHERD: "Arms Up Pottery Sherd",
                         PotterySherd.BLADE_POTTERY_SHERD: "Blade Pottery Sherd",
                         PotterySherd.BREWER_POTTERY_SHERD: "Brewer Pottery Sherd",
                         PotterySherd.BURN_POTTERY_SHERD: "Burn Pottery Sherd",
                         PotterySherd.DANGER_POTTERY_SHERD: "Danger Pottery Sherd",
                         PotterySherd.EXPLORER_POTTERY_SHERD: "Explorer Pottery Sherd",
                         PotterySherd.FRIEND_POTTERY_SHERD: "Friend Pottery Sherd",
                         PotterySherd.HEART_POTTERY_SHERD: "Heart Pottery Sherd",
                         PotterySherd.HEARTBREAK_POTTERY_SHERD: "Heartbreak Pottery Sherd",
                         PotterySherd.HOWL_POTTERY_SHERD: "Howl Pottery Sherd",
                         PotterySherd.MINER_POTTERY_SHERD: "Miner Pottery Sherd",
                         PotterySherd.MOURNER_POTTERY_SHERD: "Mourner Pottery Sherd",
                         PotterySherd.PLENTY_POTTERY_SHERD: "Plenty Pottery Sherd",
                         PotterySherd.PRIZE_POTTERY_SHERD: "Prize Pottery Sherd",
                         PotterySherd.SHEAF_POTTERY_SHERD: "Sheaf Pottery Sherd",
                         PotterySherd.SHELTER_POTTERY_SHERD: "Shelter Pottery Sherd",
                         PotterySherd.SKULL_POTTERY_SHERD: "Skull Pottery Sherd",
                         PotterySherd.SNORT_POTTERY_SHERD: "Snort Pottery Sherd"}
