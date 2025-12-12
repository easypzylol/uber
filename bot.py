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
user_states = {}

# ===== HALF OFF SERVICES =====
HALF_OFF_SERVICES = {
    "food": {
        "title": "🍽️ **HALF OFF Food Delivery**",
        "details": """🔥 **50% OFF ALL FOOD DELIVERY SERVICES:**

✅ **DoorDash Half OFF:**
• Every order 50% OFF
• No minimum purchase
• All restaurants included
• Free delivery on orders over $15

✅ **Uber Eats Half OFF:**
• 50% OFF entire cart
• All cuisines covered
• Late night delivery included
• Stack with restaurant deals

✅ **Grubhub Half OFF:**
• Half price on all orders
• Local favorites included
• Group order discounts
• Perks+ members get extra

✅ **Postmates Half OFF:**
• 50% OFF food & groceries
• Alcohol delivery included
• Convenience store items
• 24/7 delivery service

📍 **Available in ALL 50 states**
💰 **Guaranteed 50% OFF every order**
📞 **Contact for Half OFF codes**"""
    },
    "rides": {
        "title": "🚗 **HALF OFF Rides & Transportation**",
        "details": """🚖 **50% OFF ALL TRANSPORTATION:**

✅ **Uber Half OFF Rides:**
• Every ride 50% OFF
• All vehicle types included
• Airport transfers included
• No surge pricing with code

✅ **Lyft Half OFF Rides:**
• 50% OFF Lyft rides
• Lyft XL for groups
• Priority pickup available
• Scheduled rides included

✅ **Taxi Services Half OFF:**
• Traditional taxis 50% OFF
• Local cab companies
• Airport taxi services
• Corporate accounts welcome

✅ **Rental Cars Half OFF:**
• Car rentals 50% OFF
• Airport pickup included
• One-way rentals available
• Insurance discounts

📍 **Available in ALL 50 states**
💰 **Guaranteed 50% OFF every ride**
📞 **Contact for Half OFF codes**"""
    },
    "groceries": {
        "title": "🛒 **HALF OFF Grocery Delivery**",
        "details": """🥦 **50% OFF ALL GROCERY SERVICES:**

✅ **Instacart Half OFF:**
• Groceries 50% OFF
• Same-day delivery
• All major stores included
• Alcohol delivery available

✅ **Shipt Half OFF:**
• 50% OFF Shipt orders
• Target, CVS, Petco included
• Membership fee waived
• Priority delivery times

✅ **Walmart+ Half OFF:**
• Walmart delivery 50% OFF
• Free shipping included
• Fuel discounts available
• Paramount+ included

✅ **Amazon Fresh Half OFF:**
• 50% OFF Amazon Fresh
• Whole Foods included
• 2-hour delivery windows
• Prime benefits apply

📍 **Available in ALL 50 states**
💰 **Guaranteed 50% OFF every order**
📞 **Contact for Half OFF codes**"""
    },
    "shopping": {
        "title": "🛍️ **HALF OFF Shopping Delivery**",
        "details": """📦 **50% OFF ALL SHOPPING DELIVERY:**

✅ **Amazon Half OFF Delivery:**
• Amazon orders 50% OFF
• Same-day delivery included
• All product categories
• Prime membership benefits

✅ **Target Same-Day Half OFF:**
• Target delivery 50% OFF
• Drive-up pickup included
• All departments covered
• RedCard extra savings

✅ **Best Buy Half OFF Delivery:**
• Electronics 50% OFF
• Same-day delivery available
• Installation services included
• Geek Squad protection

✅ **Home Depot Half OFF:**
• Home improvement 50% OFF
• Truck delivery included
• Installation services
• Rental equipment discounts

📍 **Available in ALL 50 states**
💰 **Guaranteed 50% OFF every delivery**
📞 **Contact for Half OFF codes**"""
    },
    "subscriptions": {
        "title": "📺 **HALF OFF Streaming & Subscriptions**",
        "details": """🎬 **50% OFF ALL SUBSCRIPTIONS:**

✅ **Netflix Half OFF:**
• All plans 50% OFF
• 4K streaming included
• Multiple profiles
• No ads on Premium

✅ **Disney+ Half OFF:**
• Bundle 50% OFF
• Hulu & ESPN+ included
• 4K streaming available
• Download for offline

✅ **Spotify Half OFF:**
• Premium 50% OFF
• Ad-free listening
• Offline downloads
• High quality audio

✅ **YouTube Premium Half OFF:**
• 50% OFF Premium
• YouTube Music included
• Background play
• Offline downloads

📍 **Available in ALL 50 states**
💰 **Guaranteed 50% OFF every subscription**
📞 **Contact for Half OFF codes**"""
    },
    "bills": {
        "title": "💰 **HALF OFF ALL BILLS & UTILITIES**",
        "details": """📊 **50% OFF ALL YOUR MONTHLY BILLS:**

✅ **ELECTRICITY BILLS 50% OFF:**
• All utility companies included
• No contract required
• Prepaid & postpaid accounts
• Commercial & residential
• Back bills also eligible
• Late fee waivers included

✅ **WATER & SEWER BILLS 50% OFF:**
• Municipal water companies
• Private water suppliers
• Sewage treatment bills
• Water conservation fees
• All payment plans accepted
• Arrears clearance available

✅ **GAS & HEATING BILLS 50% OFF:**
• Natural gas providers
• Propane delivery services
• Heating oil companies
• Winter heating assistance
• Commercial gas accounts
• Budget billing programs

✅ **INTERNET & PHONE BILLS 50% OFF:**
• Comcast/Xfinity 50% OFF
• Verizon Fios 50% OFF
• AT&T Internet 50% OFF
• Spectrum 50% OFF
• T-Mobile Home Internet
• Cox Communications
• All mobile phone plans
• Landline services included
• Business internet plans

✅ **CABLE & TV BILLS 50% OFF:**
• DIRECTV 50% OFF
• DISH Network 50% OFF
• YouTube TV 50% OFF
• Hulu + Live TV 50% OFF
• Sling TV 50% OFF
• FuboTV 50% OFF
• All premium channels included
• Sports packages discounted

✅ **CREDIT CARD BILLS 50% OFF:**
• Minimum payment 50% OFF
• Balance transfer assistance
• Interest rate reduction
• Late fee elimination
• All major banks accepted:
  • Chase, Citi, Bank of America
  • Capital One, Wells Fargo
  • American Express, Discover
• Business credit cards included

✅ **LOAN PAYMENTS 50% OFF:**
• Personal loans 50% OFF
• Student loans 50% OFF
• Auto loans 50% OFF
• Mortgage payments 50% OFF
• Medical bills 50% OFF
• Payday loans assistance
• Debt consolidation help
• All credit scores accepted

✅ **INSURANCE PREMIUMS 50% OFF:**
• Car insurance 50% OFF
• Health insurance 50% OFF
• Home insurance 50% OFF
• Life insurance 50% OFF
• Renters insurance 50% OFF
• Pet insurance 50% OFF
• Business insurance 50% OFF
• All major providers accepted

✅ **RENT & MORTGAGE 50% OFF:**
• Apartment rent 50% OFF
• House rent 50% OFF
• Mortgage payments 50% OFF
• HOA fees 50% OFF
• Property taxes assistance
• Eviction prevention help
• Security deposit assistance

✅ **MEDICAL BILLS 50% OFF:**
• Hospital bills 50% OFF
• Doctor visits 50% OFF
• Dental bills 50% OFF
• Prescription costs 50% OFF
• Medical equipment 50% OFF
• Therapy & counseling 50% OFF
• All insurance types accepted

✅ **OTHER BILLS 50% OFF:**
• Car payments 50% OFF
• Gym memberships 50% OFF
• Subscription boxes 50% OFF
• Newspaper/magazine 50% OFF
• Alarm monitoring 50% OFF
• Storage unit fees 50% OFF
• Pet care services 50% OFF
• Daycare costs 50% OFF

📍 **COVERAGE:** All 50 USA States
💳 **PAYMENT METHODS ACCEPTED:**
• Credit/Debit Cards
• Bank Transfers (ACH)
• PayPal, Venmo, Cash App
• Money Orders
• Cryptocurrency (BTC, ETH)

⏰ **PROCESSING TIME:**
• Instant approval for most bills
• 1-3 business days processing
• Same-day emergency service
• 24/7 customer support

📋 **REQUIREMENTS:**
• Valid bill statement
• Account number
• Minimum $50 bill amount
• No income verification needed

🛡️ **GUARANTEE:**
• 50% OFF guaranteed or money back
• No hidden fees
• Secure payment processing
• Privacy protected
• Legal compliance assured

💎 **SPECIAL PROGRAMS:**
• First-time user bonus: Extra 10% OFF
• Referral program: $50 credit per referral
• Loyalty rewards: Earn points for discounts
• Bulk discounts: Multiple bills = Extra savings
• Emergency assistance: Same-day processing

⚠️ **IMPORTANT NOTES:**
• Must be current US resident
• Bill must be in your name
• Minimum 3-month payment history preferred
• No bankruptcy restrictions
• Service available for individuals & businesses

📞 **HOW IT WORKS:**
1. Send us your bill details
2. We verify and approve instantly
3. You pay us 50% of the bill amount
4. We pay your provider 100%
5. You save 50% every month

🔥 **LIMITED TIME OFFER:**
• First 100 customers get EXTRA 10% OFF
• Family plans available (up to 5 bills)
• Business accounts welcome (unlimited bills)
• No credit check required
• All debt types accepted

💰 **ACTUAL SAVINGS EXAMPLES:**
• $300 electric bill → Pay $150
• $200 internet bill → Pay $100  
• $150 phone bill → Pay $75
• $400 credit card → Pay $200
• $1,200 rent → Pay $600
• $500 car payment → Pay $250

🎯 **POPULAR BILLS WE PROCESS:**
• PG&E, ConEdison, Duke Energy
• Verizon, AT&T, T-Mobile
• Comcast, Spectrum, Cox
• Chase, Bank of America, Citi
• State Farm, Geico, Progressive
• Sallie Mae, Navient, FedLoan
• Most major providers accepted

📍 **Available in ALL 50 states**
💰 **Guaranteed 50% OFF every bill**
📞 **Contact for Half OFF bill payment codes**"""
    }
}

