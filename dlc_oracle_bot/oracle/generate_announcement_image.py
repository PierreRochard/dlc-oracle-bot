import logging
import math
from datetime import timezone, datetime

from PIL import Image, ImageFont, ImageDraw

from dlc_oracle_bot.oracle.config import tweet_2_image_file, font_file, monospace_font_file

logging.basicConfig(level=logging.DEBUG)


def generate_announcement_image(attestations: str, price: float, pair: str, exchange: str, maturation_time: datetime):
    my_image = Image.open(tweet_2_image_file)
    image_editable = ImageDraw.Draw(my_image)

    length = len(attestations)
    square_root = math.sqrt(length)
    width = int(square_root * 2 + 1) - 12
    height = round(square_root / 2)
    multiple = width * height
    last_row_diff = multiple - length

    attestations_font = ImageFont.truetype(monospace_font_file, 12)
    split_display_attestation = [attestations[i:i + width] for i in range(0, len(attestations), width)]
    display_attestation = '\n'.join(split_display_attestation)
    image_editable.text(
        xy=(
            490, 110
        ),
        text=display_attestation,
        fill=(
            255,
            255,
            255
        ),
        font=attestations_font
    )

    price_font = ImageFont.truetype(font_file, 42)
    image_editable.text(
        xy=(
            50, 212
        ),
        text=f'${price:,.2f} {pair}',
        fill=(
            255,
            255,
            255
        ),
        font=price_font
    )

    sub_price_font = ImageFont.truetype(font_file, 24)
    image_editable.text(
        xy=(
            50, 267
        ),
        text=f'Price • {exchange} Spot',
        fill=(
            255,
            255,
            255,
            int(255 * 0.7)
        ),
        font=sub_price_font
    )

    date_font = ImageFont.truetype(font_file, 42)
    image_editable.text(
        xy=(
            50, 366
        ),
        text=f'{maturation_time.strftime("%B %d, %Y")}',
        fill=(
            255,
            255,
            255
        ),
        font=date_font
    )

    time_font = ImageFont.truetype(font_file, 24)
    image_editable.text(
        xy=(
            50, 421
        ),
        text=f'At close {maturation_time.strftime("%H:%M UTC")}',
        fill=(
            255,
            255,
            255,
            int(255 * 0.7)
        ),
        font=time_font
    )

    my_image.save(f'data/announcement-tweet-2-{exchange}-{pair}-{maturation_time.isoformat()}.png')


if __name__ == '__main__':
    generate_announcement_image(
        attestations='fdd850fd057e3363727970746f77617463502d6b72616b656e2d4254435553442d323032312d30352d31325430303a30303a30302b30303a3030630cccf40a7e9d730f96cfe615d7349ba97cd80db0d5012fe420d9f4f6dac0f20014a1e58cf29625cd4884c12f31e9604d5f0340dd2abfbcaf99e8edec45740fdc3d28fea2ea8f2f0d6ad3e3ab118acf6eb55c3e3b902bf5f297562c2e4439e30555b75036cd8cc8dd64cb8630597482ad2add225ae4e6926627a3096eeee6351daa79e61f497e91e6749b7b7a1065f0324cf1a6a110abe0369f4379b3d7a1824d10fcad663d09c7e90fc2d7d752ffe7025d26fd2902ba336482e6ad5b1d5033c30d6fdd3dfdfb3531720196f101e61f8a16c9a5ad30b44d78bfe1aecc1d128934a563fa7876d2590736524d10eb425df989c891fb75947ace928e78344aeee9d6cc1f7c3f0298313786fda7de8702cc8ed350062c523596da3ccf30cf1974c725b4d0a3497e9d3e7d17867ee4b0b35ec27ae663a87edeb5750c41ecb69d0824158a49c39a86d39d150534476c0f3eb75ffb829880eebf4dea409ebe50eb432e61232e3ae70f0206204611b0e552a05c27e8bfbbf1bbb5e5c7e2bb42dccb1829cfa94dbf6eda362ab6aa6395c10260bd125cad38af4b33f382e1e07550263d8405836e844b36c2736fc3b7f5819c52aea09652e4a5de9cb4eadf08e0fa05671453b2f011c888e0b4c84f75127709ffa02d2fe87a39a0b210a2d2d12333fd3fd72f3cba12c05724fb58900e574aab10913cc9d076c407ba4efb591b27ac0502985d90633d0de8111a25865b5c9751faf4c91a37a3d4caec2be7d5b32ace947d3d01218fa19500d50290ffa710583b78b66adc9a7ba03c394cdc079f25ae65f6bb8ef199fb31aa1d2a01a16e9ce7693a74c1999d1777ecc8f5eae045cd995246b48d31fcb4751f2b4f38b403893844843311b113fbb65f44a10ac59d505c60e8830289655f0dc136f5d50dd2042c38935891e852fea9315880b7e9c520853938aef9b72f5ba1adbd4efc52f89078ed03a575e0f62a5ade3b8adae07bd518d9da7c41ec48eb1509d6e987352a02ea01bde9134ee938921b673b1a41d84bf7a3acab36f23544ad2d1a8769b94502bc953188f350dcc8d1ce8c73448c754af0590b5e9181c1bde7f9acb044bc8f8525a841551972ada0b15805bce88162c040a2e818ef370ca2c9e6cecaad37cdfa04b8f0be5c6d88faae3a64c4d3ab8389bad40dc170b936fd6a7e640fb6c2971c8f0259956798877eb579d642367dab273d8b48c2ec9feb279324dfc044963df61b825233f776d660a6b50260dbda44a6d23c63f92c2aa25258248be3e3730a0991bc6521e9f7c61a2bedb7b922006cc0ba529f5e55063cfd85e2b73d0a01ee0f39d92bb96e3c6c00e5097d00017b8ca736b446f6ce58177f7d1c328a27678258854e7a36905178d2ea02a2e28fdbe4a4248d1b91a419311a3c3f748113056bcce257286ddde5ac46f757eacffb2ffb2a5415f45ad448629791d20a7a75b47626317573acdc2a0d7ad122e0b1355d34e80bfa1836cdc2afe77c692c2dee526bb5367e6e8c7cbfafb55b550f7c88ff6a0093e2eb8ffdad717de6afd30b14fc502da3b1864f4524d6d111ddc5c8cf1de8c2b060270c892e9615bd3db3a2c998b620decd16799fb3cfabc690793715d5f7e09d2409ad63c0b19cf0fcf2cdfd4a5af6d5917d2977a90dc209cf8b308230ce8e40eec5b9fb174a4bb34f904aa9b30a67962b3b2bec6ff2588d62b675b03f7302a4a349ee86d3f582d3cfde4e8f8017790f4589f79ca915eb7604140e17faabde8d5cc64219f1e2e9da0935546487fe56fc8c7cecf5e14b0e9b4a93ec55e9cf3b49376522f7a1331dbc10509af3530c7a27e86d4763ba11048c88e834d233ab5d45950ffc30e101300130013001300131013101300131013101310130013101310130013101300131013001310131',
        price=37737.9,
        exchange='Kraken',
        maturation_time=datetime.today().replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        ),
        pair='BTCUSD'
    )
