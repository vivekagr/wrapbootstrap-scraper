BOT_NAME = 'wrapbootstrap'

SPIDER_MODULES = ['scraper_app.spiders']

DATABASE = 'sqlite:///wrapbootstrap.db'

ITEM_PIPELINES = {
    'scraper_app.pipelines.WrapBootstrapPipeline': 100,
}
