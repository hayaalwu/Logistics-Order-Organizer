import re
import pandas as pd

# General priority keyword groups
Priority_categories = {
    "Urgent": ["urgent", "immediate", "immediately", "critical", "emergency", "rush"],
    "ASAP": ["asap"],
    "High": ["high priority", "end of day", "eod", "today"],
    "Medium": ["tomorrow", "soon", "next day"],
    "Normal": []
}

# General time keyword groups
Time_categories = {
    "Now": ["urgent", "immediate", "immediately", "now"],
    "ASAP": ["asap"],
    "End Of Day": ["end of day", "eod", "by tonight"],
    "Tomorrow Am": ["tomorrow am", "tomorrow morning"],
    "Tomorrow": ["tomorrow", "next day"],
    "Today": ["today"]
}

# Words to remove from item names
Noise_words = [
    "deliver", "send", "bring", "pickup", "pick up",
    "need", "needs", "requires", "request", "requests",
    "urgent", "asap", "high priority", "end of day", "eod",
    "today", "tomorrow", "soon", "next day", "am", "by"
]

# Match text with a category based on keywords
def match_category(text, categories, default):
    text = text.lower()

    for label, keywords in categories.items():
        for keyword in keywords:
            if keyword in text:
                return label # the key

    return default # defult from the function


# Extract priority and assign a sorting rank
def extract_priority(text):
    priority = match_category(text, Priority_categories, "Normal")

    rank = {
        "Urgent": 1,
        "ASAP": 2,
        "High": 3,
        "Medium": 4,
        "Normal": 5
    }[priority] # rank = the number that match the [priority]

    return priority, rank


# Extract delivery time
def extract_time(text):
    return match_category(text, Time_categories, "Not Specified")


# Extract destination stop
def extract_stop(text):

    patterns = [
        r"\b(?:site|stop|location|warehouse|area|zone)\s*([A-Z])\b",
        r"\b(?:to|for|at|from)\s+([A-Z])\b",
        r"^([A-Z])\s+(?:needs|requires|requests)\b"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).upper() # group(1) --> ([A-Z])

    return "Unknown"


# Extract quantity and item name
def extract_item_details(item_text):
    text = item_text.lower().strip()
    quantity_match = re.search(r"\b(\d+)\s*(x|boxes|box|pcs|pieces|units|items)?\b", text) # (\d+) --> 0-9

    if quantity_match:
        quantity = quantity_match.group(1)

        item = re.sub(r"\b\d+\s*(x|boxes|box|pcs|pieces|units|items)?\b", "", text).strip() 

    else:
        quantity = "1"
        item = text

    noise_pattern = r"\b(" + "|".join(map(re.escape, Noise_words)) + r")\b" # clean the item from the noise

    item = re.sub(noise_pattern, "", item).strip()
    item = re.sub(r"^[a-z]\s+", "", item, flags=re.IGNORECASE).strip()
    item = re.sub(r"[()]", "", item).strip()
    item = re.sub(r"\s+", " ", item).strip()

    return quantity, item.title() # title --> make the first letter capital 


# Parse the input text into structured orders
def parse_orders(text):

    rows = []

    # Process each order separately
    for order in text.split(";"):

        order = order.strip()

        if not order:
            continue

        # Extract order information
        stop = extract_stop(order)
        priority, rank = extract_priority(order)
        when = extract_time(order)

        # Remove destination before extracting items
        item_area = re.split(r"\b(to|for|at|from)\b", order, flags=re.IGNORECASE)[0]

        # Handle multiple items in one order
        item_parts = re.split(r"\s*\+\s*|\s+and\s+", item_area, flags=re.IGNORECASE)

        for item_part in item_parts:

            quantity, item = extract_item_details(item_part)

            rows.append({
                "Stop": stop,
                "Item": item,
                "Quantity": quantity,
                "Priority": priority,
                "When": when,
                "Rank": rank
            })

    df = pd.DataFrame(rows)

    df = df.sort_values("Rank").drop(columns=["Rank"])

    return df