# ===== ALL 50 USA STATES =====
ALL_STATES = {
    "AL": {"name": "Alabama", "cities": ["Birmingham", "Montgomery", "Mobile"]},
    "AK": {"name": "Alaska", "cities": ["Anchorage", "Fairbanks", "Juneau"]},
    "AZ": {"name": "Arizona", "cities": ["Phoenix", "Tucson", "Mesa"]},
    "AR": {"name": "Arkansas", "cities": ["Little Rock", "Fort Smith", "Fayetteville"]},
    "CA": {"name": "California", "cities": ["Los Angeles", "San Francisco", "San Diego", "Sacramento"]},
    "CO": {"name": "Colorado", "cities": ["Denver", "Colorado Springs", "Aurora"]},
    "CT": {"name": "Connecticut", "cities": ["Bridgeport", "New Haven", "Hartford"]},
    "DE": {"name": "Delaware", "cities": ["Wilmington", "Dover", "Newark"]},
    "FL": {"name": "Florida", "cities": ["Miami", "Orlando", "Tampa", "Jacksonville"]},
    "GA": {"name": "Georgia", "cities": ["Atlanta", "Augusta", "Columbus"]},
    "HI": {"name": "Hawaii", "cities": ["Honolulu", "Hilo", "Kailua"]},
    "ID": {"name": "Idaho", "cities": ["Boise", "Meridian", "Nampa"]},
    "IL": {"name": "Illinois", "cities": ["Chicago", "Aurora", "Rockford"]},
    "IN": {"name": "Indiana", "cities": ["Indianapolis", "Fort Wayne", "Evansville"]},
    "IA": {"name": "Iowa", "cities": ["Des Moines", "Cedar Rapids", "Davenport"]},
    "KS": {"name": "Kansas", "cities": ["Wichita", "Overland Park", "Kansas City"]},
    "KY": {"name": "Kentucky", "cities": ["Louisville", "Lexington", "Bowling Green"]},
    "LA": {"name": "Louisiana", "cities": ["New Orleans", "Baton Rouge", "Shreveport"]},
    "ME": {"name": "Maine", "cities": ["Portland", "Lewiston", "Bangor"]},
    "MD": {"name": "Maryland", "cities": ["Baltimore", "Frederick", "Rockville"]},
    "MA": {"name": "Massachusetts", "cities": ["Boston", "Worcester", "Springfield"]},
    "MI": {"name": "Michigan", "cities": ["Detroit", "Grand Rapids", "Warren"]},
    "MN": {"name": "Minnesota", "cities": ["Minneapolis", "Saint Paul", "Rochester"]},
    "MS": {"name": "Mississippi", "cities": ["Jackson", "Gulfport", "Southaven"]},
    "MO": {"name": "Missouri", "cities": ["Kansas City", "Saint Louis", "Springfield"]},
    "MT": {"name": "Montana", "cities": ["Billings", "Missoula", "Great Falls"]},
    "NE": {"name": "Nebraska", "cities": ["Omaha", "Lincoln", "Bellevue"]},
    "NV": {"name": "Nevada", "cities": ["Las Vegas", "Henderson", "Reno"]},
    "NH": {"name": "New Hampshire", "cities": ["Manchester", "Nashua", "Concord"]},
    "NJ": {"name": "New Jersey", "cities": ["Newark", "Jersey City", "Paterson"]},
    "NM": {"name": "New Mexico", "cities": ["Albuquerque", "Las Cruces", "Rio Rancho"]},
    "NY": {"name": "New York", "cities": ["New York City", "Buffalo", "Rochester"]},
    "NC": {"name": "North Carolina", "cities": ["Charlotte", "Raleigh", "Greensboro"]},
    "ND": {"name": "North Dakota", "cities": ["Fargo", "Bismarck", "Grand Forks"]},
    "OH": {"name": "Ohio", "cities": ["Columbus", "Cleveland", "Cincinnati"]},
    "OK": {"name": "Oklahoma", "cities": ["Oklahoma City", "Tulsa", "Norman"]},
    "OR": {"name": "Oregon", "cities": ["Portland", "Salem", "Eugene"]},
    "PA": {"name": "Pennsylvania", "cities": ["Philadelphia", "Pittsburgh", "Allentown"]},
    "RI": {"name": "Rhode Island", "cities": ["Providence", "Warwick", "Cranston"]},
    "SC": {"name": "South Carolina", "cities": ["Charleston", "Columbia", "North Charleston"]},
    "SD": {"name": "South Dakota", "cities": ["Sioux Falls", "Rapid City", "Aberdeen"]},
    "TN": {"name": "Tennessee", "cities": ["Nashville", "Memphis", "Knoxville"]},
    "TX": {"name": "Texas", "cities": ["Houston", "San Antonio", "Dallas", "Austin"]},
    "UT": {"name": "Utah", "cities": ["Salt Lake City", "West Valley City", "Provo"]},
    "VT": {"name": "Vermont", "cities": ["Burlington", "South Burlington", "Rutland"]},
    "VA": {"name": "Virginia", "cities": ["Virginia Beach", "Norfolk", "Chesapeake"]},
    "WA": {"name": "Washington", "cities": ["Seattle", "Spokane", "Tacoma"]},
    "WV": {"name": "West Virginia", "cities": ["Charleston", "Huntington", "Morgantown"]},
    "WI": {"name": "Wisconsin", "cities": ["Milwaukee", "Madison", "Green Bay"]},
    "WY": {"name": "Wyoming", "cities": ["Cheyenne", "Casper", "Laramie"]}
}

