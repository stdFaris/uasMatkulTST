import random
from datetime import datetime, timedelta
from typing import List, Dict

# Constants for data generation
KECAMATAN_LIST = [
    "Menteng", "Kemang", "Kebayoran Baru", "Senayan", 
    "Tebet", "Kuningan", "Sudirman", "Thamrin",
    "Pantai Indah Kapuk", "Kelapa Gading"
]

# Added Indonesian names data
FIRST_NAMES = [
    "Muhammad", "Ahmad", "Abdul", "Budi", "Dedi", "Eko", "Firman", "Gading",
    "Hadi", "Irfan", "Joko", "Kurniawan", "Lukman", "Nizar", "Putra",
    "Ratna", "Siti", "Tri", "Utami", "Wati", "Yanti", "Zahra", "Dewi",
    "Putri", "Rina", "Ani", "Maya", "Nova", "Dian", "Lia"
]

LAST_NAMES = [
    "Wijaya", "Kusuma", "Pratama", "Saputra", "Hidayat", "Nugraha", "Ramadan",
    "Santoso", "Wibowo", "Yulianto", "Setiawan", "Permana", "Octavian", "Maulana",
    "Hidayatullah", "Firmansyah", "Gunawan", "Suryadi", "Rahman", "Abdullah",
    "Pradana", "Putra", "Hermawan", "Kartika", "Sari", "Putri", "Lestari",
    "Pertiwi", "Utami", "Handayani"
]

SPECIALIZATIONS = {
    "PEMBANTU": [
        "Cleaning", "Cooking", "Laundry", "Childcare", 
        "Elderly Care", "Pet Care", "Organization",
        "Deep Cleaning", "Window Cleaning", "Kitchen Management"
    ],
    "TUKANG_KEBUN": [
        "Landscaping", "Plant Care", "Garden Design", "Pruning",
        "Pest Control", "Irrigation", "Lawn Maintenance",
        "Flower Garden", "Vegetable Garden", "Tree Care"
    ],
    "TUKANG_PIJAT": [
        "Swedish Massage", "Deep Tissue", "Reflexology", "Sports Massage",
        "Therapeutic", "Aromatherapy", "Traditional Indonesian",
        "Shiatsu", "Thai Massage", "Chair Massage"
    ]
}

LANGUAGES = ["Indonesian", "English", "Javanese", "Sundanese", "Mandarin"]

def generate_name() -> str:
    """Generate a random Indonesian full name."""
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)
    return f"{first_name} {last_name}"

def generate_partner_data(num_partners: int = 100) -> List[Dict]:
    partners = []
    
    # Ensure minimum 6 partners per kecamatan with all roles
    for kecamatan in KECAMATAN_LIST:
        for role in ["PEMBANTU", "TUKANG_KEBUN", "TUKANG_PIJAT"]:
            # Generate 2 partners per role per kecamatan (6 total per kecamatan)
            for _ in range(2):
                partner = create_single_partner(kecamatan, role, True)
                partners.append(partner)
    
    # Generate remaining partners randomly
    remaining_partners = num_partners - (len(KECAMATAN_LIST) * 6)
    for _ in range(remaining_partners):
        kecamatan = random.choice(KECAMATAN_LIST)
        role = random.choice(["PEMBANTU", "TUKANG_KEBUN", "TUKANG_PIJAT"])
        partner = create_single_partner(kecamatan, role)
        partners.append(partner)
    
    return partners

def create_single_partner(kecamatan: str, role: str, is_baseline: bool = False) -> Dict:
    # Generate more favorable stats for baseline partners (first 6 per kecamatan)
    if is_baseline:
        experience_years = random.randint(5, 15)
        rating = round(random.uniform(4.0, 5.0), 1)
        total_reviews = random.randint(50, 200)
    else:
        experience_years = random.randint(1, 20)
        rating = round(random.uniform(3.5, 5.0), 1)
        total_reviews = random.randint(0, 300)

    # Generate pricing based on experience and rating
    base_hourly = 50000 + (experience_years * 5000) + (rating * 10000)
    pricing = {
        "hourly_rate": round(base_hourly, -3),  # Round to nearest thousand
        "daily_rate": round(base_hourly * 8 * 0.9, -3),  # 10% discount for daily
        "monthly_rate": round(base_hourly * 8 * 22 * 0.7, -3)  # 30% discount for monthly
    }

    # Select 3-5 specializations for the role
    role_specializations = random.sample(
        SPECIALIZATIONS[role], 
        random.randint(3, 5)
    )

    # Select 2-3 languages
    spoken_languages = random.sample(LANGUAGES, random.randint(2, 3))

    return {
        "full_name": generate_name(),  # Using the new name generator
        "role": role,
        "experience_years": experience_years,
        "rating": rating,
        "total_reviews": total_reviews,
        "specializations": role_specializations,
        "pricing": pricing,
        "kecamatan": kecamatan,
        "is_available": random.choice([True, True, True, False]),  # 75% chance of being available
        "languages": spoken_languages,
        "profile_description": f"Experienced {role.lower().replace('_', ' ')} with {experience_years} years of experience specializing in {', '.join(role_specializations[:2])}."
    }

def generate_partner_availability(partner_id: int) -> List[Dict]:
    availabilities = []
    start_date = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
    
    for day in range(7):  # Generate for next 7 days
        current_date = start_date + timedelta(days=day)
        
        # Morning shift: 8 AM - 2 PM
        # Afternoon shift: 2 PM - 8 PM
        shifts = [
            (current_date.replace(hour=8), current_date.replace(hour=14)),
            (current_date.replace(hour=14), current_date.replace(hour=20))
        ]
        
        for start_time, end_time in shifts:
            is_blocked = random.random() < 0.3  # 30% chance of being blocked
            availabilities.append({
                "partner_id": partner_id,
                "start_time": start_time,
                "end_time": end_time,
                "is_blocked": is_blocked
            })
    
    return availabilities

# Generate the dummy data
partners = generate_partner_data(100)

# Print sample data
print(f"Generated {len(partners)} partners")
print("\nSample partner distribution by kecamatan:")
kecamatan_count = {}
for partner in partners:
    kecamatan_count[partner['kecamatan']] = kecamatan_count.get(partner['kecamatan'], 0) + 1

for kecamatan, count in kecamatan_count.items():
    print(f"{kecamatan}: {count} partners")

# Sample output of one partner
print("\nSample partner data:")
print(partners[0])