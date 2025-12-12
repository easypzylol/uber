import os
from flask import Flask, request
import telebot
from telebot import types

# Get bot token from environment variable
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMIN_ID = 1247375362  # Replace with your actual Telegram user ID

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Store user info
user_messages = {}
broadcast_users = set()

# ===== EXPANDED USA STATES (All 50 states) =====
STATES = [
    "Alabama", "Alaska", "Arizona", "Arkansas", "California",
    "Colorado", "Connecticut", "Delaware", "Florida", "Georgia",
    "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa",
    "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland",
    "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri",
    "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey",
    "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio",
    "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina",
    "South Dakota", "Tennessee", "Texas", "Utah", "Vermont",
    "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"
]

# ===== CITIES WITH MAX TRANSPORTATION USAGE =====
CITIES = [
    # Top 10 Transportation Hubs
    "New York City, NY", "Chicago, IL", "Los Angeles, CA", 
    "Atlanta, GA", "Dallas, TX", "Denver, CO", 
    "San Francisco, CA", "Houston, TX", "Miami, FL",
    "Seattle, WA",
    
    # Major Airport Cities
    "Atlanta (ATL)", "Los Angeles (LAX)", "Chicago (ORD)",
    "Dallas (DFW)", "Denver (DEN)", "New York (JFK)",
    "San Francisco (SFO)", "Las Vegas (LAS)", "Phoenix (PHX)",
    "Orlando (MCO)",
    
    # High Public Transport Cities
    "Washington DC", "Boston, MA", "Philadelphia, PA",
    "Portland, OR", "Minneapolis, MN", "San Diego, CA",
    "Austin, TX", "Nashville, TN", "Charlotte, NC",
    "Detroit, MI",
    
    # College Towns with High Uber Usage
    "Ann Arbor, MI", "Austin, TX", "Madison, WI",
    "Berkeley, CA", "Boston, MA", "Chapel Hill, NC",
    "Ithaca, NY", "State College, PA", "Boulder, CO",
    "Gainesville, FL",
    
    # Tourist Cities with High Ride Demand
    "Las Vegas, NV", "Orlando, FL", "Miami Beach, FL",
    "New Orleans, LA", "San Antonio, TX", "Honolulu, HI",
    "San Diego, CA", "Savannah, GA", "Charleston, SC",
    "Santa Monica, CA"
]

# ===== POPULAR DISHES FOR UBER EATS SEO =====
POPULAR_DISHES = [
    # Fast Food
    "McDonald's Big Mac", "Burger King Whopper", "Wendy's Baconator",
    "Taco Bell Crunchwrap", "KFC Original Recipe", "Subway Footlong",
    "Domino's Pizza", "Pizza Hut Pan Pizza", "Chick-fil-A Sandwich",
    "Popeyes Chicken",
    
    # Healthy Options
    "Caesar Salad", "Acai Bowl", "Protein Smoothie",
    "Avocado Toast", "Greek Yogurt Bowl", "Quinoa Salad",
    "Kale Salad", "Falafel Wrap", "Sushi Rolls",
    "Buddha Bowl",
    
    # International Cuisine
    "Chicken Tikka Masala", "Pad Thai", "Beef Pho",
    "Chicken Teriyaki", "Beef Burrito", "Margherita Pizza",
    "Chicken Shawarma", "Beef Bulgogi", "Chicken Parmigiana",
    "Lamb Gyro",
    
    # American Classics
    "Cheeseburger", "BBQ Ribs", "Fried Chicken",
    "Mac & Cheese", "Hot Dog", "Buffalo Wings",
    "Clam Chowder", "Reuben Sandwich", "Philly Cheesesteak",
    "Cobb Salad"
]

