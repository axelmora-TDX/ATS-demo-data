import requests
import json
import random
import time
import os
from base64 import b64encode
from datetime import datetime, timedelta
import base64

# ============================================================
# CONFIGURATION
# reads from environment variables for GitHub Actions
# or fill in directly for local run
# ============================================================
SUBDOMAIN = "acmetechnologysolutionstelus"
EMAIL = os.environ["ZD_EMAIL"]
API_TOKEN = os.environ["ZD_API_TOKEN"]
GITHUB_TOKEN = os.environ["GH_TOKEN"]
GITHUB_REPO = "axelmora-TDX/fortify-demo-dat"
GITHUB_FILE = "data.json"

TOTAL_TICKETS = 1000
DELAY_MIN = 60
DELAY_MAX = 120

# ============================================================
# AUTH
# ============================================================
credentials = f"{EMAIL}/token:{API_TOKEN}"
encoded = b64encode(credentials.encode("utf-8")).decode("utf-8")
headers = {
    "Authorization": f"Basic {encoded}",
    "Content-Type": "application/json"
}
BASE_URL = f"https://{SUBDOMAIN}.zendesk.com/api/v2"

# ============================================================
# REFERENCE DATA
# ============================================================
PRODUCTS = ["Lightning", "Thunder", "Stormcloud"]

SERIAL_PREFIXES = {
    "Lightning": "LTN",
    "Thunder": "THN",
    "Stormcloud": "SCL"
}

CARRIERS = ["UPS", "FedEx"]
STATUSES = ["Delivered", "Shipped", "Processing", "Pending"]
SATISFACTION_SCORES = ["Great", "Good", "Okay", "N/A"]

CITIES = [
    ("New York", "NY", "10001"),
    ("Los Angeles", "CA", "90001"),
    ("Chicago", "IL", "60601"),
    ("Houston", "TX", "77001"),
    ("Phoenix", "AZ", "85001"),
    ("Philadelphia", "PA", "19101"),
    ("San Antonio", "TX", "78201"),
    ("San Diego", "CA", "92101"),
    ("Dallas", "TX", "75201"),
    ("San Jose", "CA", "95101"),
    ("Austin", "TX", "78701"),
    ("Jacksonville", "FL", "32099"),
    ("Denver", "CO", "80201"),
    ("Seattle", "WA", "98101"),
    ("Nashville", "TN", "37201"),
    ("Portland", "OR", "97201"),
    ("Las Vegas", "NV", "89101"),
    ("Memphis", "TN", "38101"),
    ("Louisville", "KY", "40201"),
    ("Baltimore", "MD", "21201")
]

FIRST_NAMES = [
    "James", "Emma", "Oliver", "Sophia", "William", "Ava", "Benjamin",
    "Isabella", "Lucas", "Mia", "Henry", "Charlotte", "Alexander",
    "Amelia", "Mason", "Harper", "Ethan", "Evelyn", "Daniel", "Abigail",
    "Michael", "Emily", "Matthew", "Elizabeth", "Jackson", "Sofia",
    "Sebastian", "Avery", "Jack", "Ella", "Owen", "Scarlett", "Samuel",
    "Grace", "Ryan", "Chloe", "Nathan", "Victoria", "Adam", "Riley",
    "Christopher", "Aria", "Andrew", "Lily", "Joshua", "Aurora",
    "David", "Zoey", "Joseph", "Penelope", "Carter", "Lillian",
    "Dylan", "Nora", "Wyatt", "Hannah", "Julian", "Layla", "Levi",
    "Brooklyn", "Isaac", "Zoe", "Lincoln", "Stella", "Gabriel",
    "Ellie", "Anthony", "Hazel", "Hudson", "Eliana", "Caleb", "Nova",
    "Eli", "Emilia", "Aaron", "Luna", "Thomas", "Camila", "Charles",
    "Natalie", "Connor", "Savannah", "Jonah", "Addison", "Adrian",
    "Audrey", "Cameron", "Allison", "Robert", "Claire", "Tyler",
    "Eleanor", "Nicholas", "Skylar", "Jordan", "Paisley", "Evan",
    "Violet", "Xavier", "Ellie", "Jaxon", "Willow", "Isaiah", "Leah"
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
    "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
    "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
    "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark",
    "Ramirez", "Lewis", "Robinson", "Walker", "Young", "Allen", "King",
    "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores", "Green",
    "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell",
    "Carter", "Roberts", "Phillips", "Evans", "Turner", "Torres", "Parker",
    "Collins", "Edwards", "Stewart", "Flores", "Morris", "Nguyen", "Murphy",
    "Rivera", "Cook", "Rogers", "Morgan", "Peterson", "Cooper", "Reed",
    "Bailey", "Bell", "Gomez", "Kelly", "Howard", "Ward", "Cox", "Diaz",
    "Richardson", "Wood", "Watson", "Brooks", "Bennett", "Gray", "James",
    "Reyes", "Cruz", "Hughes", "Price", "Myers", "Long", "Foster", "Sanders"
]

