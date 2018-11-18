# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from .user_agent import  agents
import logging
import random


class UserAgentMiddleware(object):
    """ 换User-Agent """
    def process_request(self, request, spider):
        agent = random.choice(agents)
        request.headers["User-Agent"] = agent
        logging.info(agent)





















