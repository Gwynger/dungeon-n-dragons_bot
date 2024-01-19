import json
import logging
from dataclasses import dataclass


@dataclass
class BeastCard:
    id: str
    name: str
    url: str
    danger: str | None = None
    type: str | None = None


@dataclass
class SpellCard:
    title: str | None = None
    title_en: str | None = None
    link: str | None = None
    level: str | None = None
    school: str | None = None
    level_school: str | None = None
    casting_time: str | None = None
    c_range: str | None = None
    components: str | None = None
    duration: str | None = None
    classes: str | None = None
    archetypes: str | None = None
    source: str | None = None
    description: str | None = None
    id: int | None = None


@dataclass
class FeatCard:
    title: str | None = None
    link: str | None = None
    title_en: str | None = None
    requirements: str | None = None
    description: str | None = None
    source: str | None = None
    id: int | None = None


def load_beasts(path: str = 'beasts.json') -> dict:
    try:
        with open(path, encoding='utf-8') as f:
            data = json.load(f)

        beast_cards = {k: BeastCard(**v) for k, v in data.items()}
    except FileNotFoundError:
        logging.warning(f'Beasts upload failed! File {path} not found')
        beast_cards = {}
    return beast_cards


def load_spells(path: str = 'spells.json') -> dict:
    try:
        with open(path, encoding='utf-8') as f:
            data = json.load(f)

        spell_cards = {i + 1: SpellCard(**{k: v for k, v in card.items() if k != 'id'}, id=i + 1)
                       for i, card in enumerate(data.values())}
    except FileNotFoundError:
        logging.warning(f'Spells upload failed! File {path} not found')
        spell_cards = {}
    return spell_cards


def load_feats(path: str = 'feats.json') -> dict:
    try:
        with open(path, encoding='utf-8') as f:
            data = json.load(f)

        feat_cards = {i + 1: FeatCard(**{k: v for k, v in card.items() if k != 'id'}, id=i + 1)
                      for i, card in enumerate(data.values())}
    except FileNotFoundError:
        logging.warning(f'Feats upload failed! File {path} not found')
        feat_cards = {}
    return feat_cards


