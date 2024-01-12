from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")

DB_NAME = env.str("DB_NAME")
DB_PORT = env.str("DB_PORT")
DB_HOST = env.str("DB_HOST")
DB_PASS = env.str("DB_PASS")
DB_USER = env.str("DB_USER")

channels = [
    (-1001926837172, 'Test kanal', 'https://t.me/Faxriddinov_Backend'),
    (-1001926837172, 'Test kanal', 'https://t.me/Faxriddinov_Backend'),
    (-1001926837172, 'Test kanal', 'https://t.me/Faxriddinov_Backend')
            ]
