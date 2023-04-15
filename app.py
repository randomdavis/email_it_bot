import openai

with open('apikey.txt', 'r') as f:
    API_KEY: str = f.read().strip()

openai.api_key = API_KEY

common_prompt = "You work for the IT department. " \
                "Be verbose in your response. Clarify all of your thinking, and show all of your work. " \
                "Be as descriptive as possible as to why you are making certain choices or assumptions. " \
                "Use logical chain of thought as much as possible. " \
                "Utilize all clues given so far to uncover any potential issues, being genius, clever, and brilliant." \
                "Have all of your output be in Markdown format. "

email_analyzer_prompt = "You are an email analyzer bot specialized in understanding and extracting information from " \
                        "technical support emails. Analyze the given email, identify the context, main issue, " \
                        "any relevant details, and any missing information. Provide a clear and concise summary of " \
                        "the problem and its context. Example: 'The user is facing issues with Wi-Fi connectivity at " \
                        "their office and needs assistance in fixing it.' "

troubleshooting_bot_prompt = "You are a troubleshooting bot that provides step-by-step guidance based on the problem " \
                             "summary given by the Email Analyzer Bot. Generate a list of troubleshooting steps that " \
                             "can help the user resolve the issue they're facing. Be specific and clear in your " \
                             "instructions, and consider different possible causes for the issue. Example: '1. Check " \
                             "if the Wi-Fi is turned on. 2. Restart the router and try reconnecting. 3. Check if " \
                             "other devices can connect to the same Wi-Fi network.' "

it_specialist_bot_prompt = "You are an IT specialist bot that analyzes technical issues from a broader IT " \
                           "perspective. Using the problem summary from the Email Analyzer Bot, provide any " \
                           "additional insights or suggestions that could help resolve the issue, taking into account "\
                           "hardware, software, and potential compatibility issues. Example: 'The user might want to " \
                           "check if their device's network drivers are up-to-date, as outdated drivers could cause " \
                           "connectivity issues.' "

networking_specialist_bot_prompt = "You are a networking specialist bot that analyzes technical issues specifically " \
                                   "related to networking. Based on the problem summary from the Email Analyzer Bot, " \
                                   "provide any additional insights or suggestions that could help resolve the issue, "\
                                   "taking into account network configuration, equipment, and potential interference " \
                                   "sources. Example: 'The user should check if there's any physical obstruction or " \
                                   "electronic devices causing interference near the router, as this might affect the "\
                                   "Wi-Fi signal.' "

summary_and_decision_bot_prompt = "You are a summary and decision bot that consolidates information from multiple " \
                                  "specialized bots to determine the best course of action. Review the information " \
                                  "provided by the Email Analyzer, Troubleshooting, IT Specialist, and Networking " \
                                  "Specialist bots. Summarize their inputs and recommend the most effective solution " \
                                  "and reply to the user, taking into account all perspectives and suggestions. " \
                                  "Example: 'Based on the inputs from all bots, the user should first try the " \
                                  "troubleshooting steps, check their device's network drivers, and ensure there's no "\
                                  "interference near the router. A suggested reply to the user would include these " \
                                  "recommendations.' "


# Define the email content
email_title = input("Email Title: ")
email_body = input("Email Body:")
email = f"Title: {email_title}\nBody: {email_body}"

# Email Analyzer Bot
analyzer_response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
        {"role": "system", "content": f"{email_analyzer_prompt} {common_prompt}"},
        {"role": "user", "content": email}
    ]
)

analyzer_response_formatted = f"Email Analyzer Bot: {analyzer_response['choices'][0]['message']['content']}"

print(analyzer_response_formatted)

# Troubleshooting Bot
troubleshooting_response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
        {"role": "system", "content": f"{troubleshooting_bot_prompt} {common_prompt}"},
        {"role": "user", "content": f"{email}\n"
                                    f"{analyzer_response_formatted}"}]
)

troubleshooting_response_formatted = f"Troubleshooting Bot:" \
                                     f"{troubleshooting_response['choices'][0]['message']['content']}"

print(troubleshooting_response_formatted)

# IT Specialist Bot
it_specialist_response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
        {"role": "system", "content": f"{it_specialist_bot_prompt} {common_prompt}"},
        {"role": "user", "content": f"{email}\n"
                                    f"{analyzer_response_formatted}\n"
                                    f"{troubleshooting_response_formatted}"}]
)

it_specialist_response_formatted = f"IT Specialist Bot: {it_specialist_response['choices'][0]['message']['content']}"

print(it_specialist_response_formatted)

# Networking Specialist Bot
networking_specialist_response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
        {"role": "system", "content": f"{networking_specialist_bot_prompt} {common_prompt}"},
        {"role": "user", "content": f"{email}\n"
                                    f"{analyzer_response_formatted}\n"
                                    f"{troubleshooting_response_formatted}\n"
                                    f"{it_specialist_response_formatted}"}
    ]
)

networking_specialist_response_formatted = \
    f"Networking Specialist Bot: {networking_specialist_response['choices'][0]['message']['content']}"

print(networking_specialist_response_formatted)

# Summary and Decision Bot
summary_decision_response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
        {"role": "system", "content": f"{summary_and_decision_bot_prompt} {common_prompt}"},
        {"role": "user", "content": f"{email}\n"
                                    f"{analyzer_response_formatted}\n"
                                    f"{troubleshooting_response_formatted}\n"
                                    f"{it_specialist_response_formatted}\n"
                                    f"{networking_specialist_response_formatted}"}]
)

summary_decision_response_formatted = \
    f"Summary and Decision Bot: {summary_decision_response['choices'][0]['message']['content']}"

# Print the final response from the Summary and Decision Bot
print(summary_decision_response_formatted)