RACE_LINK = 'https://dnd.su/race/'
CLASS_LINK = 'https://dnd.su/class/'
STORY_LINK = 'https://dnd.su/backgrounds/'
CLASSES = {
    'Бард': '88-bard',
    'Варвар': '87-barbarian',
    'Воин': '91-fighter',
    'Волшебник': '105-wizard',
    'Друид': '90-druid',
    'Жрец': '89-cleric',
    'Изобретатель': '137-artificer',
    'Колдун': '104-warlock',
    'Монах': '93-monk',
    'Паладин': '94-paladin',
    'Плут': '99-rogue',
    'Следопыт': '97-ranger',
    'Чародей': '101-sorcerer',
    'Алхимик': '395-alchemist',
    'Альтернативный воин': '382-alternate_fighter',
    'Альтернативный монах': '391-alternate_monk',
    'Военачальник': '403-warlord',
    'Кровавый охотник': '195-blood_hunter',
    'Магус': '277-magus',
    'Мистик': '208-mystic',
    'Неупокоенная душа': '202-the_lingering_soul',
    'Савант': '401-savant',
    'Хранитель рун': '419-runekeeper',
    'Шаман': '389-shaman',
}
CLASSIC_CLASSES = {
    'Бард': '88-bard',
    'Варвар': '87-barbarian',
    'Воин': '91-fighter',
    'Волшебник': '105-wizard',
    'Друид': '90-druid',
    'Жрец': '89-cleric',
    'Изобретатель': '137-artificer',
    'Колдун': '104-warlock',
    'Монах': '93-monk',
    'Паладин': '94-paladin',
    'Плут': '99-rogue',
    'Следопыт': '97-ranger',
    'Чародей': '101-sorcerer',
}
RACES = {
    'Ааракокра': '92-aarakocra',
    'Аасимар': '161-aasimar',
    'Автогном': '214-autognome',
    'Астральный эльф': '213-astral_elf',
    'Багбир': '167-bugbear',
    'Ведалкен': '162-vedalken',
    'Верадн': '163-verdan',
    'Гибрид Симиков': '164-simic_hybrid',
    'Гит': '165-gith',
    'Гифф': '215-giff',
    'Гном': '83-gnome',
    'Гоблин': '166-goblin',
    'Голиаф': '103-goliath',
    'Грунг': '169-grung',
    'Дварф': '78-dwarf',
    'Дженази': '102-genasi',
    'Драконорожденный': '82-dragonborn',
    'Зайцегон': '207-harengon',
    'Калаштар': '171-kalashtar',
    'Кендер': '285-kender',
    'Кенку': '172-kenku',
    'Кентавр': '173-centaur',
    'Кобольд': '175-kobold',
    'Кованый': '174-warforged',
    'Леонинец': '176-leonin',
    'Локата': '178-locathah',
    'Локсодон': '177-loxodon',
    'Людоящер': '179-lizardfolk',
    'Минотавр': '181-minotaur',
    'Орк': '187-orc',
    'Плазмоид': '217-plasmoid',
    'Полуорк': '85-half_orc',
    'Полурослик': '80-halfling',
    'Полуэльф': '84-half_elf',
    'Сатир': '182-satyr',
    'Совлин': '206-owlin',
    'Табакси': '183-tabaxi',
    'Тифлинг': '86-tiefling',
    'Тортл': '184-tortle',
    'Три-крин': '218-thri_kreen',
    'Тритон': '188-triton',
    'Фейри': '204-fairy',
    'Фирболг': '185-firbolg',
    'Хадози': '216-hadozee',
    'Хобгоблин': '168-hobgoblin',
    'Чейнджлинг': '170-changeling',
    'Человек': '81-human',
    'Шифтер': '186-shifter',
    'Эльф': '79-elf',
    'Юань-ти': '189-yuan_ti_pureblood',
}
CLASSIC_RACES = {
    'Гном': '83-gnome',
    'Дварф': '78-dwarf',
    'Драконорожденный': '82-dragonborn',
    'Полуорк': '85-half_orc',
    'Полурослик': '80-halfling',
    'Полуэльф': '84-half_elf',
    'Тифлинг': '86-tiefling',
    'Человек': '81-human',
    'Эльф': '79-elf',
}
CLASSIC_STORIES = {
    'Артист': '757-entertainer',
    'Беспризорник': '758-urchin',
    'Благородный': '759-noble',
    'Гильдейский ремесленник': '760-guild_artisan',
    'Моряк': '761-sailor',
    'Мудрец': '762-sage',
    'Народный герой': '763-folk_hero',
    'Отшельник': '764-hermit',
    'Пират': '770-pirate',
    'Преступник': '765-criminal',
    'Прислужник': '766-acolyte',
    'Солдат': '767-soldier',
    'Чужеземец': '768-outlander',
    'Шарлатан': '769-charlatan',
}
STORIES = {
    'Артист': '757-entertainer',
    'Беспризорник': '758-urchin',
    'Благородный': '759-noble',
    'Гильдейский ремесленник': '760-guild_artisan',
    'Моряк': '761-sailor',
    'Мудрец': '762-sage',
    'Народный герой': '763-folk_hero',
    'Отшельник': '764-hermit',
    'Пират': '770-pirate',
    'Преступник': '765-criminal',
    'Прислужник': '766-acolyte',
    'Солдат': '767-soldier',
    'Чужеземец': '768-outlander',
    'Шарлатан': '769-charlatan',
    'Азартный игрок': '811-gambler',
    'Истец': '812-plaintiff',
    'Неудавшийся торговец': '810-failed_merchant',
    'Потомок знаменитого ава': '809-celebrity_adventurers_scion',
    'Стажер конкурента': '813-rival_intern',
    'Ухмылка': '817-grinner',
    'Атлант': '787-athlete',
    'Ветеран наёмник': '780-mercenary_veteran',
    'Городской охотник за го': '781-urban_bounty_hunter',
    'Городской стражник': '772-city_watch',
    'Дальний путешественник': '777-far_traveler',
    'Дворянин Глубоководья': '771-waterdhavian_noble',
    'Учёный-затворник': '774-cloistered_scholar',
    'Утгардтский соплеменник': '782-uthgardt_tribe_member',
    'Рыцарь ордена': '779-knight_of_the_order',
    'Придворный': '775-courtier',
    'Представитель фракции': '776-faction_agent',
    'Наследник': '778-inheritor',
    'Клановый ремесленник': '773-clan_crafter',
    'Преследуемый': '789-haunted_one',
    'Следователь': '790-investigator',
    'Маг Высшего Чародейства': '855-mage_of_high_sorcery',
    'Соламнийский Рыцарь': '854-knight_of_solamnia',
    'Контрабандист': '784-smuggler',
    'Корабел': '785-shipwright',
    'Морской пехотинец': '786-marine',
    'Рыбак': '783-fisher',
    'Потерявшийся в царстве ': '792-feylost',
    'Подручный Ведьмосвета': '793-witchlight_hand',
    'Антрополог': '756-anthropologist',
    'Археолог': '791-archaeologist',
}

