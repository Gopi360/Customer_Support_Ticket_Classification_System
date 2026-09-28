"""Generate a synthetic customer-support ticket dataset (200 rows, 5 categories)."""
import random
import pandas as pd

random.seed(42)

openers = ["", "", "", "Hi, ", "Hello, ", "Please help. ", "Urgent: ", "Team, ", "Good morning, ", "Hi support, "]
closers = ["", "", "", " Please help.", " Kindly assist.", " Need this fixed soon.", " Thanks.", " This is affecting my work.", " Please advise."]

cores = {
    "Login Issue": [
        "I forgot my password and cannot login",
        "Password reset email is not arriving",
        "I am unable to sign in to my account",
        "The login page keeps saying invalid credentials",
        "My account got locked after too many login attempts",
        "The OTP for login is not being received on my phone",
        "I cannot log in even after resetting my password",
        "Login button does nothing when I click it",
        "It says my username does not exist but I have used it before",
        "Two-factor authentication code is rejected every time",
        "I keep getting logged out immediately after signing in",
        "The reset password link has expired again",
        "Unable to access the portal because my login is failing",
        "Single sign-on is not working for my account",
        "I am not able to log into the application from my laptop",
        "Sign in fails with an authentication failed message",
        "I entered the correct password but the system denies access",
        "My login session expires as soon as I enter the dashboard",
    ],
    "Application Error": [
        "The application shows an error while saving data",
        "I get a 500 internal server error when submitting the form",
        "The app crashes whenever I open the settings page",
        "Saving a record throws an unexpected exception",
        "An error message pops up saying something went wrong",
        "The upload feature fails with an error code",
        "The application freezes and then closes on its own",
        "I see a blank white screen after clicking submit",
        "Delete option gives an unknown error",
        "The app throws a null pointer error on the orders page",
        "Data is not getting saved and an error appears",
        "The system displays error 404 when opening my profile",
        "Export to file fails with a runtime error",
        "The application is showing a database connection error",
        "Form validation error appears even with correct inputs",
        "Attachments cannot be uploaded, the app returns an error",
        "The application quits unexpectedly while editing a record",
        "A bug causes duplicate entries and an error on save",
    ],
    "Report": [
        "Please help me generate my monthly sales report",
        "I need a report of all tickets closed last quarter",
        "The weekly summary report is not being generated",
        "Can you share the annual revenue report",
        "The report I downloaded has missing columns",
        "I need the attendance report for last month",
        "Please schedule a daily report to my email",
        "The dashboard report shows incorrect totals",
        "Need a custom report filtered by region and date",
        "Report export to Excel is giving an empty sheet",
        "I want a performance summary report for my team",
        "Where can I find the monthly billing statement report",
        "The scheduled report did not arrive this week",
        "Please provide an inventory report for the last 30 days",
        "I need to download the audit report for compliance",
        "Requesting a year-to-date expense report",
        "The PDF report is missing the charts section",
        "Kindly generate a customer activity report for March",
    ],
    "Account Update": [
        "I need to change my registered mobile number",
        "Please update my email address on the account",
        "I want to change the name on my profile",
        "Kindly update my billing address",
        "I need to add a new user to our company account",
        "Please remove an old employee from the account",
        "Requesting to change my account username",
        "I want to update my communication preferences",
        "Please change the primary contact for our organisation",
        "I need to update my company details in the profile",
        "Update my phone number, the old one is not in use",
        "Need to upgrade my account plan to the premium tier",
        "Please transfer the account ownership to my colleague",
        "I want to update the shipping address saved in my profile",
        "Can you correct the spelling of my name in the account",
        "I need to change the email used for notifications",
        "Please update my designation and department in the profile",
        "I would like to close my old account and update details on the new one",
    ],
    "Performance": [
        "The application is very slow today",
        "Pages take too long to load",
        "The system is lagging badly during working hours",
        "The dashboard takes several minutes to open",
        "Everything is running extremely slow since this morning",
        "Search results are taking forever to appear",
        "The app becomes unresponsive when many users are online",
        "Loading the orders page takes more than a minute",
        "There is a significant delay when saving records",
        "The website is very sluggish on my connection",
        "Screen transitions in the app are painfully slow",
        "The system hangs for a long time before responding",
        "Uploading a small file takes ages",
        "Response time has degraded a lot over the past week",
        "The application is slow and keeps timing out",
        "It takes a long time to switch between tabs in the app",
        "Report pages open very slowly compared to last month",
        "The software is so slow that we cannot finish our tasks",
    ],
}

