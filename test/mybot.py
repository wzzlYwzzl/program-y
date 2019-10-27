import sys
import os

sys.path.append('/Users/caoxiaojie/pythonCode/program-y/src')

print(sys.argv)

# 添加运行时的参数供程序命令行解释
args = ['--config', '/Users/caoxiaojie/pythonCode/program-y/test/template-y/config/xnix/config.yaml', '--cformat', 'yaml', '--logging', '/Users/caoxiaojie/pythonCode/program-y/test/template-y/config/xnix/logging.yaml']


from programy.clients.embed.client import MyEmbeddedBot

config_file = '/Users/caoxiaojie/pythonCode/program-y/test/template-y/config/xnix/config.yaml'

print("Initiating Client...")

my_bot = MyEmbeddedBot(config_file)
client_context = my_bot.create_client_context("testuser")
response = my_bot.process_question(client_context, "Hello")
print(response)