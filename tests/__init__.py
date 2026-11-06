import os

# Set before any project module reads the configuration.
os.environ["BOT_TOKEN"] = "123456:TEST_TOKEN"
os.environ["ADMIN_IDS"] = "1000"
os.environ["GEMINI_API_KEY"] = ""
os.environ["DESMOS_API_KEY"] = ""
os.environ["SQLITE_PATH"] = ":memory:"
os.environ["DATABASE_URL"] = os.environ.get("TEST_DATABASE_URL", "")
