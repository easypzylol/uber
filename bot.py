import os
from flask import Flask, request
import telebot
from telebot import types

# Get bot token from environment variable
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
# Add your admin user ID here
ADMIN_ID = 7016264130  # Replace with your actual Telegram user ID

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Store user info for replies and broadcast
user_messages = {}
broadcast_users = set()
user_chat_states = {}  # Track user conversation states
user_locations = {}    # Store user locations

# ===== UBER EATS DEALS =====
UBER_EATS_OFFERS = {
    "student": {
        "title": "🎓 **Uber Eats Student - 50% OFF All Orders**",
        "details": """**🍽️ UBER EATS - 50% OFF FOR STUDENTS**

🎯 **STUDENT EXCLUSIVE - 50% OFF EVERY ORDER:**
• Every student order: 50% OFF entire cart
• Campus Delivery: Free within 2 miles
• Dorm Room Delivery: Direct to your room
• Library Drop-off: Study session meals
• Exam Week: Additional 10% OFF (Total 60% OFF)

💰 **STUDENT PERMANENT DISCOUNTS:**
• All Orders: 50% OFF every time
• No minimum order requirement
• No limit on number of uses
• Valid on all restaurants
• Stack with restaurant promotions

📍 **CAMPUS COVERAGE:**
• All major universities in 50 states
• Campus food courts & dining halls
• Late night campus delivery (until 4 AM)
• 24/7 student support"""
    },
    "family": {
        "title": "👨‍👩‍👧‍👦 **Family Meals - 50% OFF Every Time**",
        "details": """**🍕 FAMILY MEAL DEALS - 50% OFF**

🏠 **FAMILY 50% OFF GUARANTEE:**
• Every family order: 50% OFF total
• Feed 4 for $25 guaranteed
• Kids eat free with adult meal
• Weekly meal plan: Additional 20% OFF
• Bulk orders: Extra 10% OFF (Total 60% OFF)

🍽️ **FAMILY-FRIENDLY RESTAURANTS:**
• Pizza chains: Large pizza deals
• Asian cuisine: Family combo platters
• Mexican: Taco family packs
• American: Burger family meals
• Italian: Pasta family sizes

💰 **PERMANENT DISCOUNTS:**
• All family orders: 50% OFF
• No membership required
• No usage limits
• Valid every day
• All restaurant categories"""
    },
    "healthy": {
        "title": "🥗 **Healthy Eats - 50% OFF Always**",
        "details": """**🌱 HEALTHY EATS - 50% OFF PERMANENT**

🥗 **HEALTHY 50% OFF GUARANTEE:**
• Every healthy order: 50% OFF
• Salad bars: Build your own bowl
• Smoothie shops: Protein packed
• Organic cafes: Farm to table
• Vegan restaurants: Plant-based
• Gluten-free: Special diet options

💪 **FITNESS NUTRITION:**
• Gym meal prep: 50% OFF all orders
• Post-workout: Protein recovery
• Low-carb: Keto friendly options
• Clean eating: No processed foods
• Detox: Juice cleanses

💰 **HEALTH DISCOUNTS:**
• Permanent: 50% OFF all healthy orders
• No verification needed
• Use unlimited times
• Valid on all healthy restaurants"""
    },
    "fastfood": {
        "title": "🍔 **Fast Food - 50% OFF All Combos**",
        "details": """**⚡ FAST FOOD - 50% OFF EVERY TIME**

🍟 **PARTNER RESTAURANTS - 50% OFF:**
• McDonald's: 50% OFF entire order
• Burger King: 50% OFF all items
• Wendy's: 50% OFF combos
• Taco Bell: 50% OFF cravings
• KFC: 50% OFF bucket meals
• Subway: 50% OFF footlongs

🎯 **FAST FOOD 50% OFF:**
• Combo meals: 50% OFF always
• Family packs: 50% OFF every order
• Late night: After 10 PM same 50% OFF
• Breakfast: Morning deals same 50% OFF
• Happy hour: 2-5 PM same 50% OFF

📱 **PERMANENT DISCOUNTS:**
• All fast food: 50% OFF
• No app required
• No first-time restrictions
• Use daily, weekly, monthly"""
    },
    "local": {
        "title": "📍 **Local Restaurants - 50% OFF Always**",
        "details": """**🏙️ LOCAL RESTAURANTS - 50% OFF PERMANENT**

🍽️ **LOCAL FAVORITES - 50% OFF:**
• Family-owned restaurants: 50% OFF
• Ethnic cuisine specialists: 50% OFF
• Neighborhood gems: 50% OFF
• Hidden food spots: 50% OFF
• Community favorites: 50% OFF

💰 **LOCAL PERMANENT DISCOUNTS:**
• Every local order: 50% OFF
• Support local businesses
• No minimum purchase
• No usage limits
• All cuisines included

📍 **LOCAL AREAS:**
• All 50 states covered
• Urban & suburban areas
• Small town restaurants
• Rural delivery options
• Community supported"""
    }
}

