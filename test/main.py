import sys
import os

sys.path.append('/Users/caoxiaojie/pythonCode/program-y/src')

print(sys.argv)

# 添加运行时的参数供程序命令行解释
args = ['--config', '/Users/caoxiaojie/pythonCode/program-y/test/template-y/config/xnix/config.yaml', '--cformat', 'yaml', '--logging', '/Users/caoxiaojie/pythonCode/program-y/test/template-y/config/xnix/logging.yaml']
for a in args:
    sys.argv.append(a)

print(os.getcwd())

from programy.clients.events.console.client import ConsoleBotClient

print("Initiating Console Client...")
def run():
    console_app = ConsoleBotClient()
    console_app.run()

run()