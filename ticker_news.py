from pygooglenews import GoogleNews
from newspaper import Article


def get_articles_info(company_name, start=None, end=None):
    gn = GoogleNews()
    return gn.search(company_name, from_=start, to_=end)['entries']


def parse_article(article_link):
    try:
        article = Article(article_link)

        article.download()
        article.parse()
        return article
    except Exception:
        return None
