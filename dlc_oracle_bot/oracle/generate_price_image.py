import logging

from PIL import Image, ImageFont, ImageDraw

logging.basicConfig(level=logging.DEBUG)


def generate_price_image(announcement, previous_day_announcement):
    first_tweet_image = Image.open('data/tweet.png')
    image_editable = ImageDraw.Draw(first_tweet_image)

    change = announcement['signed_outcome'] - previous_day_announcement['signed_outcome']
    percent_change = change / previous_day_announcement['signed_outcome']

    font = ImageFont.truetype('data/Acumin-BdPro.otf', 191)
    image_editable.text(
        xy=(
            72, 211
        ),
        text=f'${announcement["signed_outcome"]:,}',
        fill=(
            255,
            255,
            255
        ),
        font=font
    )

    font = ImageFont.truetype('data/Acumin-BdPro.otf', 64)
    image_editable.text(
        xy=(
            72, 432
        ),
        text=f'{percent_change:+.2%} ■ 24HR',
        fill=(
            255,
            255,
            255
        ),
        font=font
    )
    label_parts = announcement['label'].split('-')
    pair = label_parts[2]

    font = ImageFont.truetype('data/Acumin-RPro.otf', 24)
    image_editable.text(
        xy=(
            122, 605
        ),
        text=f'@KrakenOracle - {pair} spot price as of {announcement["maturation_time"].strftime("%B %d, %Y • %H:%M UTC")}',
        fill=(
            255,
            255,
            255
        ),
        font=font
    )

    first_tweet_image.save(f'data/announcement-tweet-1-{announcement["label"]}.png')
