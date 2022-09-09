# -*- coding: utf-8 -*-
import pytest

from gilded_rose import Item, GildedRose, SULFURAS_NAME, AGED_BRIE_NAME, BACKSTAGE_PASS_NAME


def assert_items_equal(item1: Item, item2: Item):
    assert item1.sell_in == item2.sell_in
    assert item1.quality == item2.quality
    assert item1.name == item2.name


def test_name_unchanged():
    items = [Item("foo", 0, 0)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    assert "foo" == items[0].name


def test_quality_degrades():
    items = [Item("foo", 1, 1)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    assert_items_equal(items[0], Item("foo", 0, 0))
    
    
def test_quality_degrades_twice_as_fast_after_sell_by_date():
    """Once the sell by date has passed, Quality degrades twice as fast"""
    items = [Item("best before yesterday", -1, 10), Item("yet another item", -2, 1)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    assert_items_equal(items[0], Item("best before yesterday", -2, 8))
    assert_items_equal(items[1], Item("yet another item", -3, 0))


def test_quality_not_more_than_50():
    """The Quality of an item is never more than 50"""
    items = [Item("Aged Brie", 1, 50)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    assert_items_equal(items[0], Item("Aged Brie", 0, 50))

@pytest.mark.parametrize("item_name", (SULFURAS_NAME, AGED_BRIE_NAME, BACKSTAGE_PASS_NAME, "Foo"))
@pytest.mark.parametrize("sell_in", (-1, 0, 1))
def test_quality_never_negative(item_name, sell_in):
    """The Quality of an item is never negative"""
    items = [Item(item_name, sell_in, 0)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    assert items[0].quality >= 0

@pytest.mark.parametrize("start_sell_by, start_quality, expected_quality", (
    (10, 49, 50),
    (10, 47, 48),
    (11, 47, 48),
    (5, 40, 41),
    (1, 40, 41),
    (0, 40, 42),
    (-1, 40, 42),
    (0, 49, 50),
))
def test_aged_brie_quality_increases(start_sell_by, start_quality, expected_quality):
    """Aged Brie actually increases in Quality the older it gets"""
    items = [Item(AGED_BRIE_NAME, start_sell_by, start_quality)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    assert items[0].quality == expected_quality

def test_legendary_item():
    """'Sulfuras', being a legendary item, never has to be sold or decreases in Qualit"""
    items = [Item(SULFURAS_NAME, 5, 5)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    assert_items_equal(items[0], Item(SULFURAS_NAME, 5, 5))

def test_legendary_and_common_items():
    """'Sulfuras', being a legendary item, never has to be sold or decreases in Qualit"""
    items = [Item(SULFURAS_NAME, 5, 5), Item("Common", 5, 5)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    assert_items_equal(items[0], Item(SULFURAS_NAME, 5, 5))
    assert_items_equal(items[1], Item("Common", 4, 4))

@pytest.mark.parametrize("start_sell_by, start_quality, expected_quality", (
    (10, 49, 50),
    (10, 47, 49),
    (11, 47, 48),
    (5, 40, 43),
    (1, 40, 43),
    (0, 40, 0),
    (-1, 40, 0),
))
def test_backstage_passes(start_sell_by, start_quality, expected_quality):
    """'Backstage passes', like aged brie, increases in Quality as its SellIn value approaches;
    Quality increases by 2 when there are 10 days or less and by 3 when there are 5 days or less but
	Quality drops to 0 after the concert
    """
    items = [Item(BACKSTAGE_PASS_NAME, start_sell_by, start_quality)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    assert_items_equal(items[0], Item(BACKSTAGE_PASS_NAME, start_sell_by-1, expected_quality))
    