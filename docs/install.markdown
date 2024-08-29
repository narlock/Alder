---
layout: page
title: Install Guide
permalink: /install
---
<time>Aug 29, 2024</time>

# Local Installation
The official bot that runs this source code is found on the [narlock Discord server](https://discord.gg/eEbEYbXaNS). The Alder bot that runs on the narlock server is not open to join other servers. If you want to have the bot's functionality on your server or contribute to the main project, you will need to create and self host your own bot. The instructions below will show you how to run the Alder code for your own bot.

### Dependencies
- [Python 3.10+](https://www.python.org/)
- [MySQL](https://www.mysql.com/) or [MariaDB](https://mariadb.org/)
- [Alder API]() (Part of the AlderBot code repository)
- [Discord API](https://discord.com/developers/docs/intro)
- [Rogue Boss](https://github.com/narlock/RogueBoss) (optional)

### Python Modules
- [PyYAML](https://pypi.org/project/PyYAML/)
- [discord.py](https://github.com/Rapptz/discord.py)
- [requests](https://pypi.org/project/requests/)
- [Flask](https://pypi.org/project/Flask/)
- [PyMySQL](https://pypi.org/project/PyMySQL/)
- [Flask-SQLAlchemy](https://pypi.org/project/Flask-SQLAlchemy/)
- [marshmallow-sqlalchemy](https://pypi.org/project/marshmallow-sqlalchemy/)

## Python
This Discord bot is programmed using the [Python](https://www.python.org/) programming language. This means that if you wish to self host the bot for yourself or contribute to the bot's functionality, you will need to install Python.

By opening your terminal, you can verify your Python installation by using the command:
```sh
python3 --version
```

## MySQL
[MySQL](https://dev.mysql.com/downloads/mysql/) is the database management system used for Alder. This section is for properly configuring a fresh MySQL installation.

### Linux (via Advanced Package Tool)
Enter the following command in your terminal:
```sh
sudo apt install mysql-server
```
or for MariaDB, if your Linux distribution does not have `mysql-server` as a package:
```sh
sudo apt install mariadb-server
```

### macOS
It is recommended that you install MySQL Server through the [Homebrew package manager](https://brew.sh/). With Homebrew installed, enter the following command in your terminal:
```zsh
brew install mysql-server
```

### Windows
Installing the [MySQL Workbench](https://dev.mysql.com/downloads/workbench/) will be sufficient to run Alder. This documentation will not go over the functionalities or setup of MySQL Workbench. The remainder of the document for configuring MySQL will be using the command line interface.

### After MySQL is installed

Create a user for connecting to the MySQL database. This is recommended in cases where you use MySQL for other database management. By creating a user, we can use it specifically for Alder. To set up a user using the MySQL command line:

- Login to MySQL server as the root user using `sudo mysql`, or `mysql -u root -p` followed by the password for the root user. This will open MySQL command line interface and you will see a message like the following:

```
Welcome to the MySQL monitor.
```

- Create a new user that can access the MySQL database. Replace `new_user` and `new_password` with the name and password of the user you are creating.

```sql
CREATE USER 'new_user'@'localhost' IDENTIFIED BY 'new_password';
```

- Next, you will need to grant permissions to the new user. You can follow the following to grant the user access to every database.

```sql
GRANT ALL PRIVILEGES ON *.* TO 'new_user'@'localhost';
```

or use the following command to only give access to the `alder` database. You may need to create the database in a future step before granting permissions this way.

```sql
GRANT ALL PRIVILEGES ON `alder`.* TO 'new_user'@'localhost';
```

- Apply your changes by entering the following command:

```sql
FLUSH PRIVILEGES;
```

- Now, you can login to the MySQL server by using `mysql -u new_user -p`, where `new_user` is the username you created for the user. You will enter your password now to sign into the console. You can use this information when you are configuring the bot to connect to the MySQL database.

Next, you will need to import the [setupdb.sql]() file. This will configure all of the tables in the MySQL database that Alder uses. Open the MySQL command line interface, then use the following command while being in the same working directory as the file:

```sql
source setupdb.sql
```

This will create the __alder__ database and the tables. You can view each of them by entering:

```sql
SHOW TABLES;
```

If configured correctly, the response for showing tables should appear as follows:

```
mysql> SHOW TABLES;
+-----------------+
| Tables_in_alder |
+-----------------+
| accomplishment  |
| achievement     |
| dailytime       |
| dailytoken      |
| kanban          |
| monthtime       |
| rbuser          |
| streak          |
| todo            |
| triviaquestion  |
| user            |
+-----------------+
11 rows in set (0.00 sec)
```

## Running the Bot
To run the source for Alder, you will need to create your own Discord bot following the [Discord developers page](https://discord.com/developers/docs/intro). You will need to be familiar with configuring the Bot permissions and inviting it to your server. When inviting, give the Bot the `application.commands` and `bot` scopes. It is recommended that you give your bot access to all Discord intents. If you are new to setting up a bot, I recommend reading the Discord documentation on [configuring your bot](https://discord.com/developers/docs/quick-start/getting-started#configuring-your-bot).

After your bot has joined your server of choice, download the latest release from the [Alder Releases](https://github.com/narlock/AlderBot/releases) page.

### Python Virtual Environment
It is recommended that you use a [Python virtual environment](https://docs.python.org/3/library/venv.html) when you run the Alder code. This will enable us to install dependent Python modules to a specific environment instead of to our root installation. 

Create a Python virtual environment in the root directory of the Alder application.

```sh
python3 -m venv alder-env
```

This will create a directory named `alder-env`. We can now activate the virtual environment in our current terminal by entering the following command:

```sh
source alder-env/bin/activate
```

This will activate the virtual environment. We can now install the required Python modules by running the following commands:

```sh
pip install PyYAML                        # required for parsing configuration
pip install discord                       # required for Alder Bot
pip install requests                      # required for Alder Bot
pip install Flask                         # required for Alder API
pip install PyMySQL                       # required for Alder API
pip install Flask-SQLAlchemy              # required for Alder API
pip install marshmallow-sqlalchemy        # required for Alder API
```

Once all of these are installed, we can now configure the applications.

### Starting Configuration
Inside of the `config.yaml` file, located in the root directory of the release, we can begin the configuration. Begin by configuring the `mysql` section to match your MySQL setup:

```yaml
# Configure your MySQL configurations
mysql:
  user: replace-with-your-mysql-user-name
  password: replace-with-your-mysql-user-password
  host: localhost
  database: alder
```

Configurations for Discord are under the `discord` naming. We can configure the `server` attribute by obtaining the server's ID. For the remainder of the configuration, you will need to create the associated channels, roles, emojis, and rules. After you have created each of them, you can retrieve their IDs and set their values in the configuration file. The exception is the `command.id` fields. These can only be set after the Bot has been initialized for the first time. Read [Configuring command IDs](#configuring-command-ids) for more information.

### Running the Alder API
The Alder API is a [Flask](https://flask.palletsprojects.com/en/3.0.x/) REST API used for performing operations against the MySQL database tables. The Alder Discord Bot code will make HTTP request calls to the Alder API to interact with the MySQL database. To view the different types of HTTP endpoints offered by the API that the Bot will utilize, visit the [API Specification](/Alder/api-spec) page. We will need to run the Alder API in order for the Alder Bot to communicate with the MySQL database.

With your Python virtual environment activated, navigate to the `/api` directory of the application and run the main Python file:

```sh
python3 main.py
```

This will begin the instance of the Alder API. Flask will automatically set the port to `5000`. You will see these logs in your terminal when the application spins up:

```
 * Serving Flask app 'app'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

If you have [curl](https://curl.se/) installed, we can test the instance of the Alder API by executing the following command in a separate terminal:

```sh
curl --request POST \
  --url http://127.0.0.1:5000/user/search \
  --header 'Content-Type: application/json' \
  --data '{
	"limit": 5
}'
```

You should get a response back that looks like (or populated if you met the search criteria 😊)

```sh
[]
```

To test other API endpoints, there is a provided [Insomnia](https://insomnia.rest/) collection that contains folders for each of the resources. This is located inside of the `/api` directory and can be imported into Insomnia.

### Running the Alder Bot
Now that we are running the Alder API, we can run the Alder Bot. But first, we will need to store our Discord Bot Token on our machine. Navigate to your home directory. Inside of `Documents/narlock/Alder` (create the directory if it does not exist), create a `token` file and insert your Discord bot token into the contents of the file. The bot's configuration will specifically read from this file to access your Discord Bot's token. Alternatively, you can modify the `main.py` file and insert your token in directly, although, not recommended.

With your token in place, ensure that your Python virtual environment is activated. Navigate to the `/bot` directory and start the bot up with the following command:

```
python3 main.py
```

The bot will begin to start up. The bot will perform the following tasks on start up:
1. Leave servers that are not defined in the configuration file.
2. Begin to track activity time of users currently connected to dedicated activity tracking voice channels.
3. Set the status of Alder Bot.
4. Sync the slash commands with Discord.
5. Refresh role buttons in the role channel.
6. Begin sync time tracking task loop.

Upon completion, you will see this message in your terminal log:

```
2024-08-29 13:05:48 SUCCESS on_ready AlderBot is officially ready for use!
```

With no error messages occurring on start up, the Bot has successfully started. You should see your Bot appear online on Discord. You will now be able to execute and configure your commands.

### Configuring command IDs
Inside of the configuration file, there exists application command id locations. These are the Discord IDs of the commands offered by the Discord bot. After you have started the bot, it will sync the commands. You will see an information message like the following to know when the commands sync:
```
2024-08-29 13:05:48 INFO on_ready AlderBot Slash Commands Synced: 18
```
In my experience testing this, it may take a while for a Discord client to recognize the synced commands. You will know when the commands are synced when you type `/` into a text channel and the list of options appear:

<p align="center">
  <img src="./slashCommands.png" alt="Showing slash command sync" />
</p>

You will be able to obtain the IDs of the commands after the syncing process is completed.

## Backing up the database
If you wish to create a backup of the MySQL database. First ensure that the properties in the `config.yaml` file are configured correctly for the MySQL portion. Once verified, you can execute the bash script `./backup.sh`. A backup will be created under a backups directory. Please read the [Discord Developer Policy](https://support-dev.discord.com/hc/en-us/articles/8563934450327-Discord-Developer-Policy#:~:text=You%20may%20not%20request%2C%20access,been%20aggregated%20or%20de%2Didentified) before backing up.

## Additional Integrations
The following section is dedicated for other various integrations that Alder uses.

### Rogue Boss
[Rogue Boss](https://github.com/narlock/RogueBoss) is a simple "Boss Battle" simulator for building communities. Alder offers a front end solution for Rogue Boss by enabling a Rogue Boss application command. This application command can perform different integrations against the Rogue Boss application.

To integrate with Alder, run the Rogue Boss application (requires [Java](https://www.java.com/) 17). Then set the URL of Rogue Boss in the `config.yaml` file. This will enable the Rogue Boss game.

The purpose of this integration was to offer a special event during narlock's study streams. The default usage of Alder in the source code will only be enabled during a study stream, so error messages may indicate that a session is not live.