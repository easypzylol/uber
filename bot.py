import os
from flask import Flask, request
import telebot
from telebot import types

# Get bot token from environment variable
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMIN_ID = 7016264130  # Replace with your actual Telegram user ID

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Store user info
user_messages = {}
broadcast_users = set()

# USA States & Cities for SEO
STATES = [
    "New York", "California", "Texas", "Florida", "Illinois",
    "Pennsylvania", "Ohio", "Georgia", "North Carolina", "Michigan",
    "New Jersey", "Virginia", "Washington", "Arizona", "Massachusetts",
    "Tennessee", "Indiana", "Missouri", "Maryland", "Wisconsin"
]

CITIES = [
    "New York City", "Los Angeles", "Chicago", "Houston", "Phoenix",
    "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose",
    "Austin", "Jacksonville", "Fort Worth", "Columbus", "Charlotte",
    "San Francisco", "Indianapolis", "Seattle", "Denver", "Washington DC"
]

# Popular Dishes for SEO
POPULAR_DISHES = [
    "Pizza", "Burger", "Sushi", "Tacos", "Pasta",
    "Fried Chicken", "Salad", "Sandwich", "Steak", "Burrito",
    "Ramen", "Wings", "Curry", "Pho", "BBQ",
    "Seafood", "Dumplings", "Noodles", "Rice Bowl", "Soup"
]

@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.from_user.id
    broadcast_users.add(user_id)
    
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    
    # Main buttons
    keyboard.add(
        types.InlineKeyboardButton("🍽️ Uber Eats 50% OFF", callback_data="eats_main"),
        types.InlineKeyboardButton("🚗 Uber Rides 50% OFF", callback_data="rides_main")
    )
    
    # Contact buttons
    keyboard.add(
        types.InlineKeyboardButton("📞 Contact for Order", url="https://t.me/yrfrnd_spidy"),
        types.InlineKeyboardButton("📞 Contact for Ride", url="https://t.me/Eatsplugsus")
    )
    
    # States & Cities buttons
    keyboard.add(
        types.InlineKeyboardButton("📍 USA States", callback_data="states_list"),
        types.InlineKeyboardButton("🏙️ USA Cities", callback_data="cities_list")
    )
    
    keyboard.add(
        types.InlineKeyboardButton("📢 Join Channel", url="https://t.me/flights_bills_b4u")
    )

    message_text = (
        "🚗 **Uber Deals - 50% OFF** 🍽️\n\n"
        
        "**We provide Uber Eats & Uber Rides at 50% OFF**\n\n"
        
        "✅ **UBER EATS:**\n"
        "• Food delivery 50% OFF\n"
        "• All restaurants included\n"
        "• All USA cities covered\n\n"
        
        "✅ **UBER RIDES:**\n"
        "• Transportation 50% OFF\n"
        "• All vehicle types\n"
        "• All USA states covered\n\n"
        
        "📍 **Coverage:** All USA states & cities\n"
        "💰 **Discount:** 50% OFF every order/ride\n"
        "📞 **Contact us for booking/orders**\n\n"
        
        "*Limited spots available. Contact now!*"
    )

    bot.send_message(message.chat.id, message_text, reply_markup=keyboard, parse_mode='Markdown')

# ===== MAIN HANDLERS =====
@bot.callback_query_handler(func=lambda call: call.data == 'eats_main')
def eats_main_handler(call):
    response = """🍽️ **UBER EATS - 50% OFF**

**Get 50% OFF on all food delivery:**

🔥 **ALL RESTAURANTS 50% OFF:**
• Fast food: McDonald's, Burger King, etc.
• Local restaurants: All cuisines
• Healthy options: Salads, smoothies
• Late night delivery: 24/7 service

📍 **COVERAGE:** All USA cities
💰 **DISCOUNT:** 50% OFF every order
👥 **ELIGIBILITY:** All users

**POPULAR DISHES 50% OFF:**
• Pizza • Burgers • Sushi • Tacos • Pasta
• Fried Chicken • Salads • Sandwiches • Steak
• All other dishes 50% OFF

**HOW TO ORDER:**
1. Contact us for 50% OFF code
2. Use code in Uber Eats app
3. Get 50% OFF on your order
4. Repeat for unlimited savings

📞 **Contact now for 50% OFF code:**"""
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📞 Contact for Uber Eats Code", url="https://t.me/yrfrnd_spidy"))
    markup.add(types.InlineKeyboardButton("📍 Check Cities", callback_data="cities_list"))
    
    bot.send_message(call.message.chat.id, response, reply_markup=markup, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: call.data == 'rides_main')