@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.from_user.id
    broadcast_users.add(user_id)
    
    # SEO optimized welcome message (hidden from users)
    welcome_text = (
        "🔥 **HALF OFF Services USA** 🔥\n\n"
        
        "✅ **Get 50% OFF on ALL Services in ALL 50 States**\n\n"
        
        "🎯 **OUR HALF OFF SERVICES:**\n"
        "• 🍽️ Food Delivery: DoorDash, Uber Eats, Grubhub\n"
        "• 🚗 Rides & Transportation: Uber, Lyft, Taxis\n"
        "• 🛒 Grocery Delivery: Instacart, Shipt, Walmart+\n"
        "• 🛍️ Shopping Delivery: Amazon, Target, Best Buy\n"
        "• 📺 Streaming Services: Netflix, Disney+, Spotify\n"
        "• 💰 **ALL BILLS:** Electricity, Water, Internet, Rent, Loans, Credit Cards\n\n"
        
        "📍 **COVERAGE:** All 50 USA States\n"
        "💰 **DISCOUNT:** Guaranteed 50% OFF (HALF OFF)\n"
        "⏰ **AVAILABILITY:** 24/7 Service\n\n"
        
        "*Half OFF on everything - Food, Rides, Groceries, Shopping, Bills & More!*\n"
        "*Limited spots available. Contact now for Half OFF codes!*"
    )
    
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    
    # Service categories - Updated with Bills
    keyboard.add(
        types.InlineKeyboardButton("🍽️ Food HALF OFF", callback_data="service_food"),
        types.InlineKeyboardButton("🚗 Rides HALF OFF", callback_data="service_rides")
    )
    keyboard.add(
        types.InlineKeyboardButton("🛒 Groceries HALF OFF", callback_data="service_groceries"),
        types.InlineKeyboardButton("🛍️ Shopping HALF OFF", callback_data="service_shopping")
    )
    keyboard.add(
        types.InlineKeyboardButton("📺 Subscriptions HALF OFF", callback_data="service_subscriptions"),
        types.InlineKeyboardButton("💰 Bills HALF OFF", callback_data="service_bills")
    )
    keyboard.add(
        types.InlineKeyboardButton("📍 Select Your State", callback_data="select_state")
    )
    
    # Removed SEO button, kept contact
    keyboard.add(
        types.InlineKeyboardButton("📞 Contact for 50% OFF", callback_data="contact_main")
    )
    
    keyboard.add(
        types.InlineKeyboardButton("📢 Join HALF OFF Deals", url="https://t.me/flights_bills_b4u")
    )
    
    bot.send_message(message.chat.id, welcome_text, reply_markup=keyboard, parse_mode='Markdown')