# ===== UBER EATS DEAL CATEGORIES =====
EATS_DEALS = {
    "fastfood": {
        "title": "🍔 **Fast Food - 50% OFF All Chains**",
        "details": """🔥 **ALL FAST FOOD 50% OFF:**

✅ **McDonald's:** Big Mac, Happy Meals, McNuggets
✅ **Burger King:** Whopper, Chicken Fries, Breakfast
✅ **Taco Bell:** Crunchwrap Supreme, Doritos Locos Tacos
✅ **Wendy's:** Baconator, Frosty, 4 for $4
✅ **KFC:** Original Recipe, Popcorn Chicken
✅ **Subway:** All Footlongs, Cookie deals
✅ **Pizza Chains:** Domino's, Pizza Hut, Papa John's

💰 **50% OFF GUARANTEE:**
• Entire order 50% OFF
• No minimum purchase
• All menu items included
• Use unlimited times"""
    },
    "healthy": {
        "title": "🥗 **Healthy Eats - 50% OFF + Free Delivery**",
        "details": """🌱 **HEALTHY OPTIONS 50% OFF:**

✅ **Salad Chains:** Sweetgreen, Chopt, Saladworks
✅ **Smoothie Bars:** Jamba Juice, Smoothie King
✅ **Organic Cafes:** Local organic restaurants
✅ **Vegan Restaurants:** Plant-based options
✅ **Protein Meals:** Bodybuilding nutrition
✅ **Juice Bars:** Cold-pressed juices

🎁 **BONUS OFFERS:**
• 50% OFF entire order
• FREE delivery on healthy orders
• Extra 10% OFF for gym members
• Weekly meal prep discounts"""
    },
    "late": {
        "title": "🌙 **Late Night - 60% OFF (10PM-4AM)**",
        "details": """🌃 **LATE NIGHT SPECIALS:**

⏰ **TIME:** 10:00 PM - 4:00 AM Daily
💰 **DISCOUNT:** 60% OFF (Extra 10% OFF!)

🍕 **LATE NIGHT FOODS:**
• Pizza delivery until 4 AM
• Burger joints open late
• Taco trucks & street food
• 24-hour diners
• Convenience store snacks

🚚 **LATE DELIVERY:**
• No delivery fee after midnight
• Priority delivery for late orders
• Contactless delivery option
• 30-min delivery guarantee"""
    },
    "family": {
        "title": "👨‍👩‍👧‍👦 **Family Meals - Feed 4 for $20**",
        "details": """🏠 **FAMILY DEALS:**

💰 **FAMILY PACKAGES:**
• Feed 4 for $20 (any cuisine)
• Kids eat FREE with adult meal
• Family pizza: Large 3-topping $15
• Asian family combo: 4 dishes $25
• Mexican family feast: Tacos, burritos, nachos $22

🎯 **PERFECT FOR:**
• Family dinner nights
• Weekend family meals
• Birthday celebrations
• Holiday gatherings
• Sunday brunch orders"""
    },
    "student": {
        "title": "🎓 **Student Specials - 60% OFF + Free Delivery**",
        "details": """🏫 **STUDENT EXCLUSIVES:**

🎯 **CAMPUS DELIVERY:**
• All university areas covered
• Dorm delivery directly to room
• Library drop-off available
• Study group meal deals

💰 **STUDENT DISCOUNTS:**
• 60% OFF (extra 10% for students!)
• FREE delivery within campus
• No minimum order
• Exam week: Extra 15% OFF

📚 **STUDENT MEALS:**
• Quick meals under $10
• Study session snacks
• Coffee & energy drinks
• All-night study packages"""
    }
}