def rides_main_handler(call):
    response = """🚗 **UBER RIDES - 50% OFF**

**Get 50% OFF on all Uber rides:**

🔥 **ALL RIDES 50% OFF:**
• Airport transfers: 50% OFF
• Daily commute: 50% OFF
• Night rides: 50% OFF
• Group travel: 50% OFF
• Long distance: 50% OFF

📍 **COVERAGE:** All USA states
💰 **DISCOUNT:** 50% OFF every ride
👥 **ELIGIBILITY:** All users

**RIDE TYPES 50% OFF:**
• UberX • Uber Comfort • Uber Black
• UberXL • Uber SUV • All vehicle types

**HOW TO BOOK:**
1. Contact us for 50% OFF code
2. Use code in Uber app
3. Get 50% OFF on your ride
4. Use unlimited times

📞 **Contact now for 50% OFF code:**"""
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📞 Contact for Uber Rides Code", url="https://t.me/Eatsplugsus"))
    markup.add(types.InlineKeyboardButton("📍 Check States", callback_data="states_list"))
    
    bot.send_message(call.message.chat.id, response, reply_markup=markup, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: call.data == 'states_list')
def states_list_handler(call):
    states_text = "\n".join([f"• {state}" for state in STATES])
    
    response = f"""📍 **USA STATES COVERED - 50% OFF**

**All these states get 50% OFF Uber services:**

{states_text}

**Plus all other USA states covered**

📞 **Contact for 50% OFF in your state:**"""
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📞 Get State-Specific Code", url="https://t.me/yrfrnd_spidy"))
    markup.add(types.InlineKeyboardButton("🚗 Back to Rides", callback_data="rides_main"))
    
    bot.send_message(call.message.chat.id, response, reply_markup=markup, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: call.data == 'cities_list')
def cities_list_handler(call):
    cities_text = "\n".join([f"• {city}" for city in CITIES])
    
    response = f"""🏙️ **USA CITIES COVERED - 50% OFF**

**All these cities get 50% OFF Uber Eats:**

{cities_text}

**Plus all other USA cities covered**

📞 **Contact for 50% OFF in your city:**"""
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📞 Get City-Specific Code", url="https://t.me/yrfrnd_spidy"))
    markup.add(types.InlineKeyboardButton("🍽️ Back to Eats", callback_data="eats_main"))
    
    bot.send_message(call.message.chat.id, response, reply_markup=markup, parse_mode='Markdown')

# ===== CONTACT HANDLER =====
@bot.message_handler(commands=['contact'])
def contact_command(message):
    response = """📞 **CONTACT FOR 50% OFF**

**UBER EATS 50% OFF:**
Contact: @yrfrnd_spidy
• Get 50% OFF food delivery code
• All restaurants included
• All cities covered

**UBER RIDES 50% OFF:**
Contact: @Eatsplugsus
• Get 50% OFF rides code
• All ride types included
• All states covered

**UPDATES & NEW DEALS:**
Channel: @flights_bills_b4u

**Working hours:** 24/7
**Response time:** Under 1 hour
**Discount:** 50% OFF guaranteed

*Contact now for immediate 50% OFF code*"""
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🍽️ Uber Eats Contact", url="https://t.me/yrfrnd_spidy"),
        types.InlineKeyboardButton("🚗 Uber Rides Contact", url="https://t.me/Eatsplugsus")
    )
    markup.add(types.InlineKeyboardButton("📢 Join Channel", url="https://t.me/flights_bills_b4u"))
    
    bot.send_message(message.chat.id, response, reply_markup=markup, parse_mode='Markdown')