# ===== UBER RIDES DEALS =====
UBER_RIDES_OFFERS = {
    "airport": {
        "title": "✈️ **Airport Rides - 50% OFF Always**",
        "details": """**🛄 AIRPORT TRANSFERS - 50% OFF EVERY TIME**

🏢 **AIRPORTS - 50% OFF GUARANTEE:**
• Every airport ride: 50% OFF
• All major US airports (50+)
• International terminals
• Domestic terminals
• Private jet centers
• Helicopter pads

🚗 **AIRPORT SERVICES - 50% OFF:**
• UberX to/from airport: 50% OFF always
• Uber Comfort: Extra space 50% OFF
• Uber Black: Luxury 50% OFF
• Uber XL: Groups 50% OFF
• Wait time: 30 min free waiting

💰 **PERMANENT AIRPORT DISCOUNTS:**
• All airport rides: 50% OFF
• Round trip: 50% OFF both ways
• Frequent flyer: Same 50% OFF
• Early bird: 6 AM flights 50% OFF
• Late night: Same 50% OFF"""
    },
    "daily": {
        "title": "🚗 **Daily Commute - 50% OFF Always**",
        "details": """**🏙️ DAILY COMMUTE - 50% OFF EVERY RIDE**

🏠 **COMMUTE - 50% OFF GUARANTEE:**
• Every commute ride: 50% OFF
• Home to Work: Permanent 50% OFF
• School runs: Permanent 50% OFF
• Grocery trips: Permanent 50% OFF
• Gym commute: Permanent 50% OFF
• Shopping trips: Permanent 50% OFF

🚘 **COMMUTE VEHICLES - 50% OFF:**
• UberX: Standard 50% OFF always
• Uber Pool: Shared 50% OFF always
• Uber Green: Electric 50% OFF always
• Uber Comfort: Premium 50% OFF always
• Uber Assist: Special needs 50% OFF

💰 **PERMANENT COMMUTE DISCOUNTS:**
• Every daily ride: 50% OFF
• No peak hour restrictions
• No distance limitations
• Use unlimited times
• All vehicle types"""
    },
    "night": {
        "title": "🌙 **Night Rides - 50% OFF Always**",
        "details": """**🌙 NIGHT RIDES - 50% OFF EVERY NIGHT**

🕒 **NIGHT HOURS - 50% OFF GUARANTEE:**
• Every night ride: 50% OFF
• 10 PM - 4 AM: Permanent 50% OFF
• Weekend nights: Same 50% OFF
• Bar/Club areas: Same 50% OFF
• Safe ride home: Priority dispatch

🚖 **NIGHT SERVICES - 50% OFF:**
• UberX Night: 50% OFF always
• Uber Comfort Night: 50% OFF always
• Uber Black Night: 50% OFF always
• Shared rides: 50% OFF always

🎯 **NIGHT SAFETY:**
• Share trip with friends
• Safety check-in feature
• Emergency assistance
• Well-lit pickup points
• All with 50% OFF"""
    },
    "group": {
        "title": "👥 **Group Rides - 50% OFF Always**",
        "details": """**👥 GROUP RIDES - 50% OFF EVERY TIME**

🎉 **GROUP - 50% OFF GUARANTEE:**
• Every group ride: 50% OFF
• Weddings: Permanent 50% OFF
• Parties: Permanent 50% OFF
• Corporate events: Permanent 50% OFF
• Family gatherings: Permanent 50% OFF
• Sports events: Permanent 50% OFF

🚐 **GROUP VEHICLES - 50% OFF:**
• UberXL (6 seats): 50% OFF always
• UberSUV (7 seats): 50% OFF always
• Multiple vehicles: 50% OFF each
• Charter services: 50% OFF

💰 **PERMANENT GROUP DISCOUNTS:**
• All group rides: 50% OFF
• 4+ people: 50% OFF total
• 6+ people: 50% OFF total
• Hourly rentals: 50% OFF
• Event packages: 50% OFF"""
    },
    "long": {
        "title": "🛣️ **Long Distance - 50% OFF Always**",
        "details": """**🛣️ LONG DISTANCE - 50% OFF EVERY TRIP**

📍 **DISTANCE - 50% OFF GUARANTEE:**
• Every long trip: 50% OFF
• Interstate trips: 50% OFF always
• Cross-state travel: 50% OFF always
• Road trips: 50% OFF always
• Scenic routes: 50% OFF always

🚘 **LONG DISTANCE - 50% OFF:**
• Uber Comfort Long: 50% OFF always
• Uber Black Long: 50% OFF always
• Stop options: Multiple stops 50% OFF
• Scenic route: Tourist attraction stops 50% OFF

💰 **PERMANENT LONG DISTANCE:**
• All long trips: 50% OFF
• 50+ miles: 50% OFF
• 100+ miles: 50% OFF
• Round trips: 50% OFF both ways
• Weekly rentals: 50% OFF"""
    }
}

# ===== STATES COVERAGE =====
STATES_COVERAGE = {
    "east": {
        "name": "East Coast States",
        "states": ["NY", "NJ", "PA", "MA", "CT", "RI", "NH", "VT", "ME", "MD", "DE", "VA", "WV", "NC", "SC", "GA", "FL"],
        "discount": "50% OFF ALL Uber Eats & Rides",
        "major_cities": ["New York City", "Boston", "Philadelphia", "Washington DC", "Miami", "Atlanta"]
    },
    "west": {
        "name": "West Coast States",
        "states": ["CA", "OR", "WA", "NV", "AZ", "UT", "CO", "NM", "HI", "AK"],
        "discount": "50% OFF ALL Services Permanent",
        "major_cities": ["Los Angeles", "San Francisco", "Seattle", "Las Vegas", "Phoenix", "Denver"]
    },
    "midwest": {
        "name": "Midwest States",
        "states": ["IL", "IN", "MI", "OH", "WI", "MN", "IA", "MO", "ND", "SD", "NE", "KS"],
        "discount": "50% OFF EVERY Order & Ride",
        "major_cities": ["Chicago", "Detroit", "Indianapolis", "Minneapolis", "St. Louis", "Cleveland"]
    },
    "south": {
        "name": "Southern States",
        "states": ["TX", "OK", "AR", "LA", "MS", "AL", "TN", "KY"],
        "discount": "50% OFF ALL Users Always",
        "major_cities": ["Dallas", "Houston", "Austin", "New Orleans", "Nashville", "Memphis"]
    }
}

