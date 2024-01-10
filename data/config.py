from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")

channels = [
    (-1001926837172, 'Test kanal', 'https://t.me/Faxriddinov_Backend'),
    (-1001926837172, 'Test kanal', 'https://t.me/Faxriddinov_Backend'),
    (-1001926837172, 'Test kanal', 'https://t.me/Faxriddinov_Backend')
            ]