# ===== UBER RIDES DEAL CATEGORIES =====
RIDES_DEALS = {
    "airport": {
        "title": "✈️ **Airport Rides - 60% OFF + Priority**",
        "details": """🛄 **AIRPORT SPECIALS:**

🏢 **ALL MAJOR AIRPORTS:**
• JFK, LAX, ORD, ATL, DFW, DEN, SFO, LAS, MCO
• International terminals included
• Domestic terminals covered
• Private FBO access available

🚗 **AIRPORT SERVICES:**
• UberX Airport: 60% OFF
• Uber Comfort Airport: 55% OFF  
• Uber Black Airport: 50% OFF
• Uber XL Airport: 60% OFF (groups)
• FREE 30-min waiting time

🎯 **AIRPORT PERKS:**
• Priority airport pickup
• Flight tracking included
• Baggage assistance available
• Multi-stop airport runs"""
    },
    "commute": {
        "title": "🚗 **Daily Commute - 55% OFF Monthly Pass**",
        "details": """🏙️ **COMMUTER DEALS:**

📍 **COMMUTE ROUTES:**
• Home to Office: 55% OFF daily
• School runs: 60% OFF for students
• Grocery trips: 50% OFF weekly
• Gym commute: 55% OFF for members
• Shopping trips: 50% OFF weekends

💰 **COMMUTE PACKAGES:**
• Daily pass: Unlimited rides $8/day
• Weekly pass: $35 unlimited rides
• Monthly pass: $120 (best value)
• Corporate plans: 60% OFF for companies

🚘 **COMMUTE VEHICLES:**
• UberX: Standard 55% OFF
• Uber Comfort: Premium 50% OFF
• Uber Green: Electric 60% OFF
• Uber Pool: Shared 65% OFF"""
    },
    "night": {
        "title": "🌙 **Night Rides - 65% OFF (Safety Focus)**",
        "details": """🌃 **NIGHT SAFETY RIDES:**

⏰ **NIGHT HOURS:** 10:00 PM - 5:00 AM
💰 **DISCOUNT:** 65% OFF all night rides

🎯 **NIGHT SAFETY:**
• Share trip with 3 emergency contacts
• Safety check-in feature enabled
• Verified drivers only at night
• Well-lit pickup locations
• 24/7 safety support line

🚖 **NIGHT SERVICES:**
• Bar/club pickup zones
• Concert/event transportation
• Hospital emergency rides
• Overnight shift worker specials"""
    },
    "group": {
        "title": "👥 **Group Travel - 60% OFF 6+ People**",
        "details": """🎉 **GROUP TRANSPORT:**

👥 **GROUP SIZES:**
• 4-6 people: 55% OFF
• 6-8 people: 60% OFF
• 8+ people: 65% OFF
• Multiple vehicles: Bulk discount

🚐 **GROUP VEHICLES:**
• UberXL (6 seats): 60% OFF
• UberSUV (7 seats): 55% OFF
• Multiple UberX: 60% OFF each
• Charter vans: Custom quotes

🎯 **GROUP OCCASIONS:**
• Wedding transportation
• Corporate events
• Sports team travel
• Family reunions
• Party transportation"""
    },
    "long": {
        "title": "🛣️ **Long Distance - 50% OFF + Free Stops**",
        "details": """📍 **LONG DISTANCE TRAVEL:**

🛣️ **DISTANCE COVERAGE:**
• 50-100 miles: 50% OFF
• 100-200 miles: 55% OFF
• 200+ miles: 60% OFF
• Cross-state trips: 50% OFF
• Multi-city tours: Custom pricing

🚘 **LONG TRIP FEATURES:**
• FREE multiple stops
• Scenic route options
• Comfort stops included
• Driver change available
• Overnight trip options

💰 **LONG DISTANCE DEALS:**
• Round trip: 60% OFF both ways
• Weekly car rental: 50% OFF
• Road trip packages: 55% OFF
• One-way relocation: 50% OFF"""
    }
}

@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.from_user.id
    broadcast_users.add(user_id)
    
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    
    # Main service buttons
    keyboard.add(
        types.InlineKeyboardButton("🍽️ Uber Eats Deals", callback_data="eats_main"),
        types.InlineKeyboardButton("🚗 Uber Rides Deals", callback_data="rides_main")
    )
    
    # Special deal categories
    keyboard.add(
        types.InlineKeyboardButton("🎓 Student Specials", callback_data="deal_student"),
        types.InlineKeyboardButton("✈️ Airport Deals", callback_data="deal_airport")
    )
    keyboard.add(
        types.InlineKeyboardButton("🌙 Late Night Deals", callback_data="deal_late"),
        types.InlineKeyboardButton("👥 Group Travel", callback_data="deal_group")
    )
    
    # Location buttons
    keyboard.add(
        types.InlineKeyboardButton("📍 All 50 States", callback_data="states_list"),
        types.InlineKeyboardButton("🏙️ Top Cities", callback_data="cities_list")
    )
    
    # Contact buttons
    keyboard.add(
        types.InlineKeyboardButton("📞 Contact for Eats", url="https://t.me/yrfrnd_spidy"),
        types.InlineKeyboardButton("📞 Contact for Rides", url="https://t.me/Eatsplugsus")
    )
    
    keyboard.add(
        types.InlineKeyboardButton("📢 Join Deals Channel", url="https://t.me/flights_bills_b4u")
    )

    message_text = (
        "🚗 **Uber Deals USA - 50-65% OFF** 🍽️\n\n"
        
        "🔥 **MASSIVE DISCOUNTS AVAILABLE:**\n"
        "✅ Uber Eats: 50-60% OFF food delivery\n"
        "✅ Uber Rides: 50-65% OFF transportation\n"
        "✅ All 50 states covered\n"
        "✅ All major cities included\n\n"
        
        "🎯 **TOP DEAL CATEGORIES:**\n"
        "• Students: Up to 60% OFF\n"
        "• Airport rides: Up to 60% OFF\n"
        "• Late night: Up to 65% OFF\n"
        "• Family meals: Feed 4 for $20\n"
        "• Group travel: Up to 65% OFF\n\n"
        
        "📍 **COVERAGE:** All USA states & cities\n"
        "💰 **DISCOUNTS:** 50-65% OFF guaranteed\n"
        "📞 **24/7 Support:** Contact for codes\n\n"
        
        "*Limited spots - Contact now for instant discounts!*"
    )

    bot.send_message(message.chat.id, message_text, reply_markup=keyboard, parse_mode='Markdown')

