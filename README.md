# TikTok Automation Script

This is an automation script that Pyppeteer uses to interact with TikTok. It allows you to log in to TikTok, search for a user, follow them, like their videos, and make predefined comments.

## Requirements

Before running the script, make sure you have the following installed:

- Python 3.x
- Pyppeteer (`pip install pyppeteer`)
- asyncio (comes pre-installed with Python 3.7+)
- JSON files with user information and comments.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/CHICO-CP/followers-tiktok.git
   ```
   ```bash
   cd followers-tiktok
   ```

2. Install the necessary dependencies:
```bash
pip install pyppeteer
```

3. Create the JSON files of users and comments by running the script. Files are automatically generated if they don't exist.

```bash
python TikTok-followers.py
```

Use

1. Modify the tiktok_users.json file with your TikTok user credentials:

```bash
{
    "users": [
        {"username": "your_tiktok_username", "password": "your_password"}
    ]
}
```

2. Edit the comments.json file with the comments you want to be posted:

```bash
{
    "comments": [
        "Buen video",
        "Eres el mejor",
        "Sigue así"
    ]
}
```

3. Run the script:

```bash
python script.py
```
You'll be asked to enter the name of the user you want to search for on TikTok.



# Functionality

**Log in to TikTok: Use the credentials provided in the tiktok_users.json file.**

**Find a user: Find the username you enter when prompted.**

**Follow User: Follow the found user.**

**Interact with videos: Like the user's videos.**

**Comment on videos: Post random comments from a predefined list in the comments.json file.**


# JSON files

tiktok_users.json: It contains the login credentials of TikTok users.

comments.json: It contains the comments that the script can post on TikTok videos.


Both files are created automatically if they do not exist. Make sure to edit them with the proper information.

# Warning

This script is intended for educational purposes only. Unauthorized use of bots or automation scripts on platforms like TikTok may violate their usage policies. Use this script at your own risk.

# Contributions

If you have suggestions or improvements, do not hesitate to fork the project and send a pull request.

# Developer

**Developer:** @Gh0stDeveloper

**Channel:** @TEAM_CHICO_CP
