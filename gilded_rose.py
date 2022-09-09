# -*- coding: utf-8 -*-

SULFURAS_NAME = "Sulfuras, Hand of Ragnaros"
BACKSTAGE_PASS_NAME = "Backstage passes to a TAFKAL80ETC concert"
AGED_BRIE_NAME = "Aged Brie"

class GildedRose(object):

    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            if item.name == SULFURAS_NAME:
                pass # Sulfuras is legendary, it never changes value or has to be sold
            elif item.name == AGED_BRIE_NAME:
                item.sell_in = item.sell_in - 1
                if item.quality < 50:
                    item.quality = item.quality + 1
                if item.sell_in < 0 and item.quality < 50:
                    item.quality = item.quality + 1
            elif item.name == BACKSTAGE_PASS_NAME:
                if item.quality < 50:
                    item.quality = item.quality + 1
                    if item.sell_in < 11:
                        if item.quality < 50:
                            item.quality = item.quality + 1
                    if item.sell_in < 6:
                        if item.quality < 50:
                            item.quality = item.quality + 1
                if item.sell_in <= 0:
                    item.quality = item.quality - item.quality
            else:
                if item.quality > 0:
                    item.quality -= 1
                item.sell_in -= 1
                if item.sell_in < 0:
                    if item.quality > 0:
                        item.quality -= 1


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