# ===== BROADCAST FEATURE =====
@bot.message_handler(commands=['broadcast'])
def broadcast_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    if len(broadcast_users) == 0:
        bot.reply_to(message, "No users available.")
        return
    
    msg = bot.send_message(ADMIN_ID, f"Send message to {len(broadcast_users)} users:")
    bot.register_next_step_handler(msg, process_broadcast_message)

def process_broadcast_message(message):
    if hasattr(message, 'is_broadcast_processed') and message.is_broadcast_processed:
        return
    message.is_broadcast_processed = True
    
    broadcast_text = message.text
    users = list(broadcast_users)
    success_count = 0
    
    for user_id in users:
        try:
            bot.send_message(user_id, f"📢 **Update:**\n\n{broadcast_text}")
            success_count += 1
        except:
            pass
    
    bot.send_message(ADMIN_ID, f"Broadcast sent to {success_count} users")

# ===== DEFAULT HANDLER =====
@bot.message_handler(func=lambda message: True)
def all_messages_handler(message):
    user_id = message.from_user.id
    broadcast_users.add(user_id)
    
    if message.text and message.text.lower() in ['hi', 'hello', 'hey']:
        bot.reply_to(
            message,
            "Hello! Get 50% OFF Uber Eats & Rides.\n\n"
            "Contact @yrfrnd_spidy for Uber Eats 50% OFF\n"
            "Contact @Eatsplugsus for Uber Rides 50% OFF\n\n"
            "All USA cities & states covered."
        )

@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Uber 50% OFF | Eats & Rides Discounts USA</title>
        <meta name="description" content="Get 50% OFF Uber Eats food delivery and Uber Rides transportation in all USA cities and states. Contact for discount codes.">
        <meta name="keywords" content="uber 50% off, uber eats discount, uber rides discount, usa cities, new york, california, texas, florida, chicago, los angeles">
        <style>
            body { font-family: Arial, sans-serif; text-align: center; padding: 20px; }
            .container { max-width: 600px; margin: 0 auto; }
            .contact-box { background: #f0f0f0; padding: 20px; margin: 20px 0; border-radius: 10px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚗 Uber 50% OFF Bot 🍽️</h1>
            <p>Get 50% OFF Uber Eats & Uber Rides</p>
            
            <div class="contact-box">
                <h3>📞 Contact for 50% OFF</h3>
                <p><strong>Uber Eats 50% OFF:</strong> Contact @yrfrnd_spidy</p>
                <p><strong>Uber Rides 50% OFF:</strong> Contact @Eatsplugsus</p>
                <p><strong>Updates:</strong> @flights_bills_b4u</p>
            </div>
            
            <h3>📍 USA Coverage</h3>
            <p>All 50 states • All major cities</p>
            
            <h3>💰 Permanent 50% OFF</h3>
            <p>No restrictions • All users • Unlimited use</p>
            
            <p style="margin-top: 30px;">
                Use Telegram bot for instant 50% OFF codes
            </p>
        </div>
    </body>
    </html>
    """

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    update = request.get_data().decode("utf-8")
    update_obj = telebot.types.Update.de_json(update)
    bot.process_new_updates([update_obj])
    return "OK", 200

if __name__ == "__main__":
    if not TOKEN:
        raise SystemExit("Token required")
    
    try:
        bot.remove_webhook()
        render_domain = os.environ.get("RENDER_EXTERNAL_URL")
        
        if render_domain:
            webhook_url = f"{render_domain}/{TOKEN}"
            bot.set_webhook(url=webhook_url)
            print(f"Uber 50% OFF Bot deployed")
        else:
            print("Bot running in polling mode")
            
    except Exception as e:
        print(f"Webhook setup: {e}")
    
    print("Uber 50% OFF Bot Active")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