TICKET_SUBJECTS = {
    "Lightning": [
        "Lightning product not powering on after delivery",
        "Warranty claim for Lightning device — hardware fault",
        "How do I initiate a Lightning return?",
        "Lightning order delivered damaged",
        "Lightning product serial number not recognized",
        "Request for Lightning warranty extension",
        "Lightning device overheating issue",
        "Wrong Lightning model delivered",
        "Lightning product missing from package",
        "Need invoice copy for Lightning order",
        "Lightning firmware update stuck at 50%",
        "Lightning device not connecting to network",
        "Lightning product stopped working after 3 months",
        "Lightning delivery tracking shows delivered but not received",
        "Lightning order placed twice — need cancellation"
    ],
    "Thunder": [
        "Thunder device connectivity issue after setup",
        "Thunder technical support — firmware update failed",
        "Thunder order still showing Processing after 5 days",
        "Refund request for Thunder product",
        "Thunder device performance degrading",
        "Thunder shipment tracking number not working",
        "Thunder product setup documentation request",
        "Incorrect charge on Thunder order",
        "Thunder device not recognized by system",
        "Thunder order cancellation request",
        "Thunder integration failing with third party software",
        "Thunder device making unusual noise",
        "Thunder replacement parts availability",
        "Thunder warranty repair status update",
        "Thunder product compatibility question"
    ],
    "Stormcloud": [
        "Stormcloud onboarding support needed",
        "Stormcloud billing discrepancy on invoice",
        "Stormcloud integration failing after update",
        "Stormcloud order status not updating",
        "Stormcloud technical error — cannot access dashboard",
        "Stormcloud subscription payment failed",
        "Stormcloud data export not working",
        "Stormcloud account access issue",
        "Stormcloud delivery address update request",
        "Stormcloud refund request — wrong product ordered",
        "Stormcloud API rate limiting issue",
        "Stormcloud multi-user access setup",
        "Stormcloud performance degradation report",
        "Stormcloud backup and restore query",
        "Stormcloud compliance documentation request"
    ],
    "General": [
        "Upgrade from Standard to Platinum support enquiry",
        "Unable to locate order confirmation email",
        "Payment method update for existing order",
        "Question about Standard vs Platinum SLA",
        "Request for product comparison — Lightning vs Thunder",
        "General account billing question",
        "Contact preference update request",
        "Multi-product order enquiry",
        "Corporate purchase order submission",
        "Support tier downgrade request",
        "Request for bulk order pricing",
        "Account ownership transfer request",
        "Annual support contract renewal",
        "Request for dedicated account manager",
        "Complaint about response time"
    ]
}

TICKET_BODIES = {
    "Lightning": "I am reaching out regarding my Lightning product. I need assistance with this matter as soon as possible. Please review my order details and advise on next steps. I appreciate your prompt attention to this issue.",
    "Thunder": "I am experiencing an issue with my Thunder device and would like support from your technical team. This is impacting my day-to-day operations and I would appreciate a prompt response.",
    "Stormcloud": "I need help with my Stormcloud product. This is impacting my operations and I would appreciate a prompt response from your support team. Please prioritize this request.",
    "General": "I have a general enquiry regarding my account and support services with Acme Technology Solutions. Please assist at your earliest convenience. Thank you for your support."
}