@bot.message_handler(commands=['start'])
def start_command(message):
    if message is None:
        return

    # Add user to broadcast list
    user_id = message.from_user.id
    broadcast_users.add(user_id)
    
    # Reset chat state
    user_chat_states[user_id] = 'started'

    # Create an inline keyboard
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    
    # Main categories
    keyboard.add(types.InlineKeyboardButton("🍽️ Uber Eats 50% OFF", callback_data="main_eats"))
    keyboard.add(types.InlineKeyboardButton("🚗 Uber Rides 50% OFF", callback_data="main_rides"))
    
    # Sub-categories
    keyboard.add(
        types.InlineKeyboardButton("🎓 Student 50% OFF", callback_data="eats_student"),
        types.InlineKeyboardButton("✈️ Airport 50% OFF", callback_data="rides_airport")
    )
    keyboard.add(
        types.InlineKeyboardButton("📍 By State/Region", callback_data="main_states"),
        types.InlineKeyboardButton("🎫 Get 50% OFF Code", callback_data="main_discount")
    )
    keyboard.add(types.InlineKeyboardButton("🚀 How to Get 50% OFF", callback_data="main_how"))
    
    # Contact & Channel
    button_channel = types.InlineKeyboardButton("📢 Join Uber Deals", url="https://t.me/flights_bills_b4u")
    button_contact1 = types.InlineKeyboardButton("💬 Get 50% OFF Code", url="https://t.me/yrfrnd_spidy")
    button_contact2 = types.InlineKeyboardButton("📞 Support", url="https://t.me/Eatsplugsus")
    
    keyboard.add(button_channel)
    keyboard.add(button_contact1, button_contact2)

    # Start message - 50% OFF FOR ALL
    message_text = (
        "🚗 **Uber Deals Bot - 50% OFF FOR ALL** 🍽️\n\n"
        
        "🔥 **PERMANENT DISCOUNT: 50% OFF EVERY ORDER & RIDE!**\n"
        "✅ **NO FIRST-TIME RESTRICTIONS**\n"
        "✅ **NO USAGE LIMITS**\n"
        "✅ **NO MINIMUM REQUIREMENTS**\n\n"
        
        "✅ **UBER EATS - 50% OFF ALWAYS:**\n"
        "• Students: 50% OFF every order\n"
        "• Family meals: 50% OFF always\n"
        "• Healthy eats: 50% OFF permanent\n"
        "• Fast food: 50% OFF all combos\n"
        "• Local restaurants: 50% OFF forever\n\n"
        
        "✅ **UBER RIDES - 50% OFF ALWAYS:**\n"
        "• Airport transfers: 50% OFF every time\n"
        "• Daily commute: 50% OFF all rides\n"
        "• Night rides: 50% OFF 10PM-4AM\n"
        "• Group travel: 50% OFF always\n"
        "• Long distance: 50% OFF every trip\n\n"
        
        "📍 **COVERAGE:** All 50 US States\n"
        "⏰ **VALIDITY:** Permanent - No expiration\n"
        "👥 **ELIGIBILITY:** All users - No restrictions\n\n"
        
        "*Verified Uber Partner - Permanent 50% OFF discounts*\n"
        "*Use unlimited times. No first-time user restrictions.*"
    )

    bot.send_message(message.chat.id, message_text, reply_markup=keyboard, parse_mode='Markdown')

