import sqlite3
import math
import difflib

# List of filtered names to compare against
db = sqlite3.connect('Personas.db')
cursor = db.cursor()
filtered = []
cursor.execute('SELECT alias FROM personas')
names = cursor.fetchall()
for name in names:
    filtered.append(name[0])
db.close()

# Arcana junk, best if minimised
arcanacombos = {
    'Fool Fool': 'Fool',
    'Fool Magician': 'Death',
    'Fool Priestess': 'Moon',
    'Fool Empress': 'Hanged',
    'Fool Emperor': 'Temperance',
    'Fool Hierophant': 'Hermit',
    'Fool Lovers': 'Chariot',
    'Fool Chariot': 'Moon',
    'Fool Justice': 'Star',
    'Fool Hermit': 'Priestess',
    'Fool Fortune': 'Faith',
    'Fool Strength': 'Death',
    'Fool Hanged': 'Tower',
    'Fool Death': 'Strength',
    'Fool Temperance': 'Hierophant',
    'Fool Devil': 'Temperance',
    'Fool Tower': 'Empress',
    'Fool Star': 'Magician',
    'Fool Moon': 'Justice',
    'Fool Sun': 'Justice',
    'Fool Judgement': 'Sun',
    'Fool Faith': 'Councillor',
    'Fool Councillor': 'Hierophant',
    'Magician Magician': 'Magician',
    'Magician Priestess': 'Temperance',
    'Magician Empress': 'Justice',
    'Magician Emperor': 'Faith',
    'Magician Hierophant': 'Death',
    'Magician Lovers': 'Devil',
    'Magician Chariot': 'Priestess',
    'Magician Justice': 'Emperor',
    'Magician Hermit': 'Lovers',
    'Magician Fortune': 'Justice',
    'Magician Strength': 'Fool',
    'Magician Hanged': 'Empress',
    'Magician Death': 'Hermit',
    'Magician Temperance': 'Chariot',
    'Magician Devil': 'Hierophant',
    'Magician Tower': 'Temperance',
    'Magician Star': 'Priestess',
    'Magician Moon': 'Lovers',
    'Magician Sun': 'Hierophant',
    'Magician Judgement': 'Strength',
    'Magician Faith': 'Strength',
    'Magician Councillor': 'Moon',
    'Priestess Priestess': 'Priestess',
    'Priestess Empress': 'Emperor',
    'Priestess Emperor': 'Empress',
    'Priestess Hierophant': 'Magician',
    'Priestess Lovers': 'Fortune',
    'Priestess Chariot': 'Hierophant',
    'Priestess Justice': 'Death',
    'Priestess Hermit': 'Temperance',
    'Priestess Fortune': 'Magician',
    'Priestess Strength': 'Devil',
    'Priestess Hanged': 'Death',
    'Priestess Death': 'Magician',
    'Priestess Temperance': 'Devil',
    'Priestess Devil': 'Moon',
    'Priestess Tower': 'Hanged',
    'Priestess Star': 'Hermit',
    'Priestess Moon': 'Hierophant',
    'Priestess Sun': 'Chariot',
    'Priestess Judgement': 'Justice',
    'Priestess Faith': 'Justice',
    'Priestess Councillor': 'Faith',
    'Empress Empress': 'Empress',
    'Empress Emperor': 'Justice',
    'Empress Hierophant': 'Fool',
    'Empress Lovers': 'Judgement',
    'Empress Chariot': 'Star',
    'Empress Justice': 'Lovers',
    'Empress Hermit': 'Strength',
    'Empress Fortune': 'Hermit',
    'Empress Strength': 'Faith',
    'Empress Hanged': 'Priestess',
    'Empress Death': 'Fool',
    'Empress Temperance': 'Faith',
    'Empress Devil': 'Sun',
    'Empress Tower': 'Emperor',
    'Empress Star': 'Lovers',
    'Empress Moon': 'Fortune',
    'Empress Sun': 'Tower',
    'Empress Judgement': 'Emperor',
    'Empress Faith': 'Magician',
    'Empress Councillor': 'Hanged',
    'Emperor Emperor': 'Emperor',
    'Emperor Hierophant': 'Fortune',
    'Emperor Lovers': 'Fool',
    'Emperor Chariot': 'Faith',
    'Emperor Justice': 'Chariot',
    'Emperor Hermit': 'Hierophant',
    'Emperor Fortune': 'Sun',
    'Emperor Strength': 'Tower',
    'Emperor Hanged': 'Devil',
    'Emperor Death': 'Hermit',
    'Emperor Temperance': 'Devil',
    'Emperor Devil': 'Justice',
    'Emperor Tower': 'Star',
    'Emperor Star': 'Lovers',
    'Emperor Moon': 'Tower',
    'Emperor Sun': 'Judgement',
    'Emperor Judgement': 'Priestess',
    'Emperor Faith': 'Priestess',
    'Emperor Councillor': 'Lovers',
    'Hierophant Hierophant': 'Hierophant',
    'Hierophant Lovers': 'Strength',
    'Hierophant Chariot': 'Star',
    'Hierophant Justice': 'Hanged',
    'Hierophant Hermit': 'Councillor',
    'Hierophant Fortune': 'Justice',
    'Hierophant Strength': 'Fool',
    'Hierophant Hanged': 'Sun',
    'Hierophant Death': 'Chariot',
    'Hierophant Temperance': 'Death',
    'Hierophant Devil': 'Hanged',
    'Hierophant Tower': 'Judgement',
    'Hierophant Star': 'Tower',
    'Hierophant Moon': 'Priestess',
    'Hierophant Sun': 'Lovers',
    'Hierophant Judgement': 'Faith',
    'Hierophant Faith': 'Empress',
    'Hierophant Councillor': 'Justice',
    'Lovers Lovers': 'Lovers',
    'Lovers Chariot': 'Temperance',
    'Lovers Justice': 'Judgement',
    'Lovers Hermit': 'Chariot',
    'Lovers Fortune': 'Strength',
    'Lovers Strength': 'Death',
    'Lovers Hanged': 'Councillor',
    'Lovers Death': 'Temperance',
    'Lovers Temperance': 'Strength',
    'Lovers Devil': 'Moon',
    'Lovers Tower': 'Empress',
    'Lovers Star': 'Faith',
    'Lovers Moon': 'Magician',
    'Lovers Sun': 'Empress',
    'Lovers Judgement': 'Hanged',
    'Lovers Faith': 'Tower',
    'Lovers Councillor': 'Tower',
    'Chariot Chariot': 'Chariot',
    'Chariot Justice': 'Moon',
    'Chariot Hermit': 'Devil',
    'Chariot Fortune': 'Councillor',
    'Chariot Strength': 'Hermit',
    'Chariot Hanged': 'Fool',
    'Chariot Death': 'Devil',
    'Chariot Temperance': 'Strength',
    'Chariot Devil': 'Temperance',
    'Chariot Tower': 'Fortune',
    'Chariot Star': 'Moon',
    'Chariot Moon': 'Lovers',
    'Chariot Sun': 'Priestess',
    'Chariot Faith': 'Lovers',
    'Chariot Councillor': 'Sun',
    'Justice Justice': 'Justice',
    'Justice Hermit': 'Magician',
    'Justice Fortune': 'Emperor',
    'Justice Strength': 'Councillor',
    'Justice Hanged': 'Lovers',
    'Justice Death': 'Fool',
    'Justice Temperance': 'Emperor',
    'Justice Devil': 'Fool',
    'Justice Tower': 'Sun',
    'Justice Star': 'Empress',
    'Justice Moon': 'Devil',
    'Justice Sun': 'Hanged',
    'Justice Faith': 'Hanged',
    'Justice Councillor': 'Emperor',
    'Hermit Hermit': 'Hermit',
    'Hermit Fortune': 'Star',
    'Hermit Strength': 'Hierophant',
    'Hermit Hanged': 'Star',
    'Hermit Death': 'Strength',
    'Hermit Temperance': 'Strength',
    'Hermit Devil': 'Priestess',
    'Hermit Tower': 'Judgement',
    'Hermit Star': 'Strength',
    'Hermit Moon': 'Priestess',
    'Hermit Sun': 'Devil',
    'Hermit Judgement': 'Emperor',
    'Hermit Faith': 'Judgement',
    'Hermit Councillor': 'Faith',
    'Fortune Fortune': 'Fortune',
    'Fortune Strength': 'Faith',
    'Fortune Hanged': 'Emperor',
    'Fortune Death': 'Star',
    'Fortune Temperance': 'Empress',
    'Fortune Devil': 'Hierophant',
    'Fortune Tower': 'Hanged',
    'Fortune Star': 'Devil',
    'Fortune Moon': 'Sun',
    'Fortune Sun': 'Star',
    'Fortune Judgement': 'Tower',
    'Fortune Faith': 'Councillor',
    'Fortune Councillor': 'Judgement',
    'Strength Strength': 'Strength',
    'Strength Hanged': 'Temperance',
    'Strength Death': 'Hierophant',
    'Strength Temperance': 'Chariot',
    'Strength Devil': 'Death',
    'Strength Tower': 'Faith',
    'Strength Star': 'Moon',
    'Strength Moon': 'Magician',
    'Strength Sun': 'Moon',
    'Strength Faith': 'Star',
    'Strength Councillor': 'Empress',
    'Hanged Hanged': 'Hanged',
    'Hanged Death': 'Moon',
    'Hanged Temperance': 'Death',
    'Hanged Devil': 'Fortune',
    'Hanged Tower': 'Hermit',
    'Hanged Star': 'Justice',
    'Hanged Moon': 'Councillor',
    'Hanged Sun': 'Hierophant',
    'Hanged Judgement': 'Star',
    'Hanged Faith': 'Devil',
    'Hanged Councillor': 'Star',
    'Death Death': 'Death',
    'Death Temperance': 'Hanged',
    'Death Devil': 'Chariot',
    'Death Tower': 'Sun',
    'Death Star': 'Councillor',
    'Death Moon': 'Hierophant',
    'Death Sun': 'Priestess',
    'Death Faith': 'Fool',
    'Death Councillor': 'Magician',
    'Temperance Temperance': 'Temperance',
    'Temperance Devil': 'Fool',
    'Temperance Tower': 'Fortune',
    'Temperance Star': 'Sun',
    'Temperance Moon': 'Councillor',
    'Temperance Sun': 'Magician',
    'Temperance Judgement': 'Hermit',
    'Temperance Faith': 'Hermit',
    'Temperance Councillor': 'Fool',
    'Devil Devil': 'Devil',
    'Devil Tower': 'Magician',
    'Devil Star': 'Strength',
    'Devil Moon': 'Chariot',
    'Devil Sun': 'Hermit',
    'Devil Judgement': 'Lovers',
    'Devil Faith': 'Chariot',
    'Devil Councillor': 'Chariot',
    'Tower Tower': 'Tower',
    'Tower Star': 'Councillor',
    'Tower Moon': 'Hermit',
    'Tower Sun': 'Emperor',
    'Tower Judgement': 'Moon',
    'Tower Faith': 'Death',
    'Tower Councillor': 'Death',
    'Star Star': 'Star',
    'Star Moon': 'Temperance',
    'Star Sun': 'Judgement',
    'Star Judgement': 'Fortune',
    'Star Faith': 'Temperance',
    'Star Councillor': 'Sun',
    'Moon Moon': 'Moon',
    'Moon Sun': 'Empress',
    'Moon Judgement': 'Fool',
    'Moon Faith': 'Sun',
    'Moon Councillor': 'Temperance',
    'Sun Sun': 'Sun',
    'Sun Judgement': 'Death',
    'Sun Faith': 'Emperor',
    'Sun Councillor': 'Fortune',
    'Judgement Judgement': 'Judgement',
    'Judgement Faith': 'Fortune',
    'Judgement Councillor': 'Devil',
    'Faith Faith': 'Faith',
    'Faith Councillor': 'Priestess',
    'Councillor Councillor': 'Councillor',
    'World World': 'World'}