# ============================================================
# HELPER FUNCTIONS
# ============================================================
def random_date(start_days_ago=180, end_days_ago=1):
    days = random.randint(end_days_ago, start_days_ago)
    return (datetime.now() - timedelta(days=days)).strftime("%m.%d.%Y")

def random_order_ref():
    letters = ''.join(random.choices('ABCDEFGHJKLMNPQRSTUVWXYZ', k=2))
    numbers = ''.join(random.choices('0123456789', k=6))
    return f"{letters}-{numbers}"

def random_serial(product):
    prefix = SERIAL_PREFIXES[product]
    year = random.choice(["2024", "2025", "2026"])
    number = ''.join(random.choices('0123456789', k=5))
    return f"{prefix}-{year}-{number}"

def random_phone():
    area = random.randint(200, 999)
    mid = random.randint(200, 999)
    end = random.randint(1000, 9999)
    return f"+1-{area}-{mid}-{end}"

def random_address():
    number = random.randint(100, 9999)
    streets = [
        "Main St", "Oak Avenue", "Pine Road", "Elm Street",
        "Maple Drive", "Cedar Lane", "Park Blvd", "Lake View Dr",
        "Sunset Ave", "Highland Rd", "Willow Way", "River Rd",
        "Forest Dr", "Valley View", "Mountain Ave"
    ]
    street = random.choice(streets)
    city, state, zipcode = random.choice(CITIES)
    return f"{number} {street}, {city}, {state} {zipcode}"

def generate_order_record(external_id, order_ref, name,
                          email, tier, phone, product):
    status = random.choice(STATUSES)
    order_date = random_date(180, 30)
    carrier = random.choice(CARRIERS)

    if status == "Delivered":
        delivered_date = random_date(29, 1)
        estimated_delivery = "N/A"
        tracking_number = "1Z" + ''.join(
            random.choices('0123456789', k=16))
    elif status == "Shipped":
        delivered_date = "N/A"
        estimated_delivery = (
            datetime.now() + timedelta(
                days=random.randint(1, 14)
            )
        ).strftime("%m.%d.%Y")
        tracking_number = "1Z" + ''.join(
            random.choices('0123456789', k=16))
    elif status == "Processing":
        delivered_date = "N/A"
        estimated_delivery = (
            datetime.now() + timedelta(
                days=random.randint(3, 10)
            )
        ).strftime("%m.%d.%Y")
        tracking_number = "N/A"
    else:
        delivered_date = "N/A"
        estimated_delivery = (
            datetime.now() + timedelta(
                days=random.randint(7, 21)
            )
        ).strftime("%m.%d.%Y")
        tracking_number = "N/A"

    warranty_expiry = "N/A"
    if product == "Lightning":
        order_dt = datetime.strptime(order_date, "%m.%d.%Y")
        warranty_dt = order_dt + timedelta(days=365)
        warranty_expiry = warranty_dt.strftime("%m.%d.%Y")

    price = str(round(random.uniform(29.99, 299.99), 2))

    test_cards = {
        "Visa": "4111111111111111",
        "Mastercard": "5500005555555559",
        "Amex": "340000000000009",
        "Discover": "6011000990139424"
    }
    card_type = random.choice(list(test_cards.keys()))
    credit_card = test_cards[card_type]
    exp_month = str(random.randint(1, 12)).zfill(2)
    exp_year = str(random.randint(27, 30))
    cc_expiry = f"{exp_month}/{exp_year}"
    cc_ccv = ''.join(random.choices(
        '0123456789', k=4 if card_type == "Amex" else 3))

    contact_reasons = [
        "Order status enquiry", "Technical support",
        "Billing question", "Warranty claim",
        "Return request", "General enquiry",
        "Product setup", "Shipping delay"
    ]

    return {
        "externalId": external_id,
        "customerRef": order_ref,
        "customerName": name,
        "customerEmail": email,
        "customerTier": tier,
        "customerPhone": phone,
        "product": product,
        "productSerialNumber": random_serial(product),
        "warrantyExpiry": warranty_expiry,
        "price": price,
        "orderDate": order_date,
        "deliveredDate": delivered_date,
        "status": status,
        "creditCard": credit_card,
        "cc_expiry": cc_expiry,
        "cc_ccv": cc_ccv,
        "trackingNumber": tracking_number,
        "estimatedDelivery": estimated_delivery,
        "shippingCarrier": carrier,
        "shippingAddress": random_address(),
        "signatureRequired": random.choice(["Yes", "No"]),
        "previousTickets": str(random.randint(0, 8)),
        "lastContactDate": random_date(90, 1),
        "lastContactReason": random.choice(contact_reasons),
        "satisfactionScore": random.choice(SATISFACTION_SCORES)
    }

