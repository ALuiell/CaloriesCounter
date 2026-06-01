from __future__ import annotations

TRANSLATIONS = {
    # Nouns
    "рис": {"uk": "рис", "en": "rice"},
    "гречка": {"uk": "гречка", "en": "buckwheat"},
    "каша": {"uk": "каша", "en": "porridge"},
    "овсянка": {"uk": "вівсянка", "en": "oatmeal"},
    "овсяные": {"uk": "вівсяні", "en": "oat"},
    "хлопья": {"uk": "пластівці", "en": "flakes"},
    "макароны": {"uk": "макарони", "en": "pasta"},
    "паста": {"uk": "паста", "en": "pasta"},
    "перловка": {"uk": "перловка", "en": "barley"},
    "булгур": {"uk": "булгур", "en": "bulgur"},
    "кускус": {"uk": "кускус", "en": "couscous"},
    "киноа": {"uk": "кіноа", "en": "quinoa"},
    "пшено": {"uk": "пшоно", "en": "millet"},
    "мука": {"uk": "борошно", "en": "flour"},
    "хлеб": {"uk": "хліб", "en": "bread"},
    "картофель": {"uk": "картопля", "en": "potato"},
    "картошка": {"uk": "картопля", "en": "potato"},
    "помидор": {"uk": "помідор", "en": "tomato"},
    "томат": {"uk": "томат", "en": "tomato"},
    "огурец": {"uk": "огірок", "en": "cucumber"},
    "огурцы": {"uk": "огірки", "en": "cucumbers"},
    "морковь": {"uk": "морква", "en": "carrot"},
    "лук": {"uk": "цибуля", "en": "onion"},
    "капуста": {"uk": "капуста", "en": "cabbage"},
    "брокколи": {"uk": "броколі", "en": "broccoli"},
    "перец": {"uk": "перець", "en": "pepper"},
    "салат": {"uk": "салат", "en": "salad"},
    "айсберг": {"uk": "айсберг", "en": "iceberg"},
    "кукуруза": {"uk": "кукурудза", "en": "corn"},
    "горошек": {"uk": "горошок", "en": "peas"},
    "шампиньоны": {"uk": "печериці", "en": "mushrooms"},
    "грибы": {"uk": "гриби", "en": "mushrooms"},
    "чеснок": {"uk": "часник", "en": "garlic"},
    "шпинат": {"uk": "шпинат", "en": "spinach"},
    "кабачок": {"uk": "кабачок", "en": "zucchini"},
    "цукини": {"uk": "цукіні", "en": "zucchini"},
    "яблоко": {"uk": "яблуко", "en": "apple"},
    "банан": {"uk": "банан", "en": "banana"},
    "апельсин": {"uk": "апельсин", "en": "orange"},
    "клубника": {"uk": "полуниця", "en": "strawberry"},
    "яйцо": {"uk": "яйце", "en": "egg"},
    "яичница": {"uk": "яєчня", "en": "fried egg"},
    "яйца": {"uk": "яйця", "en": "eggs"},
    "курица": {"uk": "курка", "en": "chicken"},
    "куриная": {"uk": "куряча", "en": "chicken"},
    "куриное": {"uk": "куряче", "en": "chicken"},
    "грудка": {"uk": "грудка", "en": "breast"},
    "филе": {"uk": "філе", "en": "fillet"},
    "говядина": {"uk": "яловичина", "en": "beef"},
    "свинина": {"uk": "свинина", "en": "pork"},
    "молоко": {"uk": "молоко", "en": "milk"},
    "творог": {"uk": "сир", "en": "cottage cheese"},
    "сыр": {"uk": "сир", "en": "cheese"},
    "сырники": {"uk": "сирники", "en": "syrniki"},
    "масло": {"uk": "масло", "en": "butter"},
    "рыба": {"uk": "риба", "en": "fish"},
    "лосось": {"uk": "лосось", "en": "salmon"},
    "семга": {"uk": "сьомга", "en": "salmon"},
    "хек": {"uk": "хек", "en": "hake"},
    "тунец": {"uk": "тунець", "en": "tuna"},
    "вода": {"uk": "вода", "en": "water"},
    "чай": {"uk": "чай", "en": "tea"},
    "кофе": {"uk": "кава", "en": "coffee"},
    "сок": {"uk": "сік", "en": "juice"},
    "сахар": {"uk": "цукор", "en": "sugar"},
    "соль": {"uk": "сіль", "en": "salt"},
    "батон": {"uk": "батон", "en": "baguette"},
    "сурими": {"uk": "сурімі", "en": "surimi"},
    "майонез": {"uk": "майонез", "en": "mayonnaise"},
    "горчица": {"uk": "гірчиця", "en": "mustard"},
    "мед": {"uk": "мед", "en": "honey"},
    "мёд": {"uk": "мед", "en": "honey"},
    "пюре": {"uk": "пюре", "en": "puree"},
    "плов": {"uk": "плов", "en": "pilaf"},
    "борщ": {"uk": "борщ", "en": "borscht"},
    "суп": {"uk": "суп", "en": "soup"},
    "бульон": {"uk": "бульйон", "en": "broth"},
    "омлет": {"uk": "омлет", "en": "omelette"},
    "кетчуп": {"uk": "кетчуп", "en": "ketchup"},
    "круассан": {"uk": "круасан", "en": "croissant"},
    "айран": {"uk": "айран", "en": "ayran"},
    "ряженка": {"uk": "ряжанка", "en": "ryazhenka"},
    "сулугуни": {"uk": "сулугуні", "en": "suluguni"},
    "брынза": {"uk": "бринза", "en": "brynza"},
    "творожный": {"uk": "сирний", "en": "cream"},
    "йогурт": {"uk": "йогурт", "en": "yogurt"},
    "сметана": {"uk": "сметана", "en": "sour cream"},
    "кефир": {"uk": "кефір", "en": "kefir"},
    "сливки": {"uk": "вершки", "en": "cream"},
    "индейка": {"uk": "індичка", "en": "turkey"},
    "утка": {"uk": "качка", "en": "duck"},
    "кролик": {"uk": "кролик", "en": "rabbit"},
    "креветки": {"uk": "креветки", "en": "shrimp"},
    "мидии": {"uk": "мідії", "en": "mussels"},
    "кальмары": {"uk": "кальмари", "en": "squid"},
    "малина": {"uk": "малина", "en": "raspberry"},
    "черника": {"uk": "чорниця", "en": "blueberry"},
    "голубика": {"uk": "лохина", "en": "blueberry"},
    "вишня": {"uk": "вишня", "en": "cherry"},
    "черешня": {"uk": "черешня", "en": "sweet cherry"},
    "персик": {"uk": "персик", "en": "peach"},
    "абрикос": {"uk": "абрикос", "en": "apricot"},
    "слива": {"uk": "слива", "en": "plum"},
    "груша": {"uk": "груша", "en": "pear"},
    "виноград": {"uk": "виноград", "en": "grape"},
    "лимон": {"uk": "лимон", "en": "lemon"},
    "лайм": {"uk": "лайм", "en": "lime"},
    "грейпфрут": {"uk": "грейпфрут", "en": "grapefruit"},
    "ананас": {"uk": "ананас", "en": "pineapple"},
    "манго": {"uk": "манго", "en": "mango"},
    "авокадо": {"uk": "авокадо", "en": "avocado"},
    "оливковое": {"uk": "оливкова", "en": "olive"},
    "подсолнечное": {"uk": "соняшникова", "en": "sunflower"},
    "орех": {"uk": "горіх", "en": "nut"},
    "миндаль": {"uk": "мигдаль", "en": "almond"},
    "фундук": {"uk": "фундук", "en": "hazelnut"},
    "кешью": {"uk": "кеш'ю", "en": "cashew"},
    "грецкий": {"uk": "волоський", "en": "walnut"},
    "арахис": {"uk": "арахіс", "en": "peanut"},
    "семечки": {"uk": "насіння", "en": "seeds"},
    "семена": {"uk": "насіння", "en": "seeds"},
    "тыква": {"uk": "гарбуз", "en": "pumpkin"},
    "какао": {"uk": "какао", "en": "cocoa"},
    "шоколад": {"uk": "шоколад", "en": "chocolate"},
    "соус": {"uk": "соус", "en": "sauce"},
    "соевый": {"uk": "соєвий", "en": "soy"},

    # Adjectives / Modifiers
    "белый": {"uk": "білий", "en": "white"},
    "бурый": {"uk": "бурий", "en": "brown"},
    "овсяная": {"uk": "вівсяна", "en": "oat"},
    "пшеничная": {"uk": "пшенична", "en": "wheat"},
    "яичный": {"uk": "яєчний", "en": "egg"},
    "белок": {"uk": "білок", "en": "white"},
    "желток": {"uk": "жовток", "en": "yolk"},
    "коричневый": {"uk": "коричневий", "en": "brown"},
    "цельнозерновые": {"uk": "цільнозернові", "en": "whole wheat"},
    "цельнозерновой": {"uk": "цільнозерновий", "en": "whole wheat"},
    "цельнозерновая": {"uk": "цільнозернова", "en": "whole wheat"},
    "желтая": {"uk": "жовта", "en": "yellow"},
    "желтый": {"uk": "жовтий", "en": "yellow"},
    "болгарский": {"uk": "болгарський", "en": "bell"},
    "зеленый": {"uk": "зелений", "en": "green"},
    "зеленая": {"uk": "зелена", "en": "green"},
    "красный": {"uk": "червоний", "en": "red"},
    "красная": {"uk": "червона", "en": "red"},
    "белокочанная": {"uk": "білокачанна", "en": "white"},
    "цветная": {"uk": "цвітна", "en": "cauliflower"},
    "сладкий": {"uk": "солодкий", "en": "sweet"},
    "репчатый": {"uk": "ріпчаста", "en": "onion"},
    "домашний": {"uk": "домашній", "en": "homemade"},
    "домашние": {"uk": "домашні", "en": "homemade"},
    "сливочный": {"uk": "вершковий", "en": "cream"},
    "сливочное": {"uk": "вершкове", "en": "butter"},
    "растительное": {"uk": "рослинна", "en": "vegetable"},
    "классический": {"uk": "класичний", "en": "classic"},
    "жирный": {"uk": "жирний", "en": "fatty"},
    "соленый": {"uk": "солоний", "en": "salted"},
    "соленая": {"uk": "солона", "en": "salted"},
    "пчелиный": {"uk": "бджолиний", "en": "bee"},
    "натуральный": {"uk": "натуральний", "en": "natural"},
    "кисломолочный": {"uk": "кисломолочний", "en": "fermented dairy"},
    "топленое": {"uk": "пряжене", "en": "baked"},
    "рассольный": {"uk": "ропний", "en": "brined"},
    "творожный": {"uk": "сирний", "en": "curd"},
    "обезжиренный": {"uk": "знежирений", "en": "fat-free"},
    "нежирный": {"uk": "нежирний", "en": "low-fat"},
    "сухое": {"uk": "сухе", "en": "dry"},
    "сухая": {"uk": "суха", "en": "dry"},
    "свиной": {"uk": "свинячий", "en": "pork"},
    "говяжий": {"uk": "яловичий", "en": "beef"},
    "морская": {"uk": "морська", "en": "sea"},
    "речная": {"uk": "річкова", "en": "river"},
    "черный": {"uk": "чорний", "en": "black"},
    "горький": {"uk": "гіркий", "en": "dark"},

    # States
    "вареный": {"uk": "варений", "en": "cooked"},
    "вареная": {"uk": "варена", "en": "cooked"},
    "вареные": {"uk": "варені", "en": "cooked"},
    "сухой": {"uk": "сухий", "en": "dry"},
    "сухая": {"uk": "суха", "en": "dry"},
    "сухие": {"uk": "сухі", "en": "dry"},
    "сырой": {"uk": "сирий", "en": "raw"},
    "сырая": {"uk": "сира", "en": "raw"},
    "сырое": {"uk": "сире", "en": "raw"},
    "готовый": {"uk": "готовий", "en": "cooked"},
    "готовая": {"uk": "готова", "en": "cooked"},
    "готовое": {"uk": "готове", "en": "cooked"},
    "приготовленный": {"uk": "приготовлений", "en": "cooked"},
    "отварной": {"uk": "відварний", "en": "boiled"},
    "запеченный": {"uk": "запечений", "en": "baked"},
    "запеченная": {"uk": "запечена", "en": "baked"},
    "печеная": {"uk": "печена", "en": "baked"},
    "жареный": {"uk": "смажений", "en": "fried"},
    "жареное": {"uk": "смажене", "en": "fried"},
    "консервированный": {"uk": "консервований", "en": "canned"},
    "консервированные": {"uk": "консервовані", "en": "canned"},
    "на воде": {"uk": "на воді", "en": "cooked in water"},
    "из банки": {"uk": "з банки", "en": "canned"},
}