# ===== MAIN HANDLERS =====
@bot.callback_query_handler(func=lambda call: call.data.startswith('main_'))
def main_handler(call):
    """Handle main category clicks"""
    option = call.data.replace('main_', '')
    
    if option == "eats":
        response = """🍽️ **UBER EATS - 50% OFF ALL ORDERS**

🔥 **PERMANENT 50% OFF DISCOUNTS:**

🎓 **STUDENTS - 50% OFF ALWAYS:**
• Every student order: 50% OFF entire cart
• Campus delivery included
• No verification needed after first
• Use unlimited times

👨‍👩‍👧‍👦 **FAMILY MEALS - 50% OFF ALWAYS:**
• Feed 4 for $25 guaranteed
• Kids eat free with adult meal
• Weekly meal plans 50% OFF
• Bulk orders extra discounts

🥗 **HEALTHY EATS - 50% OFF ALWAYS:**
• Organic & fresh meals 50% OFF
• Vegan/vegetarian 50% OFF
• Fitness nutrition 50% OFF
• Special diets 50% OFF

🍔 **FAST FOOD - 50% OFF ALWAYS:**
• All fast food chains 50% OFF
• Combo meals 50% OFF forever
• Late night 50% OFF
• Breakfast 50% OFF

📍 **LOCAL RESTAURANTS - 50% OFF ALWAYS:**
• Neighborhood favorites 50% OFF
• Family-owned spots 50% OFF
• Ethnic cuisine 50% OFF
• Hidden gems 50% OFF

💰 **NO RESTRICTIONS:**
• No first-time user requirements
• No usage limits
• No minimum order value
• Valid every day, all day
• Stack with restaurant promotions

👇 **Select a category for 50% OFF Uber Eats:**"""
        
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("🎓 Student 50% OFF", callback_data="eats_student"),
            types.InlineKeyboardButton("👨‍👩‍👧‍👦 Family 50% OFF", callback_data="eats_family")
        )
        markup.add(
            types.InlineKeyboardButton("🥗 Healthy 50% OFF", callback_data="eats_healthy"),
            types.InlineKeyboardButton("🍔 Fast Food 50% OFF", callback_data="eats_fastfood")
        )
        markup.add(
            types.InlineKeyboardButton("📍 Local 50% OFF", callback_data="eats_local"),
            types.InlineKeyboardButton("💰 All 50% OFF", callback_data="eats_all")
        )
        markup.add(
            types.InlineKeyboardButton("💬 Get Your 50% OFF Code", url="https://t.me/yrfrnd_spidy"),
            types.InlineKeyboardButton("📢 Updates", url="https://t.me/flights_bills_b4u")
        )
        
        bot.send_message(call.message.chat.id, response, reply_markup=markup, parse_mode='Markdown')
    
    elif option == "rides":
        response = """🚗 **UBER RIDES - 50% OFF ALL RIDES**

🔥 **PERMANENT 50% OFF DISCOUNTS:**

✈️ **AIRPORT - 50% OFF ALWAYS:**
• Every airport ride: 50% OFF
• All major airports covered
• Luxury options 50% OFF
• Round trip 50% OFF both ways

🚗 **DAILY COMMUTE - 50% OFF ALWAYS:**
• Home to work: 50% OFF every day
• Monthly unlimited 50% OFF
• Peak hour 50% OFF
• Eco-friendly 50% OFF

🌙 **NIGHT RIDES - 50% OFF ALWAYS:**
• 10 PM - 4 AM: 50% OFF every night
• Safety features included
• Bar/club areas 50% OFF
• Weekend nights 50% OFF

👥 **GROUP TRAVEL - 50% OFF ALWAYS:**
• 4+ people: 50% OFF always
• Event transportation 50% OFF
• Wedding specials 50% OFF
• Corporate rates 50% OFF

🛣️ **LONG DISTANCE - 50% OFF ALWAYS:**
• Interstate travel 50% OFF
• Road trip packages 50% OFF
• Scenic routes 50% OFF
• Multi-stop trips 50% OFF

💰 **NO RESTRICTIONS:**
• No first-time user requirements
• No usage limits
• No distance limitations
• Valid 24/7, all days
• All vehicle types included

👇 **Select a category for 50% OFF Uber Rides:**"""
        
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("✈️ Airport 50% OFF", callback_data="rides_airport"),
            types.InlineKeyboardButton("🚗 Commute 50% OFF", callback_data="rides_daily")
        )
        markup.add(
            types.InlineKeyboardButton("🌙 Night 50% OFF", callback_data="rides_night"),
            types.InlineKeyboardButton("👥 Group 50% OFF", callback_data="rides_group")
        )
        markup.add(
            types.InlineKeyboardButton("🛣️ Long Distance 50% OFF", callback_data="rides_long"),
            types.InlineKeyboardButton("💰 All Rides 50% OFF", callback_data="rides_all")
        )
        markup.add(
            types.InlineKeyboardButton("💬 Get Your 50% OFF Code", url="https://t.me/yrfrnd_spidy"),
            types.InlineKeyboardButton("📢 Updates", url="https://t.me/flights_bills_b4u")
        )
        
        bot.send_message(call.message.chat.id, response, reply_markup=markup, parse_mode='Markdown')
    
    elif option == "states":
        response = """📍 **UBER DEALS BY STATE - 50% OFF EVERYWHERE**

🇺🇸 **ALL 50 STATES - 50% OFF GUARANTEED:**

**EAST COAST - 50% OFF:**
• New York, New Jersey, Pennsylvania
• Massachusetts, Connecticut, Rhode Island
• All New England states
• Florida to Georgia coverage

**WEST COAST - 50% OFF:**
• California, Oregon, Washington
• Nevada, Arizona, Utah
• Colorado, New Mexico
• Hawaii & Alaska

**MIDWEST - 50% OFF:**
• Illinois, Indiana, Michigan
• Ohio, Wisconsin, Minnesota
• Iowa, Missouri, Kansas
• All central states

**SOUTHERN - 50% OFF:**
• Texas, Oklahoma, Arkansas
• Louisiana, Mississippi, Alabama
• Tennessee, Kentucky
• All southern states

💰 **PERMANENT 50% OFF IN EVERY STATE:**
• Uber Eats: 50% OFF all orders
• Uber Rides: 50% OFF all rides
• No state restrictions
• No residency requirements
• Valid for visitors and residents

🎯 **HOW IT WORKS:**
1. Select your region
2. Get region-specific 50% OFF code
3. Use code in Uber/Uber Eats app
4. Save 50% every time

👇 **Select your region for 50% OFF deals:**"""
        
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("🗽 East Coast 50% OFF", callback_data="region_east"),
            types.InlineKeyboardButton("🌅 West Coast 50% OFF", callback_data="region_west")
        )
        markup.add(
            types.InlineKeyboardButton("🌽 Midwest 50% OFF", callback_data="region_midwest"),
            types.InlineKeyboardButton("🤠 Southern 50% OFF", callback_data="region_south")
        )
        markup.add(
            types.InlineKeyboardButton("📍 Set My State", callback_data="state_set"),
            types.InlineKeyboardButton("💬 Get State Code", url="https://t.me/yrfrnd_spidy")
        )
        
        bot.send_message(call.message.chat.id, response, reply_markup=markup, parse_mode='Markdown')
    
    elif option == "discount":
        response = """🎫 **50% OFF UBER CODES - PERMANENT DISCOUNTS**

🔥 **PERMANENT 50% OFF CODES:**

**UBER EATS - 50% OFF ALWAYS:**
• `EATS50ALL` - 50% OFF ALL orders
• `STUDENT50` - Students 50% OFF always
• `FAMILY50` - Family meals 50% OFF always
• `HEALTHY50` - Healthy eats 50% OFF always
• `FASTFOOD50` - Fast food 50% OFF always
• `LOCAL50` - Local restaurants 50% OFF always

**UBER RIDES - 50% OFF ALWAYS:**
• `RIDE50ALL` - 50% OFF ALL rides
• `AIRPORT50` - Airport 50% OFF always
• `COMMUTE50` - Commute 50% OFF always
• `NIGHT50` - Night rides 50% OFF always
• `GROUP50` - Group travel 50% OFF always
• `LONG50` - Long distance 50% OFF always

💰 **HOW TO APPLY - PERMANENT 50% OFF:**

**For Uber Eats:**
1. Open Uber Eats app
2. Add items to cart
3. Go to checkout
4. Enter promo code in "Promotions"
5. **50% OFF applies automatically - EVERY TIME**

**For Uber Rides:**
1. Open Uber app
2. Enter destination
3. Tap "Payment"
4. Add promo code
5. **50% OFF applies automatically - EVERY TIME**

⚠️ **NO RESTRICTIONS:**
• No first-time user requirements
• No usage limits - use daily
• No minimum order/ride value
• No expiration date
• Valid 24/7 in all 50 states

💎 **PRO TIPS FOR MAXIMUM SAVINGS:**
1. Use same code every time - it never expires
2. Combine with restaurant promotions
3. Order during off-peak hours for faster service
4. Share codes with friends - they work for everyone
5. No need to find new codes - these are permanent

🎁 **BONUS FEATURES:**
• Works for new AND existing users
• No account age restrictions
• No location restrictions within US
• All restaurant and ride types included
• Customer support for code issues

👇 **Need help getting or applying your 50% OFF code?**"""
        
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("💬 Get Your 50% OFF Code", url="https://t.me/yrfrnd_spidy"),
            types.InlineKeyboardButton("📢 New Codes", url="https://t.me/flights_bills_b4u")
        )
        markup.add(
            types.InlineKeyboardButton("🍽️ Uber Eats Codes", callback_data="main_eats"),
            types.InlineKeyboardButton("🚗 Uber Rides Codes", callback_data="main_rides")
        )
        
        bot.send_message(call.message.chat.id, response, reply_markup=markup, parse_mode='Markdown')
    
    elif option == "how":
        response = """🚀 **HOW TO GET 50% OFF - STEP BY STEP**

🎯 **FOLLOW THESE STEPS FOR PERMANENT 50% OFF:**

**STEP 1: GET YOUR CODE**
1. Contact our support team
2. Provide your Uber account email
3. Receive your permanent 50% OFF code
4. Code is linked to your account permanently

**STEP 2: APPLY TO UBER EATS**
1. Open Uber Eats app
2. Add items to cart
3. Go to checkout page
4. Tap "Add Promo Code"
5. Enter your 50% OFF code
6. **50% OFF applies automatically FOREVER**

**STEP 3: APPLY TO UBER RIDES**
1. Open Uber app
2. Enter destination
3. Select vehicle type
4. Tap "Payment" method
5. Add your 50% OFF code
6. **50% OFF applies automatically FOREVER**

💰 **KEY FEATURES OF OUR 50% OFF:**
• **Permanent**: Never expires
• **Unlimited**: Use as many times as you want
• **No Restrictions**: No minimums, no blackout dates
• **All Services**: Works on Uber Eats AND Uber Rides
• **All Users**: New AND existing Uber accounts

⚠️ **IMPORTANT NOTES:**
• Codes are account-specific
• One code works for both Eats and Rides
• Support team activation required
• 24/7 support for any issues
• No geographical restrictions within US

🔒 **SECURITY & VERIFICATION:**
• Codes are securely linked to your account
• No sharing of personal payment info
• Uber-verified partner discounts
• Secure activation process
• Privacy protected

⏰ **PROCESSING TIME:**
• Code activation: 2-24 hours
• Support response: Under 1 hour
• Issues resolution: Under 4 hours
• 24/7 support available

📞 **NEED HELP?**
1. Contact @yrfrnd_spidy for codes
2. Contact @Eatsplugsus for support
3. Join @flights_bills_b4u for updates
4. Check /start for all options

👇 **Ready to get your permanent 50% OFF?**"""
        
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("💬 Get My 50% OFF Code NOW", url="https://t.me/yrfrnd_spidy"),
            types.InlineKeyboardButton("📞 Support Help", url="https://t.me/Eatsplugsus")
        )
        markup.add(
            types.InlineKeyboardButton("📢 Join for Updates", url="https://t.me/flights_bills_b4u"),
            types.InlineKeyboardButton("🔙 Back to Main", callback_data="back_main")
        )
        
        bot.send_message(call.message.chat.id, response, reply_markup=markup, parse_mode='Markdown')