# ============================================================
# ZENDESK — GET OR CREATE USER
# ============================================================
def get_or_create_user(name, email, phone, tier,
                       order_ref, external_id):
    tags = [tier.lower()]

    payload = {
        "user": {
            "name": name,
            "email": email,
            "phone": phone,
            "role": "end-user",
            "verified": True,
            "external_id": external_id,
            "tags": tags,
            "notes": f"{tier} customer — Order {order_ref}"
        }
    }

    search_url = (
        f"{BASE_URL}/users/search.json?query=email:{email}"
    )
    search_resp = requests.get(search_url, headers=headers)
    existing_id = None

    if search_resp.status_code == 200:
        results = search_resp.json().get("users", [])
        if results:
            existing_id = results[0]["id"]

    if existing_id:
        url = f"{BASE_URL}/users/{existing_id}.json"
        resp = requests.put(url, headers=headers, json=payload)
    else:
        url = f"{BASE_URL}/users.json"
        resp = requests.post(url, headers=headers, json=payload)

    if resp.status_code in [200, 201]:
        return resp.json().get("user", {}).get("id")
    else:
        print(f"    ❌ User failed: {name} — {resp.status_code}")
        return None

# ============================================================
# ZENDESK — CREATE TICKET
# ============================================================
def create_ticket(requester_id, subject, body,
                  tier, product, order_ref):
    tags = ["ai_agent_demo", product.lower()]
    if tier == "Platinum":
        tags.extend(["platinum", "platinum_routed"])
    else:
        tags.append("standard")

    priority = "high" if tier == "Platinum" else "normal"

    payload = {
        "ticket": {
            "subject": subject,
            "comment": {
                "body": f"{body}\n\nOrder Reference: {order_ref}"
            },
            "requester_id": requester_id,
            "priority": priority,
            "tags": tags
        }
    }

    resp = requests.post(
        f"{BASE_URL}/tickets.json",
        headers=headers,
        json=payload
    )

    if resp.status_code == 201:
        return resp.json().get("ticket", {}).get("id")
    else:
        print(f"    ❌ Ticket failed: {resp.status_code}")
        return None

# ============================================================
# GITHUB — BATCH UPDATE DATA.JSON
# ============================================================
def update_github_data(new_records):
    print("\n📋 Updating GitHub data.json...")

    github_headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Content-Type": "application/json"
    }

    url = (f"https://api.github.com/repos/"
           f"{GITHUB_REPO}/contents/{GITHUB_FILE}")
    resp = requests.get(url, headers=github_headers)

    if resp.status_code != 200:
        print(f"❌ Failed to fetch GitHub file: {resp.text}")
        return False

    file_data = resp.json()
    current_sha = file_data["sha"]
    current_content = base64.b64decode(
        file_data["content"]
    ).decode("utf-8")
    existing_data = json.loads(current_content)
    existing_data.update(new_records)

    updated_content = json.dumps(existing_data, indent=2)
    encoded_content = base64.b64encode(
        updated_content.encode("utf-8")
    ).decode("utf-8")

    update_payload = {
        "message": f"Add {len(new_records)} new demo customer records",
        "content": encoded_content,
        "sha": current_sha
    }

    update_resp = requests.put(
        url,
        headers=github_headers,
        json=update_payload
    )

    if update_resp.status_code == 200:
        print(f"✅ GitHub updated — {len(new_records)} new records added")
        return True
    else:
        print(f"❌ GitHub update failed: {update_resp.text}")
        return False

# ============================================================
# PROGRESS SAVE — resume if interrupted
# ============================================================
def save_progress(progress):
    with open("ticket_progress.json", "w") as f:
        json.dump(progress, f, indent=2)