# ===== SERVICE HANDLERS =====
@bot.callback_query_handler(func=lambda call: call.data.startswith('service_'))
def service_handler(call):
    service_type = call.data.replace('service_', '')
    
    if service_type in HALF_OFF_SERVICES:
        service = HALF_OFF_SERVICES[service_type]
        
        response = f"{service['title']}\n\n{service['details']}"
        
        # Removed SEO keywords section
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton(f"📞 Get {service_type.title()} Code", callback_data=f"contact_{service_type}"),
            types.InlineKeyboardButton("📍 Select State", callback_data="select_state")
        )
        markup.add(
            types.InlineKeyboardButton("🔙 All Services", callback_data="back_services"),
            types.InlineKeyboardButton("📢 Join Channel", url="https://t.me/flights_bills_b4u")
        )
        
        bot.send_message(call.message.chat.id, response, reply_markup=markup, parse_mode='Markdown')

# ===== STATE SELECTION =====
@bot.callback_query_handler(func=lambda call: call.data == 'select_state')
def select_state_handler(call):
    response = """📍 **Select Your State for HALF OFF Services**

🎯 **Get 50% OFF services specifically in your state:**

**Popular States for HALF OFF Services:**

🔸 **California:** Los Angeles, San Francisco, San Diego
🔸 **Texas:** Houston, Dallas, Austin, San Antonio  
🔸 **New York:** NYC, Buffalo, Rochester
🔸 **Florida:** Miami, Orlando, Tampa, Jacksonville
🔸 **Illinois:** Chicago, Aurora, Rockford
🔸 **Pennsylvania:** Philadelphia, Pittsburgh
🔸 **Ohio:** Columbus, Cleveland, Cincinnati

**PLUS all other 43 states covered!**

👇 **Select your state for state-specific HALF OFF codes:**"""
    
    # Create keyboard with state regions
    markup = types.InlineKeyboardMarkup(row_width=3)
    
    # First row - Major states
    markup.add(
        types.InlineKeyboardButton("📍 California", callback_data="state_CA"),
        types.InlineKeyboardButton("📍 Texas", callback_data="state_TX"),
        types.InlineKeyboardButton("📍 New York", callback_data="state_NY")
    )
    
    # Second row
    markup.add(
        types.InlineKeyboardButton("📍 Florida", callback_data="state_FL"),
        types.InlineKeyboardButton("📍 Illinois", callback_data="state_IL"),
        types.InlineKeyboardButton("📍 Pennsylvania", callback_data="state_PA")
    )
    
    # Third row
    markup.add(
        types.InlineKeyboardButton("📍 Ohio", callback_data="state_OH"),
        types.InlineKeyboardButton("📍 Georgia", callback_data="state_GA"),
        types.InlineKeyboardButton("📍 North Carolina", callback_data="state_NC")
    )
    
    # Fourth row
    markup.add(
        types.InlineKeyboardButton("📍 Michigan", callback_data="state_MI"),
        types.InlineKeyboardButton("📍 New Jersey", callback_data="state_NJ"),
        types.InlineKeyboardButton("📍 Virginia", callback_data="state_VA")
    )
    
    # Fifth row - More options
    markup.add(
        types.InlineKeyboardButton("📍 All 50 States List", callback_data="all_states"),
        types.InlineKeyboardButton("📍 Other States", callback_data="other_states")
    )
    
    markup.add(
        types.InlineKeyboardButton("🔙 Back to Services", callback_data="back_services")
    )
    
    bot.send_message(call.message.chat.id, response, reply_markup=markup, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: call.data.startswith('state_'))