# ===== UBER EATS HANDLERS =====
@bot.callback_query_handler(func=lambda call: call.data.startswith('eats_'))
def eats_handler(call):
    """Handle Uber Eats category clicks"""
    option = call.data.replace('eats_', '')
    
    if option in UBER_EATS_OFFERS:
        offer = UBER_EATS_OFFERS[option]
        
        response = f"{offer['title']}\n\n{offer['details']}"
        
        # Add permanent discount message
        response += """\n\n💰 **PERMANENT 50% OFF FEATURES:**
• Works for ALL users - new and existing
• NO usage limits - use daily if needed
• NO minimum order requirements
• NO expiration date - permanent discount
• ALL restaurants included
• Stack with restaurant promotions"""

        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("📱 Open Uber Eats", url="https://ubereats.com"),
            types.InlineKeyboardButton("💬 Get 50% OFF Code", url="https://t.me/yrfrnd_spidy")
        )
        markup.add(
            types.InlineKeyboardButton("💰 More 50% OFF Deals", callback_data="main_eats"),
            types.InlineKeyboardButton("🎫 All 50% OFF Codes", callback_data="main_discount")
        )
        
        bot.send_message(call.message.chat.id, response, reply_markup=markup, parse_mode='Markdown')
    
    elif option == "all":
        response = """🍽️ **ALL UBER EATS - 50% OFF EVERYTHING**

🔥 **COMPREHENSIVE 50% OFF COVERAGE:**

🎓 **STUDENTS - 50% OFF ALL ORDERS:**
• Campus delivery 50% OFF
• Dorm room service 50% OFF
• Exam week 50% OFF
• Group study meals 50% OFF

👨‍👩‍👧‍👦 **FAMILY MEALS - 50% OFF ALL ORDERS:**
• Family bundles 50% OFF
• Kids eat free with 50% OFF adult meals
• Weekly meal plans 50% OFF
• Bulk orders 50% OFF

🥗 **HEALTHY OPTIONS - 50% OFF ALL ORDERS:**
• Organic & fresh 50% OFF
• Vegan/vegetarian 50% OFF
• Fitness nutrition 50% OFF
• Special diets 50% OFF

🍔 **FAST FOOD - 50% OFF ALL ORDERS:**
• Chain restaurants 50% OFF
• Combo meals 50% OFF
• Late night 50% OFF
• Breakfast 50% OFF

📍 **LOCAL RESTAURANTS - 50% OFF ALL ORDERS:**
• Neighborhood favorites 50% OFF
• Family-owned spots 50% OFF
• Ethnic cuisine 50% OFF
• Hidden gems 50% OFF

💰 **NO RESTRICTIONS - PERMANENT 50% OFF:**
• No first-time user requirements
• No usage limits
• No minimum order value
• Valid every day, all day
• All restaurant categories
• Stackable with promotions

🎯 **HOW TO SAVE MAXIMUM:**
1. Get your permanent 50% OFF code
2. Use it on EVERY order
3. Combine with happy hour specials
4. Order during off-peak hours
5. Split large orders for multiple discounts

👇 **Ready for permanent 50% OFF on all Uber Eats?**"""
        
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("💬 Get Permanent 50% OFF", url="https://t.me/yrfrnd_spidy"),
            types.InlineKeyboardButton("📱 Order Now", url="https://ubereats.com")
        )
        markup.add(
            types.InlineKeyboardButton("🎓 Student 50% OFF", callback_data="eats_student"),
            types.InlineKeyboardButton("👨‍👩‍👧‍👦 Family 50% OFF", callback_data="eats_family")
        )
        
        bot.send_message(call.message.chat.id, response, reply_markup=markup, parse_mode='Markdown')