CATEGORIES = {
    "хлеб и выпечка": {"uk": "хліб та випічка", "en": "bread and bakery"},
    "сладости": {"uk": "солодощі", "en": "sweets"},
    "супы": {"uk": "супи", "en": "soups"},
    "готовые блюда": {"uk": "готові страви", "en": "ready meals"},
    "выпечка": {"uk": "випічка", "en": "bakery"},
    "орехи и семечки": {"uk": "горіхи та насіння", "en": "nuts and seeds"},
    "торты и десерты": {"uk": "торти та десерти", "en": "cakes and desserts"},
    "молочные продукты": {"uk": "молочні продукти", "en": "dairy products"},
    "яйца": {"uk": "яйця", "en": "eggs"},
    "рыба и морепродукты": {"uk": "риба та морепродукти", "en": "fish and seafood"},
    "овощи": {"uk": "овочі", "en": "vegetables"},
    "напитки": {"uk": "напої", "en": "drinks"},
    "бобовые": {"uk": "бобові", "en": "legumes"},
    "соусы": {"uk": "соуси", "en": "sauces"},
    "фрукты и ягоды": {"uk": "фрукти та ягоди", "en": "fruits and berries"},
    "жиры и масла": {"uk": "жири та олії", "en": "fats and oils"},
    "салаты и закуски": {"uk": "салати та закуски", "en": "salads and appetizers"},
    "мясо и птица": {"uk": "м'ясо та птиця", "en": "meat and poultry"},
    "крупы и гарниры": {"uk": "крупи та гарніри", "en": "grains and side dishes"},
}