# List of rare persona
rare_persona = ["Regent", "Queen's Necklace", "Stone of Scone", "Koh-i-Noor",
                "Orlov", "Emperor's Amulet", "Hope Diamond", "Crystal Skull", "Orichalum"]


# Make a Persona Object
class Persona(object):
    def __init__(self, name, arcana, level, affinities, stats):
        self.name = name
        self.arcana = arcana
        self.level = level
        self.affinities = affinities
        self.stats = stats


# Handle fusion of 2 personae
def fuse_persona(persona, secondpersona):
    db = sqlite3.connect('Personas.db')
    cursor = db.cursor()
    lower, higher = [], []
    cursor.execute('SELECT * FROM personas WHERE alias = "{}"'.format(difflib.get_close_matches(persona.replace("-", "").replace(" ", "").replace("'", "").lower(), filtered, n=1)[0]))
    persona = cursor.fetchone()
    cursor.execute('SELECT * FROM personas WHERE alias = "{}"'.format(difflib.get_close_matches(secondpersona.replace("-", "").replace(" ", "").replace("'", "").lower(), filtered, n=1)[0]))
    secondpersona = cursor.fetchone()
    persona = Persona(persona[1], persona[2], persona[3], 1, 1)
    secondpersona = Persona(secondpersona[1], secondpersona[2], secondpersona[3], 1, 1)
    if math.floor((persona.level + secondpersona.level) / 2) < (persona.level + secondpersona.level)/2 < math.ceil((persona.level + secondpersona.level) / 2):
        level = (persona.level + secondpersona.level)/2 + 0.5
    else:
        level = (persona.level + secondpersona.level)/2 + 1
    try:
        arcana = arcanacombos[f"{persona.arcana} {secondpersona.arcana}"]
    except KeyError:
        try:
            arcana = arcanacombos[f"{secondpersona.arcana} {persona.arcana}"]
        except KeyError:
            db.close()
            return "Impossible"
    cursor.execute('SELECT * FROM personas WHERE arcana = "{}"'.format(arcana))
    result = cursor.fetchall()
    for personae in result:
        if personae[3] < level:
            lower.append(f"{personae[1]}, {personae[3]}")
        elif personae[3] >= level:
            higher.append(f"{personae[1]}, {personae[3]}")
    if persona.name == secondpersona.name:
        return "Impossible"
    else:
        if len(higher) == 0:
            cursor.execute('SELECT * FROM stats WHERE name = "{}"'.format(lower[-1].split(",")[0]))
            stats = cursor.fetchone()
            cursor.execute('SELECT * FROM affinities WHERE name = "{}"'.format(lower[-1].split(",")[0]))
            affinities = cursor.fetchone()
            db.close()
            return Persona(lower[-1].split(",")[0], arcana, lower[-1].split(", ")[1], affinities, stats)
        else:
            cursor.execute('SELECT * FROM stats WHERE name = "{}"'.format(higher[0].split(",")[0]))
            stats = cursor.fetchone()
            cursor.execute('SELECT * FROM affinities WHERE name = "{}"'.format(higher[0].split(",")[0]))
            affinities = cursor.fetchone()
            db.close()
            return Persona(higher[0].split(",")[0], arcana, higher[0].split(", ")[1], affinities, stats)