# ===== UBER RIDES HANDLERS =====
@bot.callback_query_handler(func=lambda call: call.data.startswith('rides_'))
def rides_handler(call):
    """Handle Uber Rides category clicks"""
    option = call.data.replace('rides_', '')
    
    if option in UBER_RIDES_OFFERS:
        offer = UBER_RIDES_OFFERS[option]
        
        response = f"{offer['title']}\n\n{offer['details']}"
        
        # Add permanent discount message
        response += """\n\n💰 **PERMANENT 50% OFF FEATURES:**
• Works for ALL users - new and existing
• NO usage limits - ride daily with 50% OFF
• NO distance limitations
• NO time restrictions - 24/7 50% OFF
• ALL vehicle types included
• Priority support available"""

        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("📱 Open Uber", url="https://uber.com"),
            types.InlineKeyboardButton("💬 Get 50% OFF Code", url="https://t.me/yrfrnd_spidy")
        )
        markup.add(
            types.InlineKeyboardButton("💰 More 50% OFF Rides", callback_data="main_rides"),
            types.InlineKeyboardButton("🎫 All 50% OFF Codes", callback_data="main_discount")
        )
        
        bot.send_message(call.message.chat.id, response, reply_markup=markup, parse_mode='Markdown')
    
    elif option == "all":
        response = """🚗 **ALL UBER RIDES - 50% OFF EVERY RIDE**

🔥 **COMPREHENSIVE 50% OFF COVERAGE:**

✈️ **AIRPORT TRANSFERS - 50% OFF ALL:**
• All airports 50% OFF
• Luxury options 50% OFF
• Free waiting time
• Round trip 50% OFF

🚗 **DAILY COMMUTE - 50% OFF ALL:**
• Home-work travel 50% OFF
• Monthly unlimited 50% OFF
• Peak hour 50% OFF
• Eco-friendly 50% OFF

🌙 **NIGHT RIDES - 50% OFF ALL:**
• 10 PM - 4 AM 50% OFF
• Safety features included
• Weekend 50% OFF
• Bar area 50% OFF

👥 **GROUP TRAVEL - 50% OFF ALL:**
• 4+ people 50% OFF
• Event transportation 50% OFF
• Wedding packages 50% OFF
• Corporate rates 50% OFF

🛣️ **LONG DISTANCE - 50% OFF ALL:**
• Interstate travel 50% OFF
• Road trip packages 50% OFF
• Scenic routes 50% OFF
• Multi-stop trips 50% OFF

💰 **NO RESTRICTIONS - PERMANENT 50% OFF:**
• No first-time user requirements
• No usage limits - ride as much as you want
• No distance limitations
• No time restrictions
• All vehicle types
• Priority customer support

🎯 **HOW TO SAVE MAXIMUM:**
1. Get your permanent 50% OFF code
2. Use it on EVERY ride
3. Book in advance for best rates
4. Use Uber Pool for extra savings
5. Travel during off-peak hours

👇 **Ready for permanent 50% OFF on all Uber Rides?**"""
        
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("💬 Get Permanent 50% OFF", url="https://t.me/yrfrnd_spidy"),
            types.InlineKeyboardButton("📱 Book Ride", url="https://uber.com")
        )
        markup.add(
            types.InlineKeyboardButton("✈️ Airport 50% OFF", callback_data="rides_airport"),
            types.InlineKeyboardButton("🚗 Commute 50% OFF", callback_data="rides_daily")
        )
        
        bot.send_message(call.message.chat.id, response, reply_markup=markup, parse_mode='Markdown')

# ===== REGION HANDLERS =====
@bot.callback_query_handler(func=lambda call: call.data.startswith('region_'))
def region_handler(call):
    """Handle region selection clicks"""
    region_key = call.data.replace('region_', '')
    
    if region_key in STATES_COVERAGE:
        region = STATES_COVERAGE[region_key]
        
        response = f"""📍 **{region['name']} - 50% OFF UBER**

🏙️ **MAJOR CITIES - 50% OFF:**
"""
        for city in region['major_cities']:
            response += f"• {city}: 50% OFF ALL Uber services\n"
        
        response += f"\n🗺️ **STATES COVERED - 50% OFF:**\n"
        states_list = ", ".join(region['states'])
        response += f"{states_list}\n\n"
        
        response += f"""💰 **REGION DISCOUNT:** {region['discount']}

🍽️ **UBER EATS IN THIS REGION:**
• Local restaurants: 50% OFF all orders
• Regional cuisine: 50% OFF always
• Community spots: 50% OFF permanent
• All food categories: 50% OFF

🚗 **UBER RIDES IN THIS REGION:**
• Local rides: 50% OFF every ride
• Tourist routes: 50% OFF always
• Commute routes: 50% OFF daily
• All vehicle types: 50% OFF

🎯 **PERMANENT 50% OFF IN {region['name'].upper()}:**
1. All users eligible - new and existing
2. No usage limits - use daily
3. No minimum requirements
4. Valid 24/7, 365 days

💡 **REGION-SPECIFIC TIPS:**
• Use 50% OFF during local events
• Combine with local restaurant deals
• Ask drivers for local food recommendations
• Follow local Uber social media

👇 **Get your 50% OFF code for {region['name']}:**"""
        
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton(f"📍 Get {region['name']} Code", callback_data=f"getcode_{region_key}"),
            types.InlineKeyboardButton("💬 Regional Support", url="https://t.me/yrfrnd_spidy")
        )
        markup.add(
            types.InlineKeyboardButton("🍽️ Eats in Region", callback_data=f"eats_region_{region_key}"),
            types.InlineKeyboardButton("🚗 Rides in Region", callback_data=f"rides_region_{region_key}")
        )
        
        bot.send_message(call.message.chat.id, response, reply_markup=markup, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: call.data.startswith('getcode_'))
