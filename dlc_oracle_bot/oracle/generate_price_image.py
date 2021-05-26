from datetime import datetime
import logging

from PIL import Image, ImageFont, ImageDraw

from dlc_oracle_bot.oracle.config import tweet_1_image_file, bold_font_file, semi_bold_font_file

logging.basicConfig(level=logging.DEBUG)


def generate_price_image(today_price: float, yesterdays_price: float, today_date: datetime, pair: str):
    first_tweet_image = Image.open(tweet_1_image_file)
    image_editable = ImageDraw.Draw(first_tweet_image)

    change = today_price - yesterdays_price
    percent_change = change / yesterdays_price

    font = ImageFont.truetype(bold_font_file, 191)
    image_editable.text(
        xy=(
            72, 191
        ),
        text=f'${today_price:,.2f}',
        fill=(
            255,
            255,
            255
        ),
        font=font
    )

    font = ImageFont.truetype(bold_font_file, 64)
    image_editable.text(
        xy=(
            72, 432
        ),
        text=f'{percent_change:+.2%} • 24HR',
        fill=(
            255,
            255,
            255
        ),
        font=font
    )

    font = ImageFont.truetype(semi_bold_font_file, 24)
    image_editable.text(
        xy=(
            122, 600
        ),
        text=f'@KrakenOracle - {pair} spot price as of {today_date.strftime("%B %d, %Y • %H:%M UTC")}',
        fill=(
            255,
            255,
            255
        ),
        font=font
    )

    first_tweet_image.save(f'data/announcement-tweet-1-{pair}-{today_date.isoformat()}.png')


if __name__ == '__main__':
    generate_price_image(
        yesterdays_price=38833.8,
        today_price=37737.9,
        today_date=datetime.today().replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        ),
        pair='BTCUSD'
    )
