from typing import Callable
# -*- coding: utf-8 -*-

SULFURAS_NAME = "Sulfuras, Hand of Ragnaros"
BACKSTAGE_PASS_NAME = "Backstage passes to a TAFKAL80ETC concert"
AGED_BRIE_NAME = "Aged Brie"

class GildedRose(object):

    def __init__(self, items):
        self.items = items

    @staticmethod
    def increment_quality_if(item: "Item", condition: Callable[["Item"], bool]):
        if condition(item):
            GildedRose.increment_quality(item)


    @staticmethod
    def increment_quality(item: "Item"):
        if item.quality < 50:
            item.quality += 1

    @staticmethod
    def decrement_quality(item: "Item"):
        if item.quality > 0:
            item.quality -= 1

    def update_quality(self):
        for item in self.items:
            if item.name == SULFURAS_NAME:
                continue # Sulfuras is legendary, it never changes value or has to be sold
            elif item.name == AGED_BRIE_NAME:
                item.sell_in -= 1
                self.increment_quality(item)
                if item.sell_in < 0:
                    self.increment_quality(item)
            elif item.name == BACKSTAGE_PASS_NAME:
                # apply(increment, increment_if, increment_if, decrement_sell_by, zero_if_passed)
                self.increment_quality(item)
                self.increment_quality_if(item, lambda i: i.sell_in <= 10)
                self.increment_quality_if(item, lambda i: i.sell_in <= 5)

                item.sell_in -= 1
                if item.sell_in < 0:
                    item.quality = 0
            else:
                self.decrement_quality(item)
                item.sell_in -= 1
                if item.sell_in < 0:
                    self.decrement_quality(item)




class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
