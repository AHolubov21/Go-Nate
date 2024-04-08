import requests

bot_token = "xoxb-2130371976770-6066452493427-fMtngLOwJZ4OFvz82jQ3vx2e"
response = requests.post(
    "https://slack.com/api/auth.test",
    headers={"Authorization": f"Bearer {bot_token}"}
)
data = response.json()
bot_user_id = data.get("user_id")
print(f"Bot User ID: {bot_user_id}")