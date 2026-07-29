# Import tools for this file.

import hashlib
import random
from faker import Faker
from zxcvbn import zxcvbn

# Fake passwords for internal users/employees & the leaked dump.

test_passwords = ["qwerty", "123456", "password", "111111", "letmein", "admin123",
    "password1", "iloveyou", "welcome1", "monkey123", "sunshine1", "football",
    "abc12345", "PurpleWillow5", "PurpleCedar7", "SilentStorm44", "BrightOcean78",
    "BrightRiver22", "BraveFalcon14", "SilentRiver66", "HappyOcean54",
    "BrightStorm39", "LuckyStorm60", "BrightStorm22", "GoldenOcean17",
    "LuckyTiger73", "SilentBlaze8", "SilentStorm75", "GoldenStorm13",
    "QuietFalcon51", "BraveBlaze44", "BrightRiver12", "BraveBlaze90",
    "SilentTiger80", "SilentWillow81", "QuietFalcon63", "LuckyTiger86",
    "GoldenBlaze88", "GoldenRiver74", "PurpleRiver69", "BraveBlaze37",
    "SilentCedar54", "GoldenTiger72", "SilentTiger94", "GoldenCedar51",
    "LuckyFalcon97", "HappyRiver74", "LuckyStorm3", "GoldenFalcon90",
    "QuietBlaze75", "BraveFalcon56", "BrightCedar71", "SilentWillow12",
    "RapidCanyon791@", "GentleHarbor478$", "MightyMeadow69@", "CosmicPanther85@",
    "WisePhoenix979#", "SwiftMountain818%", "GentleHarbor650$", "SwiftPanther529!",
    "LoyalWolf409$", "GentlePhoenix531#", "MightyHarbor852%", "HiddenMountain229%",
    "GentleCanyon759#", "I_crave_ch0c0late!065", "BoldPanther550!", "Shitake!Mushrooms",
    "WiseMountain758!", "FuzzyRaven798%", "RapidPhoenix289!", "CozyRaven937!",
    "RapidWolf548#", "BoldCanyon486!", "HiddenSummit27!", "HiddenMountain906$",
    "CozyRaven974%", "FuzzyPhoenix724$", "CosmicRaven371@", "SwiftPanther113#",
    "BoldDragon105!", "p00h_b34r_is_cute_af!048", "FuzzyPhoenix659*", "RapidMeadow675@",
    "CosmicSummit386@", "SwiftPhoenix88@", "BoldSummit327@"]

# Imaginary employees' credentials (email, hashed password).

def generate_int_employees(num_employees):
    fake = Faker()
    users = []
    for i in range(num_employees):
        first = fake.first_name().lower()
        last = fake.last_name().lower()
        email = f"{first}.{last}@clovercrest.test"
        password = random.choice(test_passwords)
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        users.append((email, password, password_hash))
    return users

def save_int_employees(employees, filepath):
    with open(filepath, "w") as file:
        file.write("email,password_hash" + "\n")
        for email, password, password_hash in employees:
            file.write(f"{email},{password_hash}\n")

# List of dump data. Emails that match internal users vs. some unrelated to the company.

def generate_ext_dump(int_employees, matched_num_emails, unrelated_num_emails):
    fake = Faker()

    email_to_password = {}
    for email, password, password_hash in int_employees:
        email_to_password[email] = password

    all_emails = list(email_to_password.keys())
    matched_emails = random.sample(all_emails, matched_num_emails)
    unrelated_emails = [fake.email() for i in range(unrelated_num_emails)]

    ext_dump = []
    for email in matched_emails:
        roll = random.randint(1, 100)
        if roll <= 60:
            password = email_to_password[email]
        else:
            password = random.choice(test_passwords)
        ext_dump.append((email, password))

    for email in unrelated_emails:
        password = random.choice(test_passwords)
        ext_dump.append((email, password))

    return ext_dump

# Leaked dump -> plain text: email, password.

def save_ext_dump(dump, filepath):
    with open (filepath, "w") as file:
        for email, password in dump:
            file.write(f"{email}, {password}\n")

# Define password strenght with zxcvbn.

def check_password_strength(password):
    result = zxcvbn(password)
    return result["score"]

def print_strength_summary(passwords):
    weak = 0
    medium = 0
    strong = 0

    for password in passwords:
        score = check_password_strength(password)
        if score <= 1:
            weak += 1
        elif score <= 3:
            medium += 1
        else:
            strong += 1
    print("Weak:", weak, "Medium:", medium, "Strong:", strong)

print_strength_summary(test_passwords)

# Run the script & generate and save both files.

employees = generate_int_employees(50)
save_int_employees(employees, "int_employees.csv")

ext_dump = generate_ext_dump(employees, 5, 32)
save_ext_dump(ext_dump, "ext_dump.csv")

with open("common_wordlist.txt", "w") as file:
    for password in test_passwords:
        file.write(password + "\n")