def state_detail_handler(call):
    state_code = call.data.replace('state_', '')
    
    if state_code in ALL_STATES:
        state = ALL_STATES[state_code]
        
        cities_text = "\n".join([f"• {city}" for city in state["cities"]])
        
        response = f"""📍 **HALF OFF Services in {state['name']}**

🏙️ **Major Cities Covered:**
{cities_text}

🎯 **Available HALF OFF Services in {state['name']}:**

🍽️ **Food Delivery 50% OFF:**
• DoorDash, Uber Eats, Grubhub
• All local restaurants included
• Late night delivery available

🚗 **Rides 50% OFF:**
• Uber, Lyft, local taxis
• Airport transfers included
• All vehicle types

🛒 **Groceries 50% OFF:**
• Instacart, Shipt, Walmart+
• Same-day delivery
• All major grocery stores

🛍️ **Shopping 50% OFF:**
• Amazon, Target, Best Buy
• Same-day delivery available
• All product categories

💰 **BILLS 50% OFF:**
• Electricity, Water, Gas
• Internet, Phone, Cable
• Credit Cards, Loans, Rent
• Insurance, Medical Bills

💰 **STATE-SPECIFIC HALF OFF CODES:**
• Custom codes for {state['name']} residents
• Higher discount rates in some cities
• Local business partnerships
• Priority customer support

📞 **Contact for {state['name']} Half OFF codes:**"""
        
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton(f"📞 {state['name']} Codes", callback_data=f"contact_state_{state_code}"),
            types.InlineKeyboardButton("📍 Other States", callback_data="select_state")
        )
        markup.add(
            types.InlineKeyboardButton("🍽️ Food in State", callback_data="service_food"),
            types.InlineKeyboardButton("💰 Bills in State", callback_data="service_bills")
        )
        
        bot.send_message(call.message.chat.id, response, reply_markup=markup, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: call.data == 'all_states')
def all_states_handler(call):
    response = """📍 **HALF OFF Services in ALL 50 USA States**

🇺🇸 **ALL STATES COVERED - 50% OFF GUARANTEED**

**NORTHEAST STATES:**
• Maine • New Hampshire • Vermont • Massachusetts
• Rhode Island • Connecticut • New York • New Jersey
• Pennsylvania

**MIDWEST STATES:**
• Ohio • Michigan • Indiana • Illinois • Wisconsin
• Minnesota • Iowa • Missouri • North Dakota
• South Dakota • Nebraska • Kansas

**SOUTHERN STATES:**
• Delaware • Maryland • Virginia • West Virginia
• Kentucky • Tennessee • North Carolina • South Carolina
• Georgia • Florida • Alabama • Mississippi • Arkansas
• Louisiana • Texas • Oklahoma

**WESTERN STATES:**
• Montana • Idaho • Wyoming • Colorado • New Mexico
• Arizona • Utah • Nevada • California • Oregon
• Washington • Alaska • Hawaii

🎯 **EVERY STATE GETS:**
• 50% OFF all food delivery
• 50% OFF all rides & transportation
• 50% OFF grocery delivery
• 50% OFF shopping delivery
• 50% OFF streaming services
• 50% OFF ALL BILLS (Electricity, Water, Internet, Loans, etc.)

📞 **Contact for state-specific Half OFF codes!**"""
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📞 Get All States Code", callback_data="contact_all_states"))
    markup.add(types.InlineKeyboardButton("📍 Back to State Select", callback_data="select_state"))
    
    bot.send_message(call.message.chat.id, response, reply_markup=markup, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: call.data == 'other_states')
def other_states_handler(call):
    response = """📍 **Other States with HALF OFF Services**

🎯 **These states also get 50% OFF all services:**

**MORE STATES COVERED:**
• Alabama • Alaska • Arizona • Arkansas
• Colorado • Connecticut • Delaware • Hawaii
• Idaho • Iowa • Kansas • Kentucky • Louisiana
• Maine • Maryland • Massachusetts • Michigan
• Minnesota • Mississippi • Missouri • Montana
• Nebraska • Nevada • New Hampshire • New Mexico
• North Dakota • Oklahoma • Oregon • Rhode Island
• South Carolina • South Dakota • Tennessee • Utah
• Vermont • Virginia • Washington • West Virginia
• Wisconsin • Wyoming

💰 **SAME 50% OFF IN EVERY STATE:**
• No state left behind
• Uniform pricing nationwide
• Same great discounts everywhere
• No geographical restrictions

📞 **Contact for any state's Half OFF codes!**"""
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📞 Contact for State Codes", callback_data="contact_main"))
    markup.add(types.InlineKeyboardButton("📍 Back to Main", callback_data="back_services"))
    
    bot.send_message(call.message.chat.id, response, reply_markup=markup, parse_mode='Markdown')