def load_progress():
    try:
        with open("ticket_progress.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"completed": 0, "results": [], "new_records": {}}

# ============================================================
# MAIN RUN
# ============================================================
def run():
    print("\n" + "="*60)
    print("ACME — 1000 TICKET CREATION SCRIPT")
    print(f"Delay between tickets: {DELAY_MIN}-{DELAY_MAX} seconds")
    print(f"Estimated total time: "
          f"{round(TOTAL_TICKETS * DELAY_MIN / 3600, 1)}-"
          f"{round(TOTAL_TICKETS * DELAY_MAX / 3600, 1)} hours")
    print("="*60)

    # Load progress in case of resume
    progress = load_progress()
    start_index = progress["completed"]
    results = progress["results"]
    new_records = progress["new_records"]

    if start_index > 0:
        print(f"\n▶️  Resuming from ticket {start_index + 1}")

    tier_list = (["Platinum"] * 250) + (["Standard"] * 750)
    random.shuffle(tier_list)

    used_emails = set(r.get("email", "") for r in results)
    used_names = set(r.get("user", "") for r in results)

    tickets_created = 0
    tickets_failed = 0

    for i in range(start_index, TOTAL_TICKETS):
        print(f"\n[{i+1}/{TOTAL_TICKETS}] "
              f"{datetime.now().strftime('%H:%M:%S')}")

        # Generate user
        attempts = 0
        while attempts < 100:
            first = random.choice(FIRST_NAMES)
            last = random.choice(LAST_NAMES)
            full_name = f"{first} {last}"
            base_email = f"{first.lower()}.{last.lower()}"
            email = f"{base_email}@acmeclient.com"
            counter = 1
            while email in used_emails:
                email = f"{base_email}{counter}@acmeclient.com"
                counter += 1
            if full_name not in used_names:
                used_names.add(full_name)
                used_emails.add(email)
                break
            attempts += 1

        tier = tier_list[i]
        product = random.choice(PRODUCTS)
        phone = random_phone()
        order_ref = random_order_ref()
        external_id = f"ACME-CUST-{str(i + 85).zfill(5)}"

        # Generate data record
        record = generate_order_record(
            external_id, order_ref, full_name,
            email, tier, phone, product
        )
        new_records[order_ref] = record

        # Create user
        user_id = get_or_create_user(
            full_name, email, phone,
            tier, order_ref, external_id
        )

        if not user_id:
            tickets_failed += 1
            progress["completed"] = i + 1
            save_progress(progress)
            continue

        # Create ticket
        subjects = (TICKET_SUBJECTS[product] +
                    TICKET_SUBJECTS["General"])
        subject = random.choice(subjects)
        body = TICKET_BODIES.get(product, TICKET_BODIES["General"])

        ticket_id = create_ticket(
            user_id, subject, body,
            tier, product, order_ref
        )

        if ticket_id:
            tickets_created += 1
            result = {
                "ticket_id": ticket_id,
                "user": full_name,
                "email": email,
                "tier": tier,
                "product": product,
                "order_ref": order_ref,
                "external_id": external_id,
                "subject": subject
            }
            results.append(result)
            print(f"  ✅ Ticket {ticket_id}: "
                  f"{full_name} ({tier}) — {subject[:45]}")
        else:
            tickets_failed += 1

        # Save progress after every ticket
        progress["completed"] = i + 1
        progress["results"] = results
        progress["new_records"] = new_records
        save_progress(progress)

        # Batch update GitHub every 50 tickets
        if (i + 1) % 50 == 0:
            update_github_data(new_records)
            new_records = {}
            progress["new_records"] = {}
            save_progress(progress)

        # Delay between tickets
        if i < TOTAL_TICKETS - 1:
            delay = random.randint(DELAY_MIN, DELAY_MAX)
            print(f"  ⏳ Waiting {delay}s before next ticket...")
            time.sleep(delay)

    # Final GitHub update
    if new_records:
        update_github_data(new_records)

    # Save final results
    with open("ticket_results_1000.json", "w") as f:
        json.dump(results, f, indent=2)

    print("\n" + "="*60)
    print("COMPLETE")
    print("="*60)
    print(f"  ✅ Tickets created: {tickets_created}")
    print(f"  ❌ Failed:          {tickets_failed}")
    print(f"  📁 Results saved to: ticket_results_1000.json")
    print("="*60)

if __name__ == "__main__":
    run()