def get_code_handler(call):
    region_key = call.data.replace('getcode_', '')
    region_name = STATES_COVERAGE.get(region_key, {}).get('name', 'your region')
    
    bot.send_message(
        call.message.chat.id,
        f"🎫 **Getting 50% OFF Code for {region_name}**\n\n"
        f"Contact our support team for your permanent 50% OFF code:\n\n"
        f"1. Message: @yrfrnd_spidy\n"
        f"2. Provide: Your Uber account email\n"
        f"3. Mention: '{region_name} 50% OFF code'\n"
        f"4. Receive: Permanent 50% OFF code\n\n"
        f"⏰ **Processing:** 2-24 hours\n"
        f"📞 **Support:** @Eatsplugsus\n"
        f"📢 **Updates:** @flights_bills_b4u\n\n"
        f"*Code works for ALL Uber services in {region_name}*"
    )

@bot.callback_query_handler(func=lambda call: call.data == 'state_set')
def state_set_handler(call):
    bot.send_message(
        call.message.chat.id,
        "📍 **Set Your Exact Location for 50% OFF**\n\n"
        "Provide your details for location-specific 50% OFF codes:\n\n"
        "**Required Information:**\n"
        "• State (e.g., California)\n"
        "• City (e.g., Los Angeles)\n"
        "• Zip code (optional)\n"
        "• Uber account email\n\n"
        "**Example:**\n"
        "`California\nLos Angeles\n90001\nemail@example.com`\n\n"
        "**Send to:** @yrfrnd_spidy\n\n"
        "*Get permanent 50% OFF codes for your exact location!*"
    )

# ===== BROADCAST FEATURE =====
@bot.message_handler(commands=['broadcast'])
def broadcast_command(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "Admin feature only.")
        return
    
    if len(broadcast_users) == 0:
        bot.reply_to(message, "No users available.")
        return
    
    msg = bot.send_message(
        ADMIN_ID,
        f"🚗 Send 50% OFF Uber deals to {len(broadcast_users)} users:"
    )
    bot.register_next_step_handler(msg, process_broadcast_message)

def process_broadcast_message(message):
    if hasattr(message, 'is_broadcast_processed') and message.is_broadcast_processed:
        return
    message.is_broadcast_processed = True
    
    broadcast_text = message.text
    users = list(broadcast_users)
    success_count = 0
    fail_count = 0
    
    status_msg = bot.send_message(ADMIN_ID, f"🚗 Sending 50% OFF deals to {len(users)} users...")
    
    for user_id in users:
        try:
            notification = f"🚗 **UBER 50% OFF ALERT** 🍽️\n\n{broadcast_text}\n\n*50% OFF ALL Uber Eats & Rides - Permanent discounts for ALL users!*"
            bot.send_message(user_id, notification)
            success_count += 1
        except Exception:
            fail_count += 1
    
    bot.edit_message_text(
        f"✅ 50% OFF broadcast complete!\n\n"
        f"📊 Results:\n"
        f"• Success: {success_count}\n"
        f"• Failed: {fail_count}\n"
        f"• Total: {len(users)}",
        ADMIN_ID,
        status_msg.message_id
    )

@bot.message_handler(commands=['stats'])
def stats_command(message):
    if message.from_user.id != ADMIN_ID:
        return
    
    user_count = len(broadcast_users)
    location_count = len(user_locations)
    
    bot.send_message(
        ADMIN_ID,
        f"🚗 **Uber 50% OFF Bot Statistics**\n\n"
        f"👥 Total Users: {user_count}\n"
        f"📍 Locations Set: {location_count}\n"
        f"🍽️ Eats Categories: 5 (All 50% OFF)\n"
        f"🚗 Rides Categories: 5 (All 50% OFF)\n"
        f"🗺️ Regions: 4 (All 50 states)\n"
        f"💰 Discount: Permanent 50% OFF\n"
        f"📈 Daily Growth: +{min(user_count, 100)}"
    )

# ===== CHAT HANDLERS =====
@bot.message_handler(func=lambda message: message.text and message.text.lower().startswith('hello'))
def hello_handler(message):
    user = message.from_user
    user_id = user.id
    
    broadcast_users.add(user_id)
    user_chat_states[user_id] = 'waiting_for_admin'
    
    user_info = f"User: {user.first_name} {user.last_name or ''} (@{user.username or 'No username'})"
    
    user_messages[message.message_id] = {
        'user_id': user.id,
        'user_info': user_info,
        'original_message': message.text
    }
    
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("📨 Reply with 50% OFF Code", callback_data=f"reply_{message.message_id}"))
    
    forward_text = f"🚗 New Uber 50% OFF Inquiry\n\n{user_info}\nUser ID: {user.id}\n\n'{message.text}'"
    
    bot.send_message(ADMIN_ID, forward_text, reply_markup=keyboard)
    
    bot.reply_to(
        message,
        "🚗 Hello! Welcome to **Uber 50% OFF Bot**! 🍽️\n\n"
        "🎉 **PERMANENT DISCOUNT:** 50% OFF ALL Uber Eats orders AND ALL Uber rides!\n\n"
        "🔥 **NO RESTRICTIONS:**\n"
        "• No first-time user requirements\n"
        "• No usage limits\n"
        "• No minimum order/ride value\n"
        "• Valid for ALL users\n\n"
        "📍 **Set your location** for state-specific 50% OFF codes\n"
        "💰 **Get your code** for permanent 50% OFF\n"
        "📱 **Use unlimited times** - forever discount!\n\n"
        "*Official Uber partner - Permanent 50% OFF discounts!*"
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith('reply_'))
def reply_callback_handler(call):
    message_id = int(call.data.split('_')[1])
    
    if message_id in user_messages:
        user_data = user_messages[message_id]
        
        msg = bot.send_message(
            ADMIN_ID,
            f"🚗 Reply to {user_data['user_info']} with 50% OFF code\n\n"
            f"💡 Tip: Provide permanent 50% OFF code or instructions!"
        )
        bot.register_next_step_handler(msg, process_admin_reply, user_data['user_id'])
    else:
        bot.answer_callback_query(call.id, "Message not found")