extras = {
    "Login Issue": [" I tried it on both mobile and desktop.", " This started yesterday.", " I already cleared my browser cache.", ""],
    "Application Error": [" It started after the latest update.", " I have attached a screenshot.", " This happens every time I try.", ""],
    "Report": [" It is needed for tomorrow's meeting.", " Please send it in PDF format.", " The finance team is waiting for it.", ""],
    "Account Update": [" Please confirm once it is done.", " The details are attached.", " This is for our records.", ""],
    "Performance": [" It has been like this for two days.", " Other team members face the same issue.", " It was fine last week.", ""],
}


# Ambiguous tickets: mix vocabulary from other categories, labelled by the customer's main intent
hybrids = {
    "Login Issue": [
        "The login page is very slow and then shows an error, I still cannot sign in",
        "After I updated my email I cannot log in with the new one",
        "I got an error message when I tried to reset my password",
        "Login takes forever and my password is rejected",
        "I could not open the report because I am locked out of my account",
        "Sign in fails after the latest update of the application",
        "The app throws an error at the login screen every time",
        "My account details changed and now my password does not work",
    ],
    "Application Error": [
        "The app is slow and then crashes with an error on save",
        "Error while opening the report page, it shows a blank screen",
        "I updated my profile and the application threw an error",
        "After I logged in the app displayed an unexpected error",
        "The application crashed while I was generating a report",
        "Something went wrong when I tried to update my account details",
        "The app hangs and then shows an error message",
        "I get an error whenever I try to sign in through the mobile app",
    ],
    "Report": [
        "The report is taking very long to generate",
        "I cannot download the report because the page shows an error",
        "Need the report for my new account, please update it with my new name",
        "Report page asks me to login again and again",
        "The monthly report shows wrong account details",
        "I want a report on how slow the application has been this week",
        "Generating the sales report keeps failing with an error",
        "Please send the login activity report for our users",
    ],
    "Account Update": [
        "I cannot log in to change my mobile number, please update it for me",
        "My profile update fails with an error, please change my email manually",
        "The application is slow so please update my address from your side",
        "Please update my details, the report has my old name",
        "I want to change my password and my registered email",
        "After updating my number I cannot login to the account",
        "Need to add a new user, the page shows an error when I try",
        "Please change the account owner, the settings page is very slow",
    ],
    "Performance": [
        "Login is slow and the dashboard takes minutes to open",
        "The app is slow when I generate a report",
        "Saving data takes very long and sometimes throws an error",
        "Profile page is slow to load after I updated my details",
        "The system is lagging and I get logged out often",
        "Reports open very slowly and sometimes fail",
        "Everything is slow after the latest update and I see errors",
        "The application is sluggish and my account keeps timing out",
    ],
}

priority_weights = {
    "Login Issue": (["High", "Medium", "Low", "Critical"], [45, 30, 10, 15]),
    "Application Error": (["High", "Medium", "Low", "Critical"], [40, 25, 5, 30]),
    "Report": (["High", "Medium", "Low", "Critical"], [10, 45, 40, 5]),
    "Account Update": (["High", "Medium", "Low", "Critical"], [10, 35, 50, 5]),
    "Performance": (["High", "Medium", "Low", "Critical"], [35, 40, 10, 15]),
}
statuses = ["Open", "Closed", "In Progress"]

rows, seen = [], set()
for cat, phrases in cores.items():
    count = 0
    while count < 40:
        pool = phrases if count < 32 else hybrids[cat]
        core = random.choice(pool)
        text = random.choice(openers) + core + random.choice(extras[cat]) + random.choice(closers)
        text = text.strip()
        if text[0].islower():
            text = text[0].upper() + text[1:]
        if not text.endswith((".", "?", "!")):
            text += "."
        if text in seen:
            continue
        seen.add(text)
        pr, w = priority_weights[cat]
        rows.append({"ticket_description": text, "category": cat,
                     "priority": random.choices(pr, w)[0],
                     "status": random.choice(statuses)})
        count += 1

df = pd.DataFrame(rows).sample(frac=1, random_state=42).reset_index(drop=True)
df.insert(0, "ticket_id", [f"T{i+1:03d}" for i in range(len(df))])
df.to_csv("dataset/claude_tickets.csv", index=False)
print(df.shape)
print(df["category"].value_counts())
print(df.head(6).to_string())
