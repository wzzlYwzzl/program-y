import sys
import os

sys.path.append('/Users/caoxiaojie/pythonCode/program-y/src')

from programy.clients.embed.client import MyEmbeddedBot

config_file = '/Users/caoxiaojie/pythonCode/program-y/test/template-y/config/xnix/config.yaml'

print("Initiating Client...")

my_bot = MyEmbeddedBot(config_file)
client_context = my_bot.create_client_context("testuser")
response = my_bot.process_question(client_context, "总市值大于100的股票")
print(response)