# ===== MAIN HANDLERS =====
@bot.callback_query_handler(func=lambda call: call.data == 'eats_main')
def eats_main_handler(call):
    response = """🍽️ **UBER EATS - ALL DEALS 50-60% OFF**

🔥 **CATEGORIES AVAILABLE:**

🎓 **STUDENT SPECIALS:** 60% OFF + Free Delivery
• Campus delivery • Dorm drop-off • Study meals

🍔 **FAST FOOD CHAINS:** 50% OFF All Orders
• McDonald's • Burger King • Taco Bell • Wendy's

🥗 **HEALTHY OPTIONS:** 50% OFF + Free Delivery
• Salads • Smoothies • Vegan • Organic

🌙 **LATE NIGHT:** 60% OFF (10PM-4AM)
• Pizza • Burgers • Tacos • 24-hour spots

👨‍👩‍👧‍👦 **FAMILY MEALS:** Feed 4 for $20
• Family bundles • Kids eat free • Bulk orders

📍 **COVERAGE:** All USA cities
💰 **DISCOUNTS:** 50-60% OFF every order
👥 **ELIGIBILITY:** All users welcome

**HOW TO ORDER:**
1. Contact us for your 50-60% OFF code
2. Use code in Uber Eats app
3. Get massive savings instantly
4. Use unlimited times - no restrictions

📞 **Contact now for immediate 50% OFF code:**"""
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🎓 Student 60% OFF", callback_data="deal_student"),
        types.InlineKeyboardButton("🍔 Fast Food 50% OFF", callback_data="deal_fastfood")
    )
    markup.add(
        types.InlineKeyboardButton("🥗 Healthy 50% OFF", callback_data="deal_healthy"),
        types.InlineKeyboardButton("🌙 Late Night 60% OFF", callback_data="deal_late")
    )
    markup.add(
        types.InlineKeyboardButton("📞 Get Eats Code", url="https://t.me/yrfrnd_spidy"),
        types.InlineKeyboardButton("📍 Cities List", callback_data="cities_list")
    )
    
    bot.send_message(call.message.chat.id, response, reply_markup=markup, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: call.data == 'rides_main')
def rides_main_handler(call):
    response = """🚗 **UBER RIDES - ALL DEALS 50-65% OFF**

🔥 **CATEGORIES AVAILABLE:**

✈️ **AIRPORT RIDES:** 60% OFF + Priority
• All major airports • Luxury options • Free waiting

🚗 **DAILY COMMUTE:** 55% OFF Monthly Pass
• Home-work travel • School runs • Gym commute

🌙 **NIGHT RIDES:** 65% OFF + Safety Features
• 10PM-5AM rides • Bar pickups • Safety check-in

👥 **GROUP TRAVEL:** 60% OFF 6+ People
• Weddings • Events • Corporate • Family trips

🛣️ **LONG DISTANCE:** 50-60% OFF + Free Stops
• Interstate travel • Road trips • Multi-city

📍 **COVERAGE:** All 50 USA states
💰 **DISCOUNTS:** 50-65% OFF every ride
👥 **ELIGIBILITY:** New & existing users

**HOW TO BOOK:**
1. Contact us for 50-65% OFF ride code
2. Apply code in Uber app
3. Save on every ride
4. No usage limits - ride daily

📞 **Contact now for immediate 50% OFF code:**"""
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("✈️ Airport 60% OFF", callback_data="deal_airport"),
        types.InlineKeyboardButton("🚗 Commute 55% OFF", callback_data="deal_commute")
    )
    markup.add(
        types.InlineKeyboardButton("🌙 Night 65% OFF", callback_data="deal_night"),
        types.InlineKeyboardButton("👥 Group 60% OFF", callback_data="deal_group")
    )
    markup.add(
        types.InlineKeyboardButton("📞 Get Rides Code", url="https://t.me/Eatsplugsus"),
        types.InlineKeyboardButton("📍 States List", callback_data="states_list")
    )
    
    bot.send_message(call.message.chat.id, response, reply_markup=markup, parse_mode='Markdown')

