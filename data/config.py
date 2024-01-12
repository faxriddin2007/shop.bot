from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")

DB_NAME = env.list("DB_NAME")
DB_PASS = env.list("DB_PASS")
DB_HOST = env.list("DB_HOST")
DB_PORT= env.list("DB_PORT")
DB_USER = env.list("DB_USER")

channels = [
    (-1001926837172, 'Test kanal', 'https://t.me/Faxriddinov_Backend'),
    (-1001926837172, 'Test kanal', 'https://t.me/Faxriddinov_Backend'),
    (-1001926837172, 'Test kanal', 'https://t.me/Faxriddinov_Backend')
            ]