# ===== CONTACT HANDLERS =====
@bot.callback_query_handler(func=lambda call: call.data.startswith('contact_'))
def contact_handler(call):
    contact_type = call.data.replace('contact_', '')
    
    if contact_type == "main":
        response = """📞 **Contact for HALF OFF Services**

🔥 **GET 50% OFF ON EVERYTHING:**

🎯 **MAIN CONTACTS:**

1. **Primary Contact:** @yrfrnd_spidy
   • For all Half OFF service codes
   • State-specific discounts
   • Bulk order discounts
   • Corporate accounts
   • **BILL PAYMENTS:** Electricity, Water, Internet, Loans, Credit Cards

2. **Support Contact:** @Eatsplugsus
   • Technical support
   • Code activation help
   • Account issues
   • Refund assistance
   • Bill payment processing

3. **Updates Channel:** @flights_bills_b4u
   • New Half OFF deals
   • Flash sales alerts
   • Limited time offers
   • Success stories

⏰ **SERVICE HOURS:** 24/7
⏱️ **RESPONSE TIME:** Under 15 minutes
✅ **GUARANTEE:** 50% OFF minimum

💰 **WHAT YOU GET:**
• Half OFF codes for all services
• State-specific promotions
• Bill payment assistance
• No usage limits
• Permanent discounts
• Priority customer support

*Message now for immediate Half OFF codes!*"""
    
    elif contact_type in ["food", "rides", "groceries", "shopping", "subscriptions", "bills"]:
        service_name = contact_type.title()
        if contact_type == "bills":
            service_name = "All Bills"
            response = f"""📞 **Contact for BILLS HALF OFF**

🔥 **GET 50% OFF ON ALL YOUR BILLS:**

🎯 **BILL PAYMENT SPECIALISTS:**

**Primary Contact:** @yrfrnd_spidy
• Electricity bills 50% OFF
• Water & sewer bills 50% OFF
• Internet & phone bills 50% OFF
• Credit card payments 50% OFF
• Loan payments 50% OFF
• Rent & mortgage 50% OFF
• Insurance premiums 50% OFF
• Medical bills 50% OFF

**Support Available:** @Eatsplugsus
• Bill verification assistance
• Payment processing help
• Account linking support
• Urgent payment handling
• Multiple bill discounts

⏰ **Bill Support:** 24/7 Emergency Service
💰 **Discount:** Guaranteed 50% OFF
📍 **Coverage:** All 50 states
💳 **Payment Methods:** Cards, Bank Transfer, Crypto

📋 **REQUIRED INFO FOR BILL PAYMENT:**
1. Bill statement screenshot
2. Account number
3. Amount due
4. Due date
5. Provider name

🎁 **BILL PAYMENT BONUSES:**
• First bill: Extra 10% OFF
• Multiple bills: Bundle discount
• Referral bonus: $50 credit
• Loyalty rewards program
• Family plan discounts

*Message now with your bill details for 50% OFF!*"""
        else:
            response = f"""📞 **Contact for {service_name} HALF OFF**

🔥 **GET 50% OFF ON {service_name.upper()}:**

🎯 **SPECIALIZED SUPPORT:**

**Primary Contact:** @yrfrnd_spidy
• {service_name} Half OFF codes
• Service-specific discounts
• Platform troubleshooting
• Best deal recommendations

**Support Available:** @Eatsplugsus
• Activation assistance
• Code troubleshooting
• Account linking help
• Refund processing

⏰ **{service_name} Support:** 24/7
💰 **Discount:** Guaranteed 50% OFF
📍 **Coverage:** All 50 states

🎁 **{service_name.upper()} BONUSES:**
• Extra discounts for first-time users
• Loyalty rewards program
• Referral bonuses
• Seasonal promotions

*Message now for {service_name} Half OFF codes!*"""
    
    elif contact_type.startswith("state_"):
        state_code = contact_type.replace("state_", "")
        if state_code in ALL_STATES:
            state_name = ALL_STATES[state_code]["name"]
            response = f"""📞 **Contact for {state_name} HALF OFF Codes**

📍 **STATE-SPECIFIC HALF OFF:**

🎯 **{state_name.upper()} SPECIALISTS:**

**Primary Contact:** @yrfrnd_spidy
• {state_name} Half OFF codes
• City-specific promotions
• Local business partnerships
• Regional discounts
• Local bill payment assistance

**Support:** @Eatsplugsus
• Local activation help
• Regional troubleshooting
• State-specific offers
• Local delivery assistance
• Bill payment processing

🏙️ **MAJOR CITIES IN {state_name.upper()}:**
{", ".join(ALL_STATES[state_code]["cities"][:3])}

💰 **{state_name.upper()} BONUSES:**
• Extra 5% OFF for state residents
• Local restaurant partnerships
• Regional delivery discounts
• State holiday specials
• Local utility bill discounts

*Message now for {state_name} Half OFF codes!*"""
    
    elif contact_type == "all_states":
        response = """📞 **Contact for ALL 50 STATES HALF OFF**

🇺🇸 **NATIONWIDE HALF OFF COVERAGE:**

🎯 **NATIONAL ACCOUNT MANAGERS:**

**Primary Contact:** @yrfrnd_spidy
• All 50 states coverage
• National discount codes
• Corporate nationwide plans
• Bulk state discounts
• National bill payment programs

**Support:** @Eatsplugsus
• Multi-state activation
• Cross-state troubleshooting
• National account setup
• Regional manager access
• Multi-state bill payments

🗺️ **COVERAGE:** All 50 USA States
💰 **DISCOUNT:** Uniform 50% OFF nationwide
🎁 **BONUS:** No geographical restrictions

💎 **NATIONAL BENEFITS:**
• One code works in all states
• No need for multiple accounts
• Consistent pricing nationwide
• Priority national support
• National bill payment network

*Message now for nationwide Half OFF codes!*"""
    
    else:
        response = """📞 **Contact for HALF OFF Services**

Message @yrfrnd_spidy for Half OFF codes
Message @Eatsplugsus for support
Join @flights_bills_b4u for updates

24/7 service available!"""
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("💬 Message Now", url="https://t.me/yrfrnd_spidy"),
        types.InlineKeyboardButton("📞 Support", url="https://t.me/Eatsplugsus")
    )
    markup.add(
        types.InlineKeyboardButton("📢 Join Channel", url="https://t.me/flights_bills_b4u"),
        types.InlineKeyboardButton("🔙 Back to Main", callback_data="back_services")
    )
    
    bot.send_message(call.message.chat.id, response, reply_markup=markup, parse_mode='Markdown')

# ===== BACK HANDLERS =====
@bot.callback_query_handler(func=lambda call: call.data == 'back_services')
def back_services_handler(call):
    start_command(call.message)