# ===== DEAL CATEGORY HANDLERS =====
@bot.callback_query_handler(func=lambda call: call.data.startswith('deal_'))
def deal_handler(call):
    deal_type = call.data.replace('deal_', '')
    
    if deal_type in EATS_DEALS:
        deal = EATS_DEALS[deal_type]
        response = f"{deal['title']}\n\n{deal['details']}"
        
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📞 Get This Deal", url="https://t.me/yrfrnd_spidy"))
        markup.add(types.InlineKeyboardButton("🍽️ More Eats Deals", callback_data="eats_main"))
        
    elif deal_type in RIDES_DEALS:
        deal = RIDES_DEALS[deal_type]
        response = f"{deal['title']}\n\n{deal['details']}"
        
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📞 Get This Deal", url="https://t.me/Eatsplugsus"))
        markup.add(types.InlineKeyboardButton("🚗 More Rides Deals", callback_data="rides_main"))
    
    elif deal_type == "student":
        response = """🎓 **STUDENT SUPER DEAL - 60% OFF BOTH!**

🔥 **UBER EATS FOR STUDENTS:**
• 60% OFF all food delivery
• FREE campus delivery
• Dorm room drop-off
• Library study snacks
• Exam week extra 15% OFF

🚗 **UBER RIDES FOR STUDENTS:**
• 60% OFF all rides to/from campus
• Late night study ride discounts
• Group ride to events 65% OFF
• Airport trips for breaks 60% OFF

📚 **STUDENT REQUIREMENTS:**
• Valid student ID or .edu email
• Campus address verification
• Can use for entire semester
• Share with roommates allowed

💰 **STUDENT SAVINGS:**
• Food budget: Save $200+/month
• Transport: Save $150+/month
• Combined: $350+/month savings
• Perfect for tight student budgets

📞 **Contact for student verification and 60% OFF codes:**"""
        
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📞 Get Student Discount", url="https://t.me/yrfrnd_spidy"))
        markup.add(types.InlineKeyboardButton("🏫 Back to Deals", callback_data="eats_main"))
    
    elif deal_type == "airport":
        response = """✈️ **AIRPORT SUPER DEAL - 60% OFF + EXTRAS**

🏢 **COVERED AIRPORTS:**
• Top 50 USA airports included
• International terminals
• Domestic terminals
• Private FBO access
• Helicopter pads

🚗 **AIRPORT SERVICES 60% OFF:**
• UberX to airport: 60% OFF
• Uber Comfort: 55% OFF (extra space)
• Uber Black: 50% OFF (luxury)
• Uber SUV: 55% OFF (groups)
• Multiple stops: 50% OFF each

🎯 **AIRPORT PERKS INCLUDED:**
• FREE 30-minute waiting time
• Flight tracking automatic
• Priority airport pickup
• Baggage assistance available
• Multi-airport transfers

💰 **BEST FOR:**
• Business travelers
• Family vacations
• Students going home
• Frequent flyers
• International travelers

📞 **Contact for airport discount code:**"""
        
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📞 Get Airport Code", url="https://t.me/Eatsplugsus"))
        markup.add(types.InlineKeyboardButton("✈️ Back to Rides", callback_data="rides_main"))
    
    elif deal_type == "late":
        response = """🌙 **LATE NIGHT COMBO - 65% OFF BOTH!**

🍽️ **LATE NIGHT EATS (10PM-4AM):**
• 60% OFF all food delivery
• No delivery fees after midnight
• Pizza, burgers, tacos, wings
• 24-hour diners & convenience
• Drunk food specials

🚗 **LATE NIGHT RIDES (10PM-5AM):**
• 65% OFF all night rides
• Safety features enabled
• Bar/club zone pickups
• Emergency ride home
• Shift worker specials

🎯 **PERFECT FOR:**
• Night shift workers
• College students
• Party-goers
• Insomniacs
• Emergency situations

⚠️ **SAFETY FEATURES:**
• Share trip with friends
• Safety check-in button
• Verified drivers only
• Well-lit pickup spots
• 24/7 support line

📞 **Contact for late night discount codes:**"""
        
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("🍽️ Get Eats Code", url="https://t.me/yrfrnd_spidy"),
            types.InlineKeyboardButton("🚗 Get Rides Code", url="https://t.me/Eatsplugsus")
        )
        markup.add(types.InlineKeyboardButton("🌙 Back to Deals", callback_data="eats_main"))
    
    elif deal_type == "group":
        response = """👥 **GROUP TRAVEL PACKAGE - 65% OFF**

🚐 **GROUP SIZES & DISCOUNTS:**
• 4-6 people: 60% OFF
• 6-8 people: 65% OFF
• 8+ people: 70% OFF (custom quote)
• Multiple vehicles: Bulk discount

🎉 **GROUP OCCASIONS:**
• Weddings & receptions
• Corporate events
• Sports team travel
• Family reunions
• Birthday parties
• Concert transportation

🍽️ **GROUP EATS DELIVERY:**
• Family meals: 60% OFF
• Catering delivery: 55% OFF
• Bulk food orders: 65% OFF
• Party platters: 60% OFF

💰 **GROUP SAVINGS EXAMPLE:**
• 6 people to wedding: Save $120
• Family of 4 dinner: Save $40
• Corporate lunch: Save $200
• Sports team transport: Save $300

📞 **Contact for group discount codes:**"""
        
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📞 Get Group Discount", url="https://t.me/Eatsplugsus"))
        markup.add(types.InlineKeyboardButton("👥 Back to Deals", callback_data="rides_main"))
    
    else:
        response = "Select a deal category from the main menu."
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔙 Back to Main", callback_data="back_main"))
    
    bot.send_message(call.message.chat.id, response, reply_markup=markup, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: call.data == 'states_list')