def process_admin_reply(message, user_id):
    try:
        bot.send_message(
            user_id,
            f"🚗 Uber Specialist Reply:\n\n{message.text}\n\n"
            f"*Your permanent 50% OFF code works on ALL Uber services!*"
        )
        bot.reply_to(message, "✅ 50% OFF code sent to user!")
    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")

@bot.message_handler(func=lambda message: True)
def all_messages_handler(message):
    user = message.from_user
    user_id = user.id
    
    if user_id == ADMIN_ID:
        return
    
    broadcast_users.add(user_id)
    
    if user_chat_states.get(user_id) == 'waiting_for_admin' and message.text:
        user_info = f"User: {user.first_name} {user.last_name or ''} (@{user.username or 'No username'})"
        
        user_messages[message.message_id] = {
            'user_id': user_id,
            'user_info': user_info,
            'original_message': message.text
        }
        
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton("📨 Reply", callback_data=f"reply_{message.message_id}"))
        
        forward_text = f"🚗 User Message\n\n{user_info}\nUser ID: {user_id}\n\n'{message.text}'"
        
        bot.send_message(ADMIN_ID, forward_text, reply_markup=keyboard)
        
        if not message.text.lower().startswith('hello'):
            bot.reply_to(
                message,
                "✅ Got your message! Our Uber specialist will help you get:\n"
                "• Permanent 50% OFF Uber Eats code\n"
                "• Permanent 50% OFF Uber Rides code\n"
                "• State-specific discounts\n"
                "• Unlimited usage instructions"
            )

@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Uber 50% OFF Bot | Permanent Discounts for ALL Users</title>
        <meta name="description" content="Get PERMANENT 50% OFF ALL Uber Eats orders and ALL Uber rides. No first-time restrictions, no usage limits, valid for ALL users in all 50 states.">
        <meta name="keywords" content="uber 50% off permanent, uber eats 50% off all orders, uber rides 50% off always, permanent uber discounts, no restrictions uber deals">
        <style>
            body { font-family: Arial, sans-serif; text-align: center; padding: 50px; background: #000; color: white; }
            .container { max-width: 800px; margin: 0 auto; background: #1a1a1a; padding: 30px; border-radius: 10px; }
            .uber-green { color: #00D1B2; }
            .deal-badge { background: #00D1B2; color: black; padding: 15px 30px; border-radius: 25px; display: inline-block; margin: 20px; font-weight: bold; font-size: 24px; }
            .feature-list { text-align: left; max-width: 600px; margin: 30px auto; }
            .feature { background: #333; padding: 15px; margin: 10px; border-radius: 8px; }
            .highlight { color: #00D1B2; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1 class="uber-green">🚗 UBER 50% OFF BOT 🍽️</h1>
            <p>PERMANENT 50% OFF FOR ALL USERS - NO RESTRICTIONS</p>
            
            <div class="deal-badge">🔥 50% OFF EVERY ORDER & RIDE</div>
            
            <h2>✅ NO FIRST-TIME RESTRICTIONS</h2>
            <div class="feature-list">
                <div class="feature">🎯 <span class="highlight">Works for ALL users</span> - New AND existing</div>
                <div class="feature">♾️ <span class="highlight">Unlimited usage</span> - Use daily, forever</div>
                <div class="feature">🚫 <span class="highlight">No minimum requirements</span> - Any order size</div>
                <div class="feature">📅 <span class="highlight">No expiration</span> - Permanent discount</div>
                <div class="feature">📍 <span class="highlight">All 50 states</span> - Complete US coverage</div>
                <div class="feature">🍽️🚗 <span class="highlight">Both services</span> - Uber Eats AND Uber Rides</div>
            </div>
            
            <h2>🗺️ Coverage: All 50 US States</h2>
            <p>East Coast • West Coast • Midwest • Southern States</p>
            
            <h2>💰 Permanent Discounts</h2>
            <p><span class="highlight">Uber Eats:</span> 50% OFF ALL orders - Students, Family, Healthy, Fast Food, Local</p>
            <p><span class="highlight">Uber Rides:</span> 50% OFF ALL rides - Airport, Commute, Night, Group, Long Distance</p>
            
            <h2>🚀 How It Works</h2>
            <p>1. Get your permanent 50% OFF code</p>
            <p>2. Apply in Uber/Uber Eats app</p>
            <p>3. Save 50% on EVERY order/ride</p>
            <p>4. Use unlimited times - Forever!</p>
            
            <p style="margin-top: 30px; color: #888;">
                Official Uber partner discounts. Permanent 50% OFF for all users.
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
            print(f"🚗 Uber 50% OFF Bot deployed: {webhook_url}")
        else:
            print("Uber 50% OFF Bot running in polling mode")
            
    except Exception as e:
        print(f"Webhook setup: {e}")
    
    print("🚗 Uber 50% OFF Bot Active! 🍽️")
    print("💰 Discount: PERMANENT 50% OFF FOR ALL USERS")
    print("📍 Coverage: All 50 US States")
    print("✅ No restrictions: No first-time limits, no usage limits")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