REVERSE_TRANSLATIONS = {
    "en": {},
    "uk": {},
}

for ru_word, langs in TRANSLATIONS.items():
    if "en" in langs:
        en_word = langs["en"].lower()
        if en_word not in REVERSE_TRANSLATIONS["en"]:
            REVERSE_TRANSLATIONS["en"][en_word] = ru_word
    if "uk" in langs:
        uk_word = langs["uk"].lower()
        if uk_word not in REVERSE_TRANSLATIONS["uk"]:
            REVERSE_TRANSLATIONS["uk"][uk_word] = ru_word


def translate_food_name(name_ru: str, target_lang: str) -> str:
    if target_lang == "ru":
        return name_ru
    cleaned = name_ru.lower().replace(",", " ").replace("  ", " ").strip()
    words = cleaned.split()
    translated_words = []
    
    i = 0
    while i < len(words):
        # Match two-word phrases first
        if i + 1 < len(words):
            phrase = f"{words[i]} {words[i+1]}"
            if phrase in TRANSLATIONS:
                translated_words.append(TRANSLATIONS[phrase][target_lang])
                i += 2
                continue
        
        word = words[i]
        if word in TRANSLATIONS:
            translated_words.append(TRANSLATIONS[word][target_lang])
        else:
            # Fallback (keep as is)
            translated_words.append(word)
        i += 1
            
    result = " ".join(translated_words)
    if target_lang == "en":
        return result.capitalize()
    return result


def reverse_translate_food_name(text: str, source_lang: str) -> str:
    if source_lang == "ru":
        return text
        
    cleaned = text.lower().replace(",", " ").replace("  ", " ").strip()
    words = cleaned.split()
    translated_words = []
    
    reverse_map = REVERSE_TRANSLATIONS.get(source_lang, {})
    
    i = 0
    while i < len(words):
        # Try matching up to 2 words
        if i + 1 < len(words):
            phrase = f"{words[i]} {words[i+1]}"
            if phrase in reverse_map:
                translated_words.append(reverse_map[phrase])
                i += 2
                continue
                
        word = words[i]
        if word in reverse_map:
            translated_words.append(reverse_map[word])
        else:
            translated_words.append(word)
        i += 1
        
    return " ".join(translated_words)


def translate_category(category_ru: str, target_lang: str) -> str:
    if target_lang == "ru":
        return category_ru
    cat = category_ru.lower().strip()
    if cat in CATEGORIES:
        return CATEGORIES[cat][target_lang]
    return category_ru