def states_list_handler(call):
    # Split states into chunks for better display
    states_chunks = [STATES[i:i+10] for i in range(0, len(STATES), 10)]
    
    response = """📍 **ALL 50 USA STATES COVERED**

✅ **50% - 65% OFF Uber services in every state:**

"""
    
    for chunk in states_chunks[:3]:  # Show first 30 states
        response += "• " + " • ".join(chunk) + "\n"
    
    response += "\n**PLUS 20 more states fully covered!**\n\n"
    
    response += """🎯 **TOP STATES FOR UBER SERVICES:**

🚗 **High Ride Demand States:**
• California • New York • Texas • Florida • Illinois
• High population • Major cities • Tourism hubs

🍽️ **High Eats Demand States:**
• New York • California • Texas • Florida • Illinois
• Foodie cities • College towns • Urban centers

💰 **ALL STATES GET:**
• Uber Eats: 50-60% OFF delivery
• Uber Rides: 50-65% OFF transportation
• 24/7 service availability
• Local restaurant partnerships

📞 **Contact for state-specific discount codes:**"""
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📞 Get State Code", url="https://t.me/yrfrnd_spidy"))
    markup.add(types.InlineKeyboardButton("🗺️ Back to Main", callback_data="back_main"))
    
    bot.send_message(call.message.chat.id, response, reply_markup=markup, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: call.data == 'cities_list')
def cities_list_handler(call):
    # Group cities by category
    response = """🏙️ **TOP USA CITIES COVERED**

🎯 **CITIES WITH MAX TRANSPORTATION USAGE:**

🚗 **MAJOR TRANSPORT HUBS:**
• New York City, NY • Chicago, IL • Los Angeles, CA
• Atlanta, GA • Dallas, TX • Denver, CO
• San Francisco, CA • Houston, TX • Miami, FL
• Seattle, WA

✈️ **MAJOR AIRPORT CITIES:**
• Atlanta (ATL) • Los Angeles (LAX) • Chicago (ORD)
• Dallas (DFW) • Denver (DEN) • New York (JFK)
• San Francisco (SFO) • Las Vegas (LAS)

🏫 **COLLEGE TOWNS (High Uber Usage):**
• Ann Arbor, MI • Austin, TX • Madison, WI
• Berkeley, CA • Boston, MA • Chapel Hill, NC
• Ithaca, NY • State College, PA

🎡 **TOURIST CITIES (High Demand):**
• Las Vegas, NV • Orlando, FL • Miami Beach, FL
• New Orleans, LA • San Antonio, TX • Honolulu, HI

💰 **ALL CITIES GET:**
• Uber Eats: 50-60% OFF food delivery
• Uber Rides: 50-65% OFF transportation
• Local restaurant specials
• Priority service areas

📞 **Contact for city-specific discount codes:**"""
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📞 Get City Code", url="https://t.me/yrfrnd_spidy"))
    markup.add(types.InlineKeyboardButton("🏙️ Back to Main", callback_data="back_main"))
    
    bot.send_message(call.message.chat.id, response, reply_markup=markup, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: call.data == 'back_main')
