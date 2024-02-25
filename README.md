# SUTERAKIRA
Work in progress.
## Running the project

This project runs on Python 3.12.2, but it probably also works on earlier versions. After defining your venv install requirements from `requirements.txt`<sup>[1]</sup>.

Define the following environment variables:
* `RUN_ENV`: This will determine the environment in which you bot will run, determining the settings file used. If running locally then it is recommended to use `local` and define the settings<sup>[2]</sup> you need in `settings/local.py` (use contents of `prod.py` as a reference.)
* `DISCORD_BOT_TOKEN`: The token of your bot.

The bot is now ready to run with `python suterakira.py`.

---

### Notes
1. A library included in requirements.py by the name of `psutils` might be difficult to install on Windows. If you give up and decide to run the bot without it, feel free to remove it from your `requirements.py` file and any references to it in the code.
2. Ensure that your bot has the needed access to the log channel you define in the settings file.