# ===== ADMIN COMMANDS =====
@bot.message_handler(commands=['stats'])
def stats_command(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "⚠️ Admin command only.")
        return
    
    user_count = len(broadcast_users)
    
    stats_message = (
        f"📊 **HALF OFF BOT STATISTICS**\n\n"
        f"👥 **Total Users:** {user_count}\n"
        f"💰 **Services:** {len(HALF_OFF_SERVICES)} categories\n"
        f"🇺🇸 **States Database:** {len(ALL_STATES)} (All USA)\n"
        f"✅ **New Service:** Bills HALF OFF added\n\n"
        f"💰 **Discount:** 50% OFF (Half OFF)\n"
        f"📈 **Growth:** Active\n"
        f"⏰ **Status:** ✅ Active\n\n"
        f"*Last updated: Just now*"
    )
    
    bot.send_message(ADMIN_ID, stats_message, parse_mode='Markdown')

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
        f"📤 Send HALF OFF broadcast to {len(broadcast_users)} users:\n\n"
        f"Type your Half OFF deal announcement:"
    )
    bot.register_next_step_handler(msg, process_broadcast_message)

def process_broadcast_message(message):
    if hasattr(message, 'is_broadcast_processed') and message.is_broadcast_processed:
        return
    
    message.is_broadcast_processed = True
    broadcast_text = message.text
    users = list(broadcast_users)
    success_count = 0
    
    status_msg = bot.send_message(ADMIN_ID, f"📤 Sending Half OFF deals to {len(users)} users...")
    
    for user_id in users:
        try:
            notification = (
                f"🔥 **HALF OFF ALERT** 🔥\n\n"
                f"{broadcast_text}\n\n"
                f"📍 All 50 states covered\n"
                f"💰 50% OFF guaranteed\n"
                f"📞 Contact for Half OFF codes!"
            )
            bot.send_message(user_id, notification)
            success_count += 1
        except Exception:
            pass
    
    bot.edit_message_text(
        f"✅ **Half OFF Broadcast Complete!**\n\n"
        f"📊 **Results:**\n"
        f"• ✅ Success: {success_count} users\n"
        f"• 📊 Total: {len(users)} users\n\n"
        f"*Half OFF deal sent successfully!*",
        ADMIN_ID,
        status_msg.message_id
    )

# ===== DEFAULT HANDLER =====
@bot.message_handler(func=lambda message: True)
def all_messages_handler(message):
    user_id = message.from_user.id
    broadcast_users.add(user_id)
    
    if message.text and message.text.lower() in ['hi', 'hello', 'hey', '/start']:
        return
    
    if not message.text.startswith('/'):
        bot.send_message(
            message.chat.id,
            "🔥 **HALF OFF Services USA** 🔥\n\n"
            "🎯 **Get 50% OFF on everything:**\n"
            "• Food Delivery • Rides • Groceries\n"
            "• Shopping • Streaming Services\n"
            "• **ALL BILLS:** Electricity, Water, Internet, Loans\n\n"
            "📍 **All 50 states covered**\n"
            "💰 **Guaranteed 50% OFF**\n\n"
            "📞 **Contact for Half OFF codes:**\n"
            "• @yrfrnd_spidy (Main contact)\n"
            "• @Eatsplugsus (Support)\n\n"
            "Type /start for all Half OFF services!"
        )

@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Half OFF Services USA | 50% OFF Everything</title>
        <style>
            body { font-family: 'Arial', sans-serif; margin: 0; padding: 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
            .container { max-width: 1000px; margin: 0 auto; padding: 40px 20px; }
            .header { text-align: center; margin-bottom: 50px; }
            .half-off-badge { background: #FF6B6B; color: white; padding: 20px 40px; border-radius: 50px; font-size: 36px; font-weight: bold; display: inline-block; margin: 20px 0; box-shadow: 0 10px 30px rgba(255, 107, 107, 0.4); }
            .services-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 25px; margin: 40px 0; }
            .service-card { background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(10px); padding: 25px; border-radius: 15px; border: 1px solid rgba(255, 255, 255, 0.2); }
            .service-icon { font-size: 40px; margin-bottom: 15px; }
            .states-section { background: rgba(255, 255, 255, 0.1); padding: 30px; border-radius: 15px; margin: 40px 0; }
            .state-list { column-count: 3; column-gap: 30px; }
            .state-item { padding: 8px 0; border-bottom: 1px solid rgba(255, 255, 255, 0.1); }
            .contact-box { background: #4CAF50; padding: 30px; border-radius: 15px; margin: 40px 0; text-align: center; }
            .keyword-tags { display: flex; flex-wrap: wrap; gap: 10px; margin: 20px 0; }
            .keyword-tag { background: rgba(255, 255, 255, 0.2); padding: 8px 15px; border-radius: 20px; font-size: 14px; }
            @media (max-width: 768px) {
                .state-list { column-count: 2; }
                .half-off-badge { font-size: 28px; padding: 15px 30px; }
            }
            @media (max-width: 480px) {
                .state-list { column-count: 1; }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🔥 HALF OFF SERVICES USA 🔥</h1>
                <p class="subtitle">50% OFF Everything in All 50 States</p>
                <div class="half-off-badge">HALF OFF EVERYTHING</div>
                <p>Food Delivery • Rides • Groceries • Shopping • Streaming • ALL BILLS</p>
            </div>
            
            <div class="services-grid">
                <div class="service-card">
                    <div class="service-icon">🍽️</div>
                    <h3>Food Delivery HALF OFF</h3>
                    <p>50% OFF DoorDash, Uber Eats, Grubhub, Postmates.</p>
                </div>
                <div class="service-card">
                    <div class="service-icon">🚗</div>
                    <h3>Rides HALF OFF</h3>
                    <p>50% OFF Uber, Lyft, taxis, airport transfers.</p>
                </div>
                <div class="service-card">
                    <div class="service-icon">🛒</div>
                    <h3>Groceries HALF OFF</h3>
                    <p>50% OFF Instacart, Shipt, Walmart+, Amazon Fresh.</p>
                </div>
                <div class="service-card">
                    <div class="service-icon">🛍️</div>
                    <h3>Shopping HALF OFF</h3>
                    <p>50% OFF Amazon, Target, Best Buy, Home Depot.</p>
                </div>
                <div class="service-card">
                    <div class="service-icon">📺</div>
                    <h3>Streaming HALF OFF</h3>
                    <p>50% OFF Netflix, Disney+, Spotify, YouTube Premium.</p>
                </div>
                <div class="service-card">
                    <div class="service-icon">💰</div>
                    <h3>ALL BILLS HALF OFF</h3>
                    <p>50% OFF Electricity, Water, Internet, Loans, Credit Cards, Rent, Insurance.</p>
                </div>
            </div>
            
            <div class="states-section">
                <h2 style="text-align: center;">📍 All 50 USA States Covered</h2>
                <div class="state-list">
                    <div class="state-item">Alabama - HALF OFF</div>
                    <div class="state-item">Alaska - HALF OFF</div>
                    <div class="state-item">Arizona - HALF OFF</div>
                    <div class="state-item">Arkansas - HALF OFF</div>
                    <div class="state-item">California - HALF OFF</div>
                    <div class="state-item">Colorado - HALF OFF</div>
                    <div class="state-item">Connecticut - HALF OFF</div>
                    <div class="state-item">Delaware - HALF OFF</div>
                    <div class="state-item">Florida - HALF OFF</div>
                    <div class="state-item">Georgia - HALF OFF</div>
                    <div class="state-item">Hawaii - HALF OFF</div>
                    <div class="state-item">Idaho - HALF OFF</div>
                    <div class="state-item">Illinois - HALF OFF</div>
                    <div class="state-item">Indiana - HALF OFF</div>
                    <div class="state-item">Iowa - HALF OFF</div>
                    <div class="state-item">Kansas - HALF OFF</div>
                    <div class="state-item">Kentucky - HALF OFF</div>
                    <div class="state-item">Louisiana - HALF OFF</div>
                    <div class="state-item">Maine - HALF OFF</div>
                    <div class="state-item">Maryland - HALF OFF</div>
                    <div class="state-item">Massachusetts - HALF OFF</div>
                    <div class="state-item">Michigan - HALF OFF</div>
                    <div class="state-item">Minnesota - HALF OFF</div>
                    <div class="state-item">Mississippi - HALF OFF</div>
                    <div class="state-item">Missouri - HALF OFF</div>
                    <div class="state-item">Montana - HALF OFF</div>
                    <div class="state-item">Nebraska - HALF OFF</div>
                    <div class="state-item">Nevada - HALF OFF</div>
                    <div class="state-item">New Hampshire - HALF OFF</div>
                    <div class="state-item">New Jersey - HALF OFF</div>
                    <div class="state-item">New Mexico - HALF OFF</div>
                    <div class="state-item">New York - HALF OFF</div>
                    <div class="state-item">North Carolina - HALF OFF</div>
                    <div class="state-item">North Dakota - HALF OFF</div>
                    <div class="state-item">Ohio - HALF OFF</div>
                    <div class="state-item">Oklahoma - HALF OFF</div>
                    <div class="state-item">Oregon - HALF OFF</div>
                    <div class="state-item">Pennsylvania - HALF OFF</div>
                    <div class="state-item">Rhode Island - HALF OFF</div>
                    <div class="state-item">South Carolina - HALF OFF</div>
                    <div class="state-item">South Dakota - HALF OFF</div>
                    <div class="state-item">Tennessee - HALF OFF</div>
                    <div class="state-item">Texas - HALF OFF</div>
                    <div class="state-item">Utah - HALF OFF</div>
                    <div class="state-item">Vermont - HALF OFF</div>
                    <div class="state-item">Virginia - HALF OFF</div>
                    <div class="state-item">Washington - HALF OFF</div>
                    <div class="state-item">West Virginia - HALF OFF</div>
                    <div class="state-item">Wisconsin - HALF OFF</div>
                    <div class="state-item">Wyoming - HALF OFF</div>
                </div>
            </div>
            
            <div class="contact-box">
                <h3>📞 Get Your HALF OFF Codes Now!</h3>
                <p>Telegram Bot: @HalfOffServicesBot</p>
                <p>Main Contact: @yrfrnd_spidy</p>
                <p>Support: @Eatsplugsus</p>
                <p>Channel: @flights_bills_b4u</p>
                <p style="margin-top: 20px; font-size: 18px;">✅ 50% OFF Guaranteed • 📍 All 50 States • ⏰ 24/7 Service</p>
            </div>
            
            <footer style="text-align: center; margin-top: 50px; padding-top: 20px; border-top: 1px solid rgba(255, 255, 255, 0.2);">
                <p>© 2024 Half OFF Services USA. All rights reserved.</p>
                <p>50% OFF discounts on all services across all 50 United States.</p>
            </footer>
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
            print(f"✅ HALF OFF Services Bot deployed!")
            print(f"💰 Discount: 50% OFF (Half OFF)")
            print(f"📍 Coverage: All 50 USA States")
            print(f"📊 New Service: BILLS HALF OFF added")
            print(f"📞 Admin ID: {ADMIN_ID}")
        else:
            print("🔧 Bot running in polling mode")
            
    except Exception as e:
        print(f"⚠️ Webhook setup: {e}")
    
    print("🔥 HALF OFF Services Bot Active!")
    print("🎯 Services: Food, Rides, Groceries, Shopping, Streaming, BILLS")
    print("💰 Bills Covered: Electricity, Water, Internet, Loans, Credit Cards, Rent, Insurance")
    print("🇺🇸 States: All 50 USA states covered")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
