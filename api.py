from flask import Flask, request, jsonify
from ticker_news import get_articles_info, parse_article

app = Flask(__name__)


@app.route('/company_articles', methods=['GET'])
def get_news():
    company = request.args.get('company')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    get_body = request.args.get('get_body')
    articles_info = get_articles_info(company, start=start_date, end=end_date)

    if get_body is not None and get_body.lower() == 'true':
        articles = filter(lambda x: x is not None, [parse_article(info['link']) for info in articles_info])
        return jsonify([{'title': article.title, 'body': article.text} for article in articles])

    return jsonify([{'title': info['title']} for info in articles_info])


if __name__ == "__main__":
    app.run(host='0.0.0.0')
