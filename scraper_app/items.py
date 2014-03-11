from scrapy.item import Item, Field


class WrapBootstrapTemplate(Item):
    item_hash = Field()
    title = Field()
    thumbnail = Field()
    description = Field()
    creator = Field()
    when = Field()
    bootstrap_version = Field()
    cost_single = Field()
    cost_multiple = Field()
    cost_extended = Field()
    purchases = Field()