def back_main_handler(call):
    start_command(call.message)

# ===== STATS COMMAND =====
@bot.message_handler(commands=['stats'])
def stats_command(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "⚠️ Admin command only.")
        return
    
    user_count = len(broadcast_users)
    
    stats_message = (
        f"📊 **UBER DEALS BOT STATISTICS**\n\n"
        f"👥 **Total Users:** {user_count}\n"
        f"📍 **States Covered:** {len(STATES)} (All 50 USA)\n"
        f"🏙️ **Cities Covered:** {len(CITIES)}+\n"
        f"🍽️ **Eats Deal Categories:** {len(EATS_DEALS)}\n"
        f"🚗 **Rides Deal Categories:** {len(RIDES_DEALS)}\n"
        f"🍔 **Popular Dishes Listed:** {len(POPULAR_DISHES)}\n\n"
        f"💰 **Discount Range:** 50-65% OFF\n"
        f"📈 **Estimated Growth:** +{min(user_count, 150)} today\n"
        f"⏰ **Bot Status:** ✅ Active & Running\n"
        f"📞 **Support Contacts:** 2 active\n\n"
        f"*Last updated: Just now*"
    )
    
    bot.send_message(ADMIN_ID, stats_message, parse_mode='Markdown')

# ===== CONTACT HANDLER =====
@bot.message_handler(commands=['contact'])
def contact_command(message):
    response = """📞 **CONTACT FOR 50-65% OFF UBER DEALS**

🔥 **IMMEDIATE DISCOUNT CODES AVAILABLE:**

🍽️ **UBER EATS 50-60% OFF:**
Contact: @yrfrnd_spidy
• Get instant 50-60% OFF food delivery codes
• All restaurants included
• All USA cities covered
• No usage limits

🚗 **UBER RIDES 50-65% OFF:**
Contact: @Eatsplugsus
• Get instant 50-65% OFF ride codes
• All ride types included
• All 50 states covered
• Priority support

📢 **DEAL UPDATES & NEW OFFERS:**
Channel: @flights_bills_b4u
• New discount codes
• Flash sale alerts
• Limited time offers
• Success stories

⏰ **SERVICE HOURS:** 24/7
⏱️ **RESPONSE TIME:** Under 30 minutes
✅ **GUARANTEE:** 50% minimum discount

💎 **WHY CHOOSE US:**
• Largest Uber discounts available
• All USA coverage
• No restrictions or limits
• Verified Uber partner
• Thousands of happy customers

*Contact now for immediate 50% OFF code!*"""
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🍽️ Uber Eats Contact", url="https://t.me/yrfrnd_spidy"),
        types.InlineKeyboardButton("🚗 Uber Rides Contact", url="https://t.me/Eatsplugsus")
    )
    markup.add(
        types.InlineKeyboardButton("📢 Join Channel", url="https://t.me/flights_bills_b4u"),
        types.InlineKeyboardButton("🔙 Main Menu", callback_data="back_main")
    )
    
    bot.send_message(message.chat.id, response, reply_markup=markup, parse_mode='Markdown')