# Database mess
def get_persona(persona):
    db = sqlite3.connect('Personas.db')
    cursor = db.cursor()
    cursor.execute('SELECT * FROM personas WHERE alias = "{}"'.format(difflib.get_close_matches(persona.replace("-", "").replace(" ", "").replace("'", "").lower(), filtered, n=1)[0]))
    result = cursor.fetchone()
    cursor.execute('SELECT * FROM stats WHERE name = "{}"'.format(result[1]))
    stats = cursor.fetchone()
    cursor.execute('SELECT * FROM affinities WHERE name = "{}"'.format(result[1]))
    affinities = cursor.fetchone()
    db.close()
    try:
        persona = Persona(result[1], result[2], result[3]. affinities, stats)
        return persona
    except TypeError:
        return f"Error, '{persona}' not found"


# Get things that fuse to the persona
def get_fusions(persona):
    possibles, organized = [], []
    db = sqlite3.connect('Personas.db')
    cursor = db.cursor()
    cursor.execute('SELECT * FROM personas WHERE alias = "{}"'.format(difflib.get_close_matches(persona.replace("-", "").replace(" ", "").replace("'", "").lower(), filtered, n=1)[0]))
    result = cursor.fetchone()
    persona = Persona(result[1], result[2], result[3], 1, 1)
    for arcana, result in arcanacombos.items():
        if result == persona.arcana:
            firstarcana, secondarcana = arcana.split()[0], arcana.split()[1]
            cursor.execute('SELECT * FROM personas WHERE arcana = "{}"'.format(firstarcana))
            firstpersonas = cursor.fetchall()
            cursor.execute('SELECT * FROM personas WHERE arcana = "{}"'.format(secondarcana))
            secondpersonas = cursor.fetchall()
            for firstpersona in firstpersonas:
                for secondpersona in secondpersonas:
                    fusionresult = fuse_persona(firstpersona[1], secondpersona[1])
                    if fusionresult != "Impossible":
                        if fusionresult.name == persona.name and firstpersona[1] != persona.name and secondpersona[1] != persona.name:
                            if firstpersona[1] not in rare_persona and secondpersona[1] not in rare_persona:
                                if f"{firstpersona[1]} / {secondpersona[1]}" not in possibles and f"{secondpersona[1]} / {firstpersona[1]}" not in possibles:
                                    cost = 0 + (27 * int(firstpersona[3]) * int(firstpersona[3])) + (126 * int(firstpersona[3])) + 2147
                                    cost += (27 * int(secondpersona[3]) * int(secondpersona[3])) + (126 * int(secondpersona[3])) + 2147
                                    possibles.append(f"{cost}: {firstpersona[1]} / {secondpersona[1]}")
    for possibility in possibles:
        organized.append(possibility.split(":"))
    organized = sorted(organized)
    comparison = organized[0][0]
    i = 0
    for index, number in enumerate(organized):
        if len(number[0]) < len(comparison):
            organized.pop(index)
            organized.insert(i, number)
            i += 1
    possibles.clear()
    for possibility in organized:
        possibles.append(": ".join(possibility))
    return possibles

