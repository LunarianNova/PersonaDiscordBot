from requests_html import HTMLSession
import sqlite3


# Make Database
db = sqlite3.connect('Personas.db')
cursor = db.cursor()
cursor.execute('''DROP TABLE IF EXISTS personas''')
cursor.execute('''CREATE TABLE IF NOT EXISTS personas (
                alias TEXT,
                name TEXT,
                arcana TEXT,
                level INTEGER
                )''')
cursor.execute('''DROP TABLE IF EXISTS affinities''')
cursor.execute('''CREATE TABLE IF NOT EXISTS affinities (
                name TEXT,
                physical TEXT,
                gun TEXT,
                fire TEXT,
                ice TEXT,
                electric TEXT,
                wind TEXT,
                psychic TEXT,
                nuclear TEXT,
                bless TEXT,
                curse TEXT
                )''')
cursor.execute('''DROP TABLE IF EXISTS stats''')
cursor.execute('''CREATE TABLE IF NOT EXISTS stats (
                name TEXT,
                strength INTEGER,
                magic INTEGER,
                endurance INTEGER,
                agility INTEGER,
                luck INTEGER
                )''')


# Connect to the Googs and retrieve Data
session = HTMLSession()
website = session.get(url="https://chinhodado.github.io/persona5_calculator/indexRoyal.html#/list")
website.html.render(retries=8)
levels = website.html.find("td.ng-binding")
names = website.html.find("a.persona-name.ng-binding")
tds = website.html.find("td")
affinitylist = []
for td in tds:
    affinities = ['-', 'ab', 'wk', 'rs', 'rp', 'nu']
    if td.text in affinities:
        affinitylist.append(td.text)
levellist, arcanalist, count = [], [], 0

# Add the Arcana and Level to a list
for level in levels:
    try:
        int(level.text)
        levellist.append(level.text)
    except ValueError:
        arcanalist.append(level.text)

# Bring it all together, and add to db
for level in levellist[::6]:
    sql = '''INSERT INTO personas(alias, name, arcana, level) VALUES(?, ?, ?, ?)'''
    likename = names[count].text.replace("-", "").replace(" ", "").replace("'", "").lower()
    val = (likename, names[count].text, arcanalist[count], level)
    cursor.execute(sql, val)
    db.commit()
    count += 1

# Erase the levels from the list, leaving stats
for level in levellist[::6]:
    levellist.remove(level)

# Add stats to table
statnumber = 0
for persona in range(0, len(names)):
    st, ma, en, ag, lu = levellist[statnumber], levellist[statnumber+1], levellist[statnumber+2], levellist[statnumber+3], levellist[statnumber+4]
    sql = '''INSERT INTO stats(name, strength, magic, endurance, agility, luck) VALUES(?, ?, ?, ?, ?, ?)'''
    val = (names[persona].text, st, ma, en, ag, lu)
    cursor.execute(sql, val)
    db.commit()
    statnumber += 5

# Add affinities to table
affinitynumber = 0
for persona in range(0, len(names)):
    phys, gun, fire, ice, elec, wind, psy, nuke, bless, curse = affinitylist[affinitynumber], affinitylist[affinitynumber+1], affinitylist[affinitynumber+2], affinitylist[affinitynumber+3], affinitylist[affinitynumber+4], affinitylist[affinitynumber+5], affinitylist[affinitynumber+6], affinitylist[affinitynumber+7], affinitylist[affinitynumber+8], affinitylist[affinitynumber+9]
    sql = '''INSERT INTO affinities(name, physical, gun, fire, ice, electric, wind, psychic, nuclear, bless, curse)
     VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
    val = (names[persona].text, phys, gun, fire, ice, elec, wind, psy, nuke, bless, curse)
    cursor.execute(sql, val)
    db.commit()
    affinitynumber += 10

cursor.execute('''SELECT * FROM personas''')
print(cursor.fetchall())
db.close()