from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from crewai import Agent, Task, Crew, LLM
import os

# ========== YAHAN APNI DETAILS BHARO ==========
TELEGRAM_BOT_TOKEN = "8929738339:AAGsJ2UGIXQaTe0S9d6404RftIFb7A11eGY"
GEMINI_API_KEY = "AQ.Ab8RN6KrGRU_X-XPOiA8YifZKRzgLD2YvWjnnZewmS8gK-njDw"
# ==============================================

# Gemini LLM setup
llm = LLM(model="gemini/gemini-3.5-flash", api_key="AQ.Ab8RN6KrGRU_X-XPOiA8YifZKRzgLD2YvWjnnZewmS8gK-njDw")

# Agents
researcher = Agent(
    role="Researcher",
    goal="Kisi bhi topic ki research karna",
    backstory="Main research karta hoon aur important points nikalta hoon",
    llm=llm,
    verbose=False
)

writer = Agent(
    role="Writer",
    goal="Research se short report likhna",
    backstory="Main clear aur simple report likhta hoon",
    llm=llm,
    verbose=False
)

# Telegram Bot functions
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Namaste! 👋\n\n"
        "Main aapka AI Agent hoon.\n"
        "Mujhe koi bhi topic bhejo, main research karke report bana dunga.\n\n"
        "Example: AI Agents kya hote hain"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    # User ko batao ki kaam shuru ho gaya
    await update.message.reply_text("⏳ Agent kaam shuru kar raha hai... thoda wait karein...")

    try:
        # Tasks
        task1 = Task(
            description=f"Is topic par research karo: {user_message}",
            expected_output="5-7 important points",
            agent=researcher
        )

        task2 = Task(
            description=f"Research se short aur clear report likho topic: {user_message}",
            expected_output="Ek short structured report",
            agent=writer
        )

        # Crew
        crew = Crew(
            agents=[researcher, writer],
            tasks=[task1, task2],
            verbose=False
        )

        # Async version use karo
        result = await crew.kickoff_async()

        # Result bhejo
        await update.message.reply_text(f"✅ Report Ready:\n\n{result}")

    except Exception as e:
        await update.message.reply_text(f"❌ Error aaya: {str(e)}")

def main():
    print("Telegram Bot start ho raha hai...")
    
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot chal raha hai... Telegram pe message bhejo!")
    app.run_polling()

if __name__ == "__main__":
    main()