# ===== BROADCAST FEATURE =====
@bot.message_handler(commands=['broadcast'])
def broadcast_command(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "⚠️ Admin command only.")
        return
    
    if len(broadcast_users) == 0:
        bot.reply_to(message, "No users available for broadcast.")
        return
    
    msg = bot.send_message(
        ADMIN_ID, 
        f"📤 Send broadcast to {len(broadcast_users)} users:\n\n"
        f"Type your Uber deal announcement:"
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
    
    status_msg = bot.send_message(ADMIN_ID, f"📤 Sending to {len(users)} users...")
    
    for user_id in users:
        try:
            notification = f"🔥 **NEW UBER DEAL ALERT** 🔥\n\n{broadcast_text}\n\n📍 All 50 states covered\n💰 50-65% OFF guaranteed\n📞 Contact for codes!"
            bot.send_message(user_id, notification)
            success_count += 1
        except Exception:
            fail_count += 1
    
    bot.edit_message_text(
        f"✅ **Broadcast Complete!**\n\n"
        f"📊 **Results:**\n"
        f"• ✅ Success: {success_count} users\n"
        f"• ❌ Failed: {fail_count} users\n"
        f"• 📊 Total: {len(users)} users\n\n"
        f"*Uber deal sent successfully!*",
        ADMIN_ID,
        status_msg.message_id
    )

# ===== DEFAULT HANDLER =====
@bot.message_handler(func=lambda message: True)
def all_messages_handler(message):
    user_id = message.from_user.id
    broadcast_users.add(user_id)
    
    if message.text and message.text.lower() in ['hi', 'hello', 'hey', '/start']:
        return  # Already handled
    
    if not message.text.startswith('/'):
        bot.send_message(
            message.chat.id,
            "🚗 **Get 50-65% OFF Uber Deals!** 🍽️\n\n"
            "📞 **Contact for immediate discounts:**\n"
            "• Uber Eats: @yrfrnd_spidy\n"
            "• Uber Rides: @Eatsplugsus\n\n"
            "📍 **Coverage:** All 50 USA states\n"
            "💰 **Discount:** 50-65% OFF guaranteed\n\n"
            "Type /start for all deal categories!"
        )

@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Uber 50-65% OFF Deals | All 50 USA States Coverage</title>
        <meta name="description" content="Get 50-65% OFF Uber Eats food delivery and Uber Rides transportation. All 50 USA states covered. Major cities, college towns, tourist destinations.">
        <meta name="keywords" content="uber 50% off, uber eats discount, uber rides cheap, all usa states, new york uber, california uber, texas uber, florida uber, chicago uber, los angeles uber, airport uber discount, student uber deals">
        <style>
            body { font-family: Arial, sans-serif; text-align: center; padding: 20px; background: #000; color: white; }
            .container { max-width: 800px; margin: 0 auto; background: #1a1a1a; padding: 30px; border-radius: 10px; }
            .uber-green { color: #00D1B2; }
            .deal-badge { background: #00D1B2; color: black; padding: 15px 30px; border-radius: 25px; display: inline-block; margin: 20px; font-weight: bold; font-size: 24px; }
            .coverage-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin: 20px 0; }
            .coverage-card { background: #333; padding: 15px; border-radius: 8px; }
            .contact-box { background: #00D1B2; color: black; padding: 20px; margin: 30px 0; border-radius: 10px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1 class="uber-green">🚗 UBER DEALS USA 🍽️</h1>
            <p>50-65% OFF Uber Eats & Uber Rides</p>
            
            <div class="deal-badge">🔥 50-65% OFF ALL SERVICES</div>
            
            <h2>📍 Coverage: All 50 USA States</h2>
            <div class="coverage-grid">
                <div class="coverage-card">🗽 All Major Cities</div>
                <div class="coverage-card">✈️ All Major Airports</div>
                <div class="coverage-card">🏫 All College Towns</div>
                <div class="coverage-card">🎡 Tourist Destinations</div>
            </div>
            
            <div class="contact-box">
                <h3>📞 Immediate 50% OFF Codes</h3>
                <p><strong>Uber Eats 50-60% OFF:</strong> Contact @yrfrnd_spidy</p>
                <p><strong>Uber Rides 50-65% OFF:</strong> Contact @Eatsplugsus</p>
                <p><strong>Deal Updates:</strong> @flights_bills_b4u</p>
            </div>
            
            <h3>💰 Deal Categories</h3>
            <p>• Students: 60% OFF</p>
            <p>• Airport Rides: 60% OFF</p>
            <p>• Late Night: 65% OFF</p>
            <p>• Family Meals: Feed 4 for $20</p>
            <p>• Group Travel: 60% OFF 6+ people</p>
            <p>• Long Distance: 50-60% OFF</p>
            
            <p style="margin-top: 30px; color: #888;">
                Verified Uber partner discounts. Limited time offers.
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
            print(f"✅ Uber Deals Bot deployed successfully!")
            print(f"📊 States Covered: {len(STATES)} (All 50 USA)")
            print(f"🏙️ Cities Covered: {len(CITIES)}")
            print(f"💰 Discounts: 50-65% OFF")
            print(f"📞 Admin ID: {ADMIN_ID}")
        else:
            print("🔧 Bot running in polling mode")
            
    except Exception as e:
        print(f"⚠️ Webhook setup: {e}")
    
    print("🚀 Uber Deals Bot Active!")
    print("🍽️ Uber Eats: 50-60% OFF food delivery")
    print("🚗 Uber Rides: 50-65% OFF transportation")
    print("📍 Coverage: All 50 USA states")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