CLASSIC_ITEMS = {
    'char_class': CLASSIC_CLASSES,
    'char_race': CLASSIC_RACES,
    'char_story': CLASSIC_STORIES,
}

EXTENDED_ITEMS = {
    'char_class': CLASSES,
    'char_race': RACES,
    'char_story': STORIES,
}

# for story, link in STORIES.items():
#     print(f"'{story[:23]}': '{link}',")
# STORIES = {
#     'Артист': '757-entertainer',
#     'Беспризорник': '758-urchin',
#     'Благородный': '759-noble',
#     'Гильдейский ремесленник': '760-guild_artisan',
#     'Моряк': '761-sailor',
#     'Мудрец': '762-sage',
#     'Народный герой': '763-folk_hero',
#     'Отшельник': '764-hermit',
#     'Пират': '770-pirate',
#     'Преступник': '765-criminal',
#     'Прислужник': '766-acolyte',
#     'Солдат': '767-soldier',
#     'Чужеземец': '768-outlander',
#     'Шарлатан': '769-charlatan',
#     'Азартный игрок': '811-gambler',
#     'Истец': '812-plaintiff',
#     'Неудавшийся торговец': '810-failed_merchant',
#     'Потомок знаменитого авантюриста': '809-celebrity_adventurers_scion',
#     'Стажер конкурента': '813-rival_intern',
#     'Ухмылка': '817-grinner',
#     'Атлант': '787-athlete',
#     'Ветеран наёмник': '780-mercenary_veteran',
#     'Городской охотник за головами': '781-urban_bounty_hunter',
#     'Городской стражник': '772-city_watch',
#     'Дальний путешественник': '777-far_traveler',
#     'Дворянин Глубоководья': '771-waterdhavian_noble',
#     'Учёный-затворник': '774-cloistered_scholar',
#     'Утгардтский соплеменник': '782-uthgardt_tribe_member',
#     'Рыцарь ордена': '779-knight_of_the_order',
#     'Придворный': '775-courtier',
#     'Представитель фракции': '776-faction_agent',
#     'Наследник': '778-inheritor',
#     'Клановый ремесленник': '773-clan_crafter',
#     'Преследуемый': '789-haunted_one',
#     'Следователь': '790-investigator',
#     'Маг Высшего Чародейства': '855-mage_of_high_sorcery',
#     'Соламнийский Рыцарь': '854-knight_of_solamnia',
#     'Контрабандист': '784-smuggler',
#     'Корабел': '785-shipwright',
#     'Морской пехотинец': '786-marine',
#     'Рыбак': '783-fisher',
#     'Потерявшийся в царстве фей': '792-feylost',
#     'Подручный Ведьмосвета': '793-witchlight_hand',
#     'Антрополог': '756-anthropologist',
#     'Археолог': '791-archaeologist',
# }
