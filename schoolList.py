rolesEmojis = [
    "1️⃣",  # For School 1
    "2️⃣",  # For School 2
    "3️⃣",  # For School 3
    "4️⃣",  # For School 4
    "5️⃣",  # For School 5
    "6️⃣",  # For School 6
    "7️⃣",  # For School 7
    "8️⃣",  # For School 8
    "9️⃣",  # For School 9
    "🔟",  # For School 10
    "🔴",  # For School 11
    "🟠",  # For School 12
    "🟡",  # For School 13
    "🟢",  # For School 14
    "🔵",  # For School 15
    "🟣",  # For School 16
    "🟤",  # For School 17
    "⚪",  # For School 18
    "⚫",  # For School 19
    "⭐"   # For School 20
]



schoolList = [
    "DPS Ruby Park",
    "South Point",
    "DPS Megacity",
    "Don Bosco Bandel",
    "Don Bosco Park Circus",
    "Heritage",
    "South City",
    "Birla High",
    "Calcutta Boys",
    "Prac Memorial",
    "St. Augustine",
    "St. Xavier's",
    "MP Birla",
    "Narayana Howrah"
]

def getSchoolList() -> list:
    schoolList.sort()
    return schoolList

def getSchoolRolesDict() -> dict:

    SortedSchools = getSchoolList()

    SchoolRolesEmoji = {}

    for i in range(len(SortedSchools)):

        SchoolRolesEmoji[rolesEmojis[i]] = SortedSchools[i]

    return SchoolRolesEmoji
