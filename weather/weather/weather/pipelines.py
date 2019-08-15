# -*- coding: utf-8 -*-


# Define your item pipelines here

#

# Don't forget to add your pipeline to the ITEM_PIPELINES setting

# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os

import codecs

import json

import csv

from scrapy.exporters import JsonItemExporter

from openpyxl import Workbook




class JsonPipeline(object):

    def __init__(self):
        self.file = open('weather1.json', 'wb')

        self.exporter = JsonItemExporter(self.file, ensure_ascii=False)

        self.exporter.start_exporting()

    def process_item(self, item, spider):
        print('Write')

        self.exporter.export_item(item)

        return item

    def close_spider(self, spider):
        print('Close')

        self.exporter.finish_exporting()

        self.file.close()


class TxtPipeline(object):

    def process_item(self, item, spider):

        base_dir = os.getcwd()

        filename = base_dir + 'weather.txt'

        print('创建Txt')

        with open(filename, 'a') as f:
            f.write('城市:' + item['city'] + ' ')

            f.write(item['city_addition'] + ' ')

            f.write(item['city_addition2'] + '\n')

            f.write('天气:' + item['weather'] + '\n')

            f.write('温度:' + item['temperatureMin'] + '~' + item['temperatureMax'] + '℃\n')


class ExcelPipeline(object):

    def __init__(self):
        self.wb = Workbook()
        self.ws = self.wb.active

        self.ws.append(['省', '市', '县(乡)', '日期', '天气', '最高温', '最低温'])

    def process_item(self, item, spider):
        line = [item['city'], item['city_addition'], item['city_addition2'], item['data'], item['weather'],
                item['temperatureMax'], item['temperatureMin']]
        self.ws.append(line)
        self.wb.save('weather.xlsx')
        return item
