"""
Copyright (c) 2016-2019 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
from programy.utils.logging.ylogger import YLogger

from programy.config.container import BaseContainerConfigurationData
from programy.config.bot.bot import BotConfiguration
from programy.scheduling.config import SchedulerConfiguration
from programy.storage.config import StorageConfiguration
from programy.utils.substitutions.substitues import Substitutions
from programy.utils.email.config import EmailConfiguration
from programy.triggers.config import TriggerConfiguration
from programy.clients.ping.config import PingResponderConfig


class ClientConfigurationData(BaseContainerConfigurationData):

    def __init__(self, name):
        BaseContainerConfigurationData.__init__(self, name)
        self._description = 'ProgramY AIML2.0 Client'
        self._bot_configs = []
        self._bot_configs.append(BotConfiguration("bot"))
        self._bot_selector = None
        self._renderer = None
        self._scheduler = SchedulerConfiguration()
        self._storage = StorageConfiguration()
        self._email = EmailConfiguration()
        self._triggers = TriggerConfiguration()
        self._responder = PingResponderConfig()

    @property
    def description(self):
        return self._description

    @property
    def configurations(self):
        return self._bot_configs

    @property
    def bot_selector(self):
        return self._bot_selector

    @property
    def scheduler(self):
        return self._scheduler

    @property
    def storage(self):
        return self._storage

    @property
    def renderer(self):
        return self._renderer

    @property
    def email(self):
        return self._email

    @property
    def triggers(self):
        return self._triggers

    @property
    def responder(self):
        return self._responder

    def check_for_license_keys(self, license_keys):
        BaseContainerConfigurationData.check_for_license_keys(
            self, license_keys)

    def load_configuration(self, configuration_file, bot_root, subs: Substitutions = None):
        client = configuration_file.get_section(self.section_name)
        if client is None:
            YLogger.error(
                None, 'Client section named [%s] not found, trying "client"', self.section_name)
            client = configuration_file.get_section('client')

        if client is not None:
            self.load_configuration_section(
                configuration_file, client, bot_root, subs)
        else:
            YLogger.error(None, 'No client section not found!')

    def load_configuration_section(self, configuration_file, section, bot_root, subs: Substitutions = None):
        """加载client section中的内容，比如console section中的内容。
        """
        assert(configuration_file is not None)

        if section is not None:  # 这里获取的是client section通用的配置
            self._description = configuration_file.get_option(section, "description",
                                                              missing_value='ProgramY AIML2.0 Client', subs=subs)

            # 读取配置文件中定义的bot的名字，list
            bot_names = configuration_file.get_multi_option(
                section, "bot", missing_value="bot", subs=subs)
            first = True
            for name in bot_names:
                # 这里就是用来加载bot配置和brain配置
                if first is True:
                    # 要求配置文件中必须有一个section名字是bot的配置节
                    config = self._bot_configs[0]
                    first = False

                else:
                    config = BotConfiguration(name)
                    self._bot_configs.append(config)

                config.load_configuration(
                    configuration_file, bot_root, subs=subs)

            """为什么会有多个bot，为什么需要bot_selector？
            按照目前的理解，通过多个bot可以是回答的问题不会因为每次问题相同而结果一样，为了应对这种场景。
            """

            # 读取client中的bot_selector配置项
            self._bot_selector = configuration_file.get_option(section, "bot_selector",
                                                               missing_value="programy.clients.client.DefaultBotSelector",
                                                               subs=subs)

            # 读取schedular配置section
            self._scheduler.load_config_section(
                configuration_file, section, bot_root, subs=subs)

            # 读取storage配置section
            self._storage.load_config_section(
                configuration_file, section, bot_root, subs=subs)

            # 读取renderer配置项，renderer的作用就是对结果进行渲染包装。
            self._renderer = configuration_file.get_option(
                section, "renderer", subs=subs)

            # 读取email配置节
            self._email.load_config_section(
                configuration_file, section, bot_root, subs=subs)

            # 读取trigger配置节
            self._triggers.load_config_section(
                configuration_file, section, bot_root, subs=subs)

            # 读取responder配置节，responder健康状况的监听器，接受外界ping请求。
            self._responder.load_config_section(
                configuration_file, section, bot_root, subs=subs)

        else:
            YLogger.warning(
                self, "No bot name defined for client [%s], defaulting to 'bot'.", self.section_name)
            self._bot_configs[0]._section_name = "bot"
            self._bot_configs[0].load_configuration(
                configuration_file, bot_root, subs=subs)

    def to_yaml(self, data, defaults=True):

        assert (data is not None)

        if defaults is True:
            data['description'] = 'ProgramY AIML2.0 Client'
            data['bot'] = 'bot'
            data['bot_selector'] = "programy.clients.client.DefaultBotSelector"

            data[self._scheduler.id] = {}
            self._scheduler.to_yaml(data[self._scheduler.id], defaults)

            data['renderer'] = "programy.clients.render.text.TextRenderer"

        else:
            data['description'] = self._description
            data['bot'] = self._bot_configs[0].id
            data['bot_selector'] = self.bot_selector

            data[self._scheduler.id] = {}
            self._scheduler.to_yaml(data[self._scheduler.id], defaults)

            data['email'] = {}
            self._email.to_yaml(data['email'], defaults)

            data['triggers'] = {}
            self._email.to_yaml(data['triggers'], defaults)

            data['responder'] = {}
            self._email.to_yaml(data['responder'], defaults)

            data['renderer'] = self.renderer
