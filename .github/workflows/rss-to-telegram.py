import feedparser
import telegram
from telegram import bot
from telegraph import Telegraph

# 从环境变量中获取BOT_TOKEN和CHAT_ID
bot_token = os.environ['BOT_TOKEN']
chat_id = os.environ['CHAT_ID']
feed_url = os.environ['FEED_URL']

# 实例化Telegram bot和Telegraph对象
bot = telegram.Bot(bot_token)
telegraph = Telegraph(access_token=ACCESS_TOKEN)

def get_feed():
    # 用feedparser解析rss feed
    feed = feedparser.parse(feed_url)
    return feed

def send_to_telegram(html):
    # 内容通过Telegraph网站预览
    telegraph.create_page(html_content=html)
    response = telegraph.edit_page(
        page_path=telegraph.get_path(),
        title='RSS订阅'
    )
    # 将Telegraph文章转发给Telegram群组或者个人chatID
    bot.send_message(chat_id=chat_id, text=response['url'], disable_web_page_preview=True)

if __name__ == '__main__':
    feed = get_feed()

    for item in feed.entries:
        # 每个订阅中的文章生成HTML预览页
        html = f"<h3>{item.title}</h3><p>{item.summary}</p>" + \
               f"<a href='{item.link}'>{'阅读全文'}</a>"
        send_to_telegram(html)
