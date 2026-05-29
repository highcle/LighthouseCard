"""全国の灯台カードデータをDBに初期投入するスクリプト。"""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from app.database import SessionLocal, engine, Base
from app.models import user, lighthouse, user_card  # noqa: F401
from app.models.lighthouse import Lighthouse
from app.models.user_card import UserCard

Base.metadata.create_all(bind=engine)

# qr_code_url: 現地でQRコードを読み取って判明した実際のURL
#   形式: https://www.kaiho.mlit.go.jp/info/lighthouse/card/{ランダムトークン}.html
#   None = まだ現地で確認できていない灯台

LIGHTHOUSES = [
    # ── 北海道 ────────────────────────────────────────────────────────────
    {"id": 1, "name": "沓形岬灯台", "region": "北海道・東北", "prefecture": "北海道", "latitude": 45.187, "longitude": 141.198, "is_climbable": False, "qr_code_url": None},
    {"id": 2, "name": "稚内灯台", "region": "北海道・東北", "prefecture": "北海道", "latitude": 45.414, "longitude": 141.680, "is_climbable": False, "qr_code_url": None},
    {"id": 3, "name": "宗谷岬灯台", "region": "北海道・東北", "prefecture": "北海道", "latitude": 45.523, "longitude": 141.934, "is_climbable": False, "qr_code_url": None},
    {"id": 4, "name": "紋別灯台", "region": "北海道・東北", "prefecture": "北海道", "latitude": 44.357, "longitude": 143.353, "is_climbable": False, "qr_code_url": None},
    {"id": 5, "name": "能取岬灯台", "region": "北海道・東北", "prefecture": "北海道", "latitude": 44.096, "longitude": 144.210, "is_climbable": False, "qr_code_url": None},
    {"id": 6, "name": "宇登呂灯台", "region": "北海道・東北", "prefecture": "北海道", "latitude": 44.025, "longitude": 144.906, "is_climbable": False, "qr_code_url": None},
    {"id": 7, "name": "納沙布岬灯台", "region": "北海道・東北", "prefecture": "北海道", "latitude": 43.396, "longitude": 145.816, "established_year": 1872, "description": "日本最東端に位置する灯台。1872年（明治5年）初点灯。北方領土を望む最東端の岬に立ち、霧の多い海域を照らし続けている。", "jcg_page_url": "https://www.kaiho.mlit.go.jp/01kanku/hakodate/lighthouse/nosappu.html", "is_climbable": False, "qr_code_url": None},
    {"id": 8, "name": "落石岬灯台", "region": "北海道・東北", "prefecture": "北海道", "latitude": 43.088, "longitude": 145.027, "is_climbable": False, "qr_code_url": None},
    {"id": 9, "name": "羅臼灯台", "region": "北海道・東北", "prefecture": "北海道", "latitude": 44.027, "longitude": 145.200, "is_climbable": False, "qr_code_url": None},
    {"id": 10, "name": "ノッカマップ埼灯台", "region": "北海道・東北", "prefecture": "北海道", "latitude": 43.340, "longitude": 145.558, "is_climbable": False, "qr_code_url": None},
    {"id": 11, "name": "花咲灯台", "region": "北海道・東北", "prefecture": "北海道", "latitude": 43.259, "longitude": 145.582, "is_climbable": False, "qr_code_url": None},
    {"id": 12, "name": "野付埼灯台", "region": "北海道・東北", "prefecture": "北海道", "latitude": 43.545, "longitude": 145.182, "is_climbable": False, "qr_code_url": None},
    {"id": 13, "name": "湯沸岬灯台", "region": "北海道・東北", "prefecture": "北海道", "latitude": 43.068, "longitude": 144.847, "is_climbable": False, "qr_code_url": None},
    {"id": 14, "name": "襟裳岬灯台", "name_kana": "えりもみさきとうだい", "region": "北海道・東北", "prefecture": "北海道", "latitude": 41.931, "longitude": 143.249, "established_year": 1889, "description": "北海道日高山脈の南端、襟裳岬に建つ灯台。年間272日も霧が発生する日本有数の霧の岬で、太平洋を行き交う船舶を導く。", "jcg_page_url": "https://www.kaiho.mlit.go.jp/01kanku/hakodate/lighthouse/erimo.html", "is_climbable": False, "qr_code_url": "https://www.kaiho.mlit.go.jp/info/lighthouse/card/0109lsa620mr.html"},
    {"id": 15, "name": "チキウ岬灯台", "region": "北海道・東北", "prefecture": "北海道", "latitude": 42.350, "longitude": 140.916, "is_climbable": False, "qr_code_url": None},
    {"id": 16, "name": "恵山岬灯台", "name_kana": "えさんみさきとうだい", "region": "北海道・東北", "prefecture": "北海道", "latitude": 41.807, "longitude": 141.178, "established_year": 1890, "description": "津軽海峡に面した岬に建つ灯台。活火山・恵山の麓に位置し、海峡を往来する船舶の安全を守る。", "jcg_page_url": "https://www.kaiho.mlit.go.jp/01kanku/hakodate/lighthouse/esan.html", "is_climbable": False, "qr_code_url": None},
    {"id": 17, "name": "葛登支岬灯台", "region": "北海道・東北", "prefecture": "北海道", "latitude": 41.828, "longitude": 140.993, "is_climbable": False, "qr_code_url": None},
    {"id": 18, "name": "鴎島灯台", "region": "北海道・東北", "prefecture": "北海道", "latitude": 42.033, "longitude": 139.830, "is_climbable": False, "qr_code_url": None},
    {"id": 19, "name": "稲穂岬灯台", "region": "北海道・東北", "prefecture": "北海道", "latitude": None, "longitude": None, "is_climbable": False, "qr_code_url": None},
    {"id": 20, "name": "茂津多岬灯台", "region": "北海道・東北", "prefecture": "北海道", "latitude": None, "longitude": None, "is_climbable": False, "qr_code_url": None},
    {"id": 21, "name": "弁慶岬灯台", "region": "北海道・東北", "prefecture": "北海道", "latitude": 42.803, "longitude": 139.736, "is_climbable": False, "qr_code_url": None},
    {"id": 22, "name": "神威岬灯台", "region": "北海道・東北", "prefecture": "北海道", "latitude": 43.334, "longitude": 140.337, "is_climbable": False, "qr_code_url": None},
    {"id": 23, "name": "日和山灯台", "region": "北海道・東北", "prefecture": "北海道", "latitude": 43.179, "longitude": 140.995, "is_climbable": False, "qr_code_url": None},
    {"id": 24, "name": "石狩灯台", "region": "北海道・東北", "prefecture": "北海道", "latitude": 43.249, "longitude": 141.398, "is_climbable": False, "qr_code_url": None},
    {"id": 25, "name": "増毛灯台", "region": "北海道・東北", "prefecture": "北海道", "latitude": 43.851, "longitude": 141.879, "is_climbable": False, "qr_code_url": None},
    {"id": 26, "name": "金比羅岬灯台", "region": "北海道・東北", "prefecture": "北海道", "latitude": 43.698, "longitude": 141.672, "is_climbable": False, "qr_code_url": None},
    # ── 東北 ──────────────────────────────────────────────────────────────
    {"id": 27, "name": "艫作埼灯台", "region": "北海道・東北", "prefecture": "青森県", "latitude": 40.639, "longitude": 139.929, "is_climbable": False, "qr_code_url": None},
    {"id": 28, "name": "龍飛埼灯台", "name_kana": "たっぴさきとうだい", "region": "北海道・東北", "prefecture": "青森県", "latitude": 41.254, "longitude": 140.349, "established_year": 1932, "description": "津軽半島最北端の龍飛岬に建つ灯台。強風で知られる岬に立ち、津軽海峡の船舶を導く。", "jcg_page_url": "https://www.kaiho.mlit.go.jp/02kanku/lighthouse/tappisaki.html", "is_climbable": False, "qr_code_url": None},
    {"id": 29, "name": "青森港北防波堤西灯台", "region": "北海道・東北", "prefecture": "青森県", "latitude": 40.830, "longitude": 140.723, "is_climbable": False, "qr_code_url": None},
    {"id": 30, "name": "平館灯台", "region": "北海道・東北", "prefecture": "青森県", "latitude": 41.220, "longitude": 140.631, "is_climbable": False, "qr_code_url": None},
    {"id": 31, "name": "大間埼灯台", "region": "北海道・東北", "prefecture": "青森県", "latitude": 41.553, "longitude": 141.024, "is_climbable": False, "qr_code_url": None},
    {"id": 32, "name": "尻屋埼灯台", "name_kana": "しりやさきとうだい", "region": "北海道・東北", "prefecture": "青森県", "latitude": 41.428, "longitude": 141.458, "established_year": 1876, "description": "本州最北東端に建つ白亜の灯台。寒立馬が放牧される荒涼とした岬に立つ、登れる灯台として親しまれている。", "jcg_page_url": "https://www.kaiho.mlit.go.jp/02kanku/lighthouse/shiriyazaki.html", "is_climbable": True, "qr_code_url": None},
    {"id": 33, "name": "鮫角灯台", "region": "北海道・東北", "prefecture": "青森県", "latitude": 40.568, "longitude": 141.512, "is_climbable": False, "qr_code_url": None},
    {"id": 34, "name": "陸中黒埼灯台", "region": "北海道・東北", "prefecture": "岩手県", "latitude": 40.019, "longitude": 141.832, "is_climbable": False, "qr_code_url": None},
    {"id": 35, "name": "碁石埼灯台", "region": "北海道・東北", "prefecture": "岩手県", "latitude": 39.078, "longitude": 141.838, "is_climbable": False, "qr_code_url": None},
    {"id": 36, "name": "岩井埼灯台", "region": "北海道・東北", "prefecture": "宮城県", "latitude": 38.836, "longitude": 141.779, "is_climbable": False, "qr_code_url": None},
    {"id": 37, "name": "大須埼灯台", "region": "北海道・東北", "prefecture": "宮城県", "latitude": 38.344, "longitude": 141.455, "is_climbable": False, "qr_code_url": None},
    {"id": 38, "name": "花淵灯台", "region": "北海道・東北", "prefecture": "宮城県", "latitude": 38.393, "longitude": 141.183, "is_climbable": False, "qr_code_url": None},
    {"id": 39, "name": "入道埼灯台", "name_kana": "にゅうどうさきとうだい", "region": "北海道・東北", "prefecture": "秋田県", "latitude": 39.990, "longitude": 139.697, "established_year": 1902, "description": "男鹿半島最北端に建つ白黒縞模様の灯台。日本海の夕日と絶景で知られる登れる灯台。", "is_climbable": True, "qr_code_url": None},
    {"id": 40, "name": "鵜ノ埼灯台", "region": "北海道・東北", "prefecture": "秋田県", "latitude": 39.789, "longitude": 139.900, "is_climbable": False, "qr_code_url": None},
    {"id": 41, "name": "酒田灯台", "region": "北海道・東北", "prefecture": "山形県", "latitude": 38.900, "longitude": 139.790, "is_climbable": False, "qr_code_url": None},
    {"id": 42, "name": "鼠ケ関灯台", "region": "北海道・東北", "prefecture": "山形県", "latitude": 38.332, "longitude": 139.567, "is_climbable": False, "qr_code_url": None},
    {"id": 43, "name": "鵜ノ尾埼灯台", "region": "北海道・東北", "prefecture": "福島県", "latitude": 37.920, "longitude": 141.033, "is_climbable": False, "qr_code_url": None},
    {"id": 44, "name": "塩屋埼灯台", "name_kana": "しおやさきとうだい", "region": "北海道・東北", "prefecture": "福島県", "latitude": 36.978, "longitude": 140.952, "established_year": 1898, "description": "いわき市小名浜に建つ白亜の灯台。美空ひばりの歌「みだれ髪」の舞台として有名な登れる灯台。", "is_climbable": True, "qr_code_url": None},
    # ── 関東・北陸・東海 ──────────────────────────────────────────────────
    {"id": 45, "name": "大津岬灯台", "region": "関東・北陸・東海", "prefecture": "茨城県", "latitude": 36.463, "longitude": 140.565, "is_climbable": False, "qr_code_url": None},
    {"id": 46, "name": "日立灯台", "region": "関東・北陸・東海", "prefecture": "茨城県", "latitude": 36.574, "longitude": 140.663, "is_climbable": False, "qr_code_url": None},
    {"id": 47, "name": "犬吠埼灯台", "name_kana": "いぬぼうさきとうだい", "region": "関東・北陸・東海", "prefecture": "千葉県", "latitude": 35.708, "longitude": 140.871, "established_year": 1874, "description": "本州最東端に近い岬の灯台。1874年（明治7年）初点灯。英国人技師が設計した白亜の灯台で、世界灯台100選に選ばれている。", "jcg_page_url": "https://www.kaiho.mlit.go.jp/03kanku/lighthouse/inubosaki.html", "is_climbable": True, "qr_code_url": None},
    {"id": 48, "name": "勝浦灯台", "region": "関東・北陸・東海", "prefecture": "千葉県", "latitude": 35.139, "longitude": 140.310, "is_climbable": False, "qr_code_url": None},
    {"id": 49, "name": "野島埼灯台", "name_kana": "のじまさきとうだい", "region": "関東・北陸・東海", "prefecture": "千葉県", "latitude": 34.900, "longitude": 139.883, "established_year": 1870, "description": "房総半島最南端に建つ灯台。1870年（明治3年）初点灯。相模湾と太平洋の境界を守る登れる灯台。", "jcg_page_url": "https://www.kaiho.mlit.go.jp/03kanku/lighthouse/nojima.html", "is_climbable": True, "qr_code_url": None},
    {"id": 50, "name": "洲埼灯台", "region": "関東・北陸・東海", "prefecture": "千葉県", "latitude": 34.958, "longitude": 139.863, "is_climbable": False, "qr_code_url": None},
    {"id": 51, "name": "八丈島灯台", "region": "関東・北陸・東海", "prefecture": "東京都", "latitude": 33.047, "longitude": 139.720, "is_climbable": False, "qr_code_url": None},
    {"id": 52, "name": "観音埼灯台", "name_kana": "かんのんざきとうだい", "region": "関東・北陸・東海", "prefecture": "神奈川県", "latitude": 35.656, "longitude": 139.775, "established_year": 1869, "description": "日本初の西洋式灯台。1869年（明治2年）に点灯。東京湾の入口を守り、150年以上の歴史を持つ登れる灯台。", "jcg_page_url": "https://www.kaiho.mlit.go.jp/03kanku/lighthouse/kannonzaki.html", "is_climbable": True, "qr_code_url": None},
    {"id": 53, "name": "剱埼灯台", "region": "関東・北陸・東海", "prefecture": "神奈川県", "latitude": 35.153, "longitude": 139.711, "is_climbable": False, "qr_code_url": None},
    {"id": 54, "name": "城ケ島灯台", "region": "関東・北陸・東海", "prefecture": "神奈川県", "latitude": 35.130, "longitude": 139.620, "is_climbable": False, "qr_code_url": None},
    {"id": 55, "name": "角田岬灯台", "region": "関東・北陸・東海", "prefecture": "新潟県", "latitude": 37.596, "longitude": 138.523, "is_climbable": False, "qr_code_url": None},
    {"id": 56, "name": "粟島灯台", "region": "関東・北陸・東海", "prefecture": "新潟県", "latitude": 38.487, "longitude": 139.289, "is_climbable": False, "qr_code_url": None},
    {"id": 57, "name": "弾埼灯台", "region": "関東・北陸・東海", "prefecture": "新潟県", "latitude": 38.258, "longitude": 138.456, "is_climbable": False, "qr_code_url": None},
    {"id": 58, "name": "姫埼灯台", "region": "関東・北陸・東海", "prefecture": "新潟県", "latitude": 38.099, "longitude": 138.582, "is_climbable": False, "qr_code_url": None},
    {"id": 59, "name": "佐渡大埼灯台", "region": "関東・北陸・東海", "prefecture": "新潟県", "latitude": 37.948, "longitude": 138.231, "is_climbable": False, "qr_code_url": None},
    {"id": 60, "name": "生地鼻灯台", "region": "関東・北陸・東海", "prefecture": "富山県", "latitude": 36.789, "longitude": 137.388, "is_climbable": False, "qr_code_url": None},
    {"id": 61, "name": "岩崎ノ鼻灯台", "region": "関東・北陸・東海", "prefecture": "富山県", "latitude": 36.589, "longitude": 137.088, "is_climbable": False, "qr_code_url": None},
    {"id": 62, "name": "能登観音埼灯台", "region": "関東・北陸・東海", "prefecture": "石川県", "latitude": 37.154, "longitude": 137.248, "is_climbable": False, "qr_code_url": None},
    {"id": 63, "name": "禄剛埼灯台", "name_kana": "ろっこうさきとうだい", "region": "関東・北陸・東海", "prefecture": "石川県", "latitude": 37.534, "longitude": 137.319, "established_year": 1883, "description": "能登半島最先端の珠洲市に建つ灯台。1883年（明治16年）初点灯。昼は太陽の光を、夜は灯台の光を放つとされる登れる灯台。", "is_climbable": True, "qr_code_url": None},
    {"id": 64, "name": "猿山岬灯台", "region": "関東・北陸・東海", "prefecture": "石川県", "latitude": 37.430, "longitude": 136.737, "is_climbable": False, "qr_code_url": None},
    {"id": 65, "name": "福浦灯台", "region": "関東・北陸・東海", "prefecture": "石川県", "latitude": 36.994, "longitude": 136.676, "is_climbable": False, "qr_code_url": None},
    {"id": 66, "name": "越前岬灯台", "region": "関東・北陸・東海", "prefecture": "福井県", "latitude": 35.972, "longitude": 135.957, "established_year": 1897, "is_climbable": True, "qr_code_url": None},
    {"id": 67, "name": "立石岬灯台", "region": "関東・北陸・東海", "prefecture": "福井県", "latitude": 35.731, "longitude": 135.688, "is_climbable": False, "qr_code_url": None},
    {"id": 68, "name": "初島灯台", "region": "関東・北陸・東海", "prefecture": "静岡県", "latitude": 35.098, "longitude": 139.076, "is_climbable": False, "qr_code_url": None},
    {"id": 69, "name": "石廊埼灯台", "name_kana": "いろうさきとうだい", "region": "関東・北陸・東海", "prefecture": "静岡県", "latitude": 34.599, "longitude": 138.848, "established_year": 1871, "description": "伊豆半島最南端の断崖に建つ灯台。荒波が打ち寄せる岬の先端に立ち、太平洋を行き交う船舶を導く。", "jcg_page_url": "https://www.kaiho.mlit.go.jp/03kanku/lighthouse/irozaki.html", "is_climbable": False, "qr_code_url": None},
    {"id": 70, "name": "清水灯台", "region": "関東・北陸・東海", "prefecture": "静岡県", "latitude": 35.019, "longitude": 138.541, "is_climbable": False, "qr_code_url": None},
    {"id": 71, "name": "御前埼灯台", "name_kana": "おまえざきとうだい", "region": "関東・北陸・東海", "prefecture": "静岡県", "latitude": 34.594, "longitude": 138.229, "established_year": 1874, "description": "駿河湾の入口、御前崎岬に建つ白亜の灯台。1874年（明治7年）初点灯。登れる灯台として人気を誇る。", "jcg_page_url": "https://www.kaiho.mlit.go.jp/03kanku/lighthouse/omaezaki.html", "is_climbable": True, "qr_code_url": None},
    {"id": 72, "name": "舞阪灯台", "region": "関東・北陸・東海", "prefecture": "静岡県", "latitude": 34.678, "longitude": 137.597, "is_climbable": False, "qr_code_url": None},
    {"id": 73, "name": "伊良湖岬灯台", "name_kana": "いらごみさきとうだい", "region": "関東・北陸・東海", "prefecture": "愛知県", "latitude": 34.580, "longitude": 137.000, "description": "渥美半島の先端、伊良湖岬に建つ灯台。伊勢湾の入口を守る。与謝野鉄幹・晶子夫妻が訪れたことで知られる。", "is_climbable": False, "qr_code_url": None},
    {"id": 74, "name": "野間埼灯台", "region": "関東・北陸・東海", "prefecture": "愛知県", "latitude": 34.883, "longitude": 136.793, "is_climbable": False, "qr_code_url": None},
    {"id": 75, "name": "贄埼灯台", "region": "関東・北陸・東海", "prefecture": "三重県", "latitude": 34.661, "longitude": 136.640, "is_climbable": False, "qr_code_url": None},
    {"id": 76, "name": "神島灯台", "region": "関東・北陸・東海", "prefecture": "三重県", "latitude": 34.499, "longitude": 136.987, "description": "三島由紀夫の小説「潮騒」の舞台となった神島に建つ灯台。", "is_climbable": False, "qr_code_url": None},
    {"id": 77, "name": "菅島灯台", "region": "関東・北陸・東海", "prefecture": "三重県", "latitude": 34.440, "longitude": 136.870, "is_climbable": False, "qr_code_url": None},
    {"id": 78, "name": "安乗埼灯台", "name_kana": "あのりさきとうだい", "region": "関東・北陸・東海", "prefecture": "三重県", "latitude": 34.481, "longitude": 136.808, "established_year": 1873, "description": "志摩半島の先端、安乗岬に建つ四角形の珍しい灯台。1873年（明治6年）初点灯の登れる灯台。", "jcg_page_url": "https://www.kaiho.mlit.go.jp/04kanku/lighthouse/anori.html", "is_climbable": True, "qr_code_url": None},
    {"id": 79, "name": "大王埼灯台", "name_kana": "だいおうさきとうだい", "region": "関東・北陸・東海", "prefecture": "三重県", "latitude": 34.273, "longitude": 136.918, "established_year": 1927, "description": "英虞湾の入口、大王崎に建つ灯台。「恋する灯台」に認定されており、カップルに人気の登れる灯台。", "jcg_page_url": "https://www.kaiho.mlit.go.jp/04kanku/lighthouse/daio.html", "is_climbable": True, "qr_code_url": None},
    {"id": 80, "name": "三木埼灯台", "region": "関東・北陸・東海", "prefecture": "三重県", "latitude": 33.993, "longitude": 136.131, "is_climbable": False, "qr_code_url": None},
    {"id": 81, "name": "二木島灯台", "region": "関東・北陸・東海", "prefecture": "三重県", "latitude": 33.851, "longitude": 136.083, "is_climbable": False, "qr_code_url": None},
    # ── 近畿・中国・四国 ──────────────────────────────────────────────────
    {"id": 82, "name": "経ケ岬灯台", "name_kana": "きょうがみさきとうだい", "region": "近畿・中国・四国", "prefecture": "京都府", "latitude": 35.789, "longitude": 135.219, "description": "近畿地方最北端の経ヶ岬に建つ灯台。丹後半島の岬に立ち、日本海を行き交う船を照らす。", "is_climbable": False, "qr_code_url": None},
    {"id": 83, "name": "余部埼灯台", "region": "近畿・中国・四国", "prefecture": "兵庫県", "latitude": 35.684, "longitude": 134.454, "is_climbable": False, "qr_code_url": None},
    {"id": 84, "name": "浜坂港矢城ケ鼻灯台", "region": "近畿・中国・四国", "prefecture": "兵庫県", "latitude": 35.643, "longitude": 134.452, "is_climbable": False, "qr_code_url": None},
    {"id": 85, "name": "江埼灯台", "region": "近畿・中国・四国", "prefecture": "兵庫県", "latitude": 34.631, "longitude": 135.040, "is_climbable": False, "qr_code_url": None},
    {"id": 86, "name": "赤穂御埼灯台", "region": "近畿・中国・四国", "prefecture": "兵庫県", "latitude": 34.660, "longitude": 134.413, "is_climbable": False, "qr_code_url": None},
    {"id": 87, "name": "梶取埼灯台", "region": "近畿・中国・四国", "prefecture": "和歌山県", "latitude": 33.700, "longitude": 135.520, "is_climbable": False, "qr_code_url": None},
    {"id": 88, "name": "樫野埼灯台", "name_kana": "かしのさきとうだい", "region": "近畿・中国・四国", "prefecture": "和歌山県", "latitude": 33.469, "longitude": 135.860, "description": "串本沖の大島に建つ灯台。1870年（明治3年）初点灯。トルコ軍艦エルトゥールル号の遭難慰霊碑が近くにある登れる灯台。", "established_year": 1870, "is_climbable": True, "qr_code_url": None},
    {"id": 89, "name": "潮岬灯台", "name_kana": "しおのみさきとうだい", "region": "近畿・中国・四国", "prefecture": "和歌山県", "latitude": 33.434, "longitude": 135.766, "established_year": 1873, "description": "本州最南端の岬に建つ灯台。1873年（明治6年）初点灯。太平洋の荒波を見渡せる登れる灯台として人気。", "jcg_page_url": "https://www.kaiho.mlit.go.jp/05kanku/lighthouse/shionomi.html", "is_climbable": True, "qr_code_url": None},
    {"id": 90, "name": "紀伊日ノ御埼灯台", "region": "近畿・中国・四国", "prefecture": "和歌山県", "latitude": 33.872, "longitude": 135.173, "is_climbable": False, "qr_code_url": None},
    {"id": 91, "name": "雑賀埼灯台", "region": "近畿・中国・四国", "prefecture": "和歌山県", "latitude": 34.171, "longitude": 135.133, "is_climbable": False, "qr_code_url": None},
    {"id": 92, "name": "友ヶ島灯台", "name_kana": "ともがしまとうだい", "region": "近畿・中国・四国", "prefecture": "和歌山県", "latitude": 34.282, "longitude": 135.047, "established_year": 1872, "description": "紀淡海峡に浮かぶ無人島・沖ノ島に建つ灯台。旧軍の砲台跡が残るラピュタの島として有名。", "jcg_page_url": "https://www.kaiho.mlit.go.jp/05kanku/lighthouse/tomogashima.html", "is_climbable": False, "qr_code_url": None},
    {"id": 93, "name": "美保関灯台", "name_kana": "みほのせきとうだい", "region": "近畿・中国・四国", "prefecture": "島根県", "latitude": 35.570, "longitude": 133.323, "established_year": 1898, "description": "島根半島最東端に位置する灯台。1898年（明治31年）初点灯。石造りの優美な姿と美保神社への参拝路が人気を呼ぶ登れる灯台。", "jcg_page_url": "https://www.kaiho.mlit.go.jp/08kanku/lighthouse/mihonoseki.html", "is_climbable": True, "qr_code_url": None},
    {"id": 94, "name": "出雲日御碕灯台", "name_kana": "いずもひのみさきとうだい", "region": "近畿・中国・四国", "prefecture": "島根県", "latitude": 35.436, "longitude": 132.627, "established_year": 1903, "description": "日本一高い石造り灯台（高さ43.65m）。1903年（明治36年）初点灯。出雲大社に近い景勝地に立ち、日本海を見渡す登れる灯台。", "jcg_page_url": "https://www.kaiho.mlit.go.jp/08kanku/lighthouse/hinomisaki.html", "is_climbable": True, "qr_code_url": "https://www.kaiho.mlit.go.jp/info/lighthouse/card/0806j18ffffb.html"},
    {"id": 95, "name": "白島埼灯台", "region": "近畿・中国・四国", "prefecture": "島根県", "latitude": 36.128, "longitude": 133.063, "is_climbable": False, "qr_code_url": None},
    {"id": 96, "name": "西郷岬灯台", "region": "近畿・中国・四国", "prefecture": "島根県", "latitude": 36.213, "longitude": 133.186, "is_climbable": False, "qr_code_url": None},
    {"id": 97, "name": "大岬灯台", "region": "近畿・中国・四国", "prefecture": "島根県", "latitude": 34.702, "longitude": 131.973, "is_climbable": False, "qr_code_url": None},
    {"id": 98, "name": "石見大崎鼻灯台", "region": "近畿・中国・四国", "prefecture": "島根県", "latitude": 34.600, "longitude": 132.114, "is_climbable": False, "qr_code_url": None},
    {"id": 99, "name": "六島灯台", "region": "近畿・中国・四国", "prefecture": "岡山県", "latitude": 34.277, "longitude": 133.932, "is_climbable": False, "qr_code_url": None},
    {"id": 100, "name": "大浜埼灯台", "region": "近畿・中国・四国", "prefecture": "広島県", "latitude": 34.342, "longitude": 133.017, "is_climbable": False, "qr_code_url": None},
    {"id": 101, "name": "小佐木島灯台", "region": "近畿・中国・四国", "prefecture": "広島県", "latitude": 34.264, "longitude": 132.969, "is_climbable": False, "qr_code_url": None},
    {"id": 102, "name": "佐木島灯台", "region": "近畿・中国・四国", "prefecture": "広島県", "latitude": 34.281, "longitude": 133.002, "is_climbable": False, "qr_code_url": None},
    {"id": 103, "name": "中ノ鼻灯台", "region": "近畿・中国・四国", "prefecture": "広島県", "latitude": 34.193, "longitude": 132.581, "is_climbable": False, "qr_code_url": None},
    {"id": 104, "name": "宇品灯台", "region": "近畿・中国・四国", "prefecture": "広島県", "latitude": 34.350, "longitude": 132.460, "is_climbable": False, "qr_code_url": None},
    {"id": 105, "name": "室津灯台", "region": "近畿・中国・四国", "prefecture": "山口県", "latitude": 34.013, "longitude": 131.889, "is_climbable": False, "qr_code_url": None},
    {"id": 106, "name": "徳山下松港徳山築港防波堤灯台", "region": "近畿・中国・四国", "prefecture": "山口県", "latitude": 33.957, "longitude": 131.820, "is_climbable": False, "qr_code_url": None},
    {"id": 107, "name": "草山埼灯台", "region": "近畿・中国・四国", "prefecture": "山口県", "latitude": 33.877, "longitude": 131.330, "is_climbable": False, "qr_code_url": None},
    {"id": 108, "name": "六連島灯台", "name_kana": "むつれじまとうだい", "region": "近畿・中国・四国", "prefecture": "山口県", "latitude": 33.968, "longitude": 130.888, "established_year": 1872, "description": "関門海峡の玄関口にある六連島に建つ灯台。1872年（明治5年）初点灯。日本最初期の洋式灯台の一つ。", "jcg_page_url": "https://www.kaiho.mlit.go.jp/07kanku/lighthouse/mutsure.html", "is_climbable": False, "qr_code_url": None},
    {"id": 109, "name": "角島灯台", "name_kana": "つのしまとうだい", "region": "近畿・中国・四国", "prefecture": "山口県", "latitude": 34.370, "longitude": 130.858, "established_year": 1876, "description": "下関市の角島に建つ石造りの灯台。1876年（明治9年）初点灯。エメラルドグリーンの海に囲まれ、日本屈指の絶景とされる登れる灯台。", "jcg_page_url": "https://www.kaiho.mlit.go.jp/07kanku/lighthouse/tsunoshima.html", "is_climbable": True, "qr_code_url": None},
    {"id": 110, "name": "虎ケ埼灯台", "region": "近畿・中国・四国", "prefecture": "山口県", "latitude": 34.083, "longitude": 130.823, "is_climbable": False, "qr_code_url": None},
    {"id": 111, "name": "孫埼灯台", "region": "近畿・中国・四国", "prefecture": "徳島県", "latitude": 34.108, "longitude": 134.720, "is_climbable": False, "qr_code_url": None},
    {"id": 112, "name": "蒲生田岬灯台", "name_kana": "かもだみさきとうだい", "region": "近畿・中国・四国", "prefecture": "徳島県", "latitude": 33.843, "longitude": 134.724, "description": "四国最東端の蒲生田岬に建つ灯台。紀伊水道の難所を照らす。", "is_climbable": False, "qr_code_url": None},
    {"id": 113, "name": "高松港玉藻防波堤灯台", "region": "近畿・中国・四国", "prefecture": "香川県", "latitude": 34.340, "longitude": 134.047, "is_climbable": False, "qr_code_url": None},
    {"id": 114, "name": "地蔵埼灯台", "region": "近畿・中国・四国", "prefecture": "香川県", "latitude": 34.333, "longitude": 133.809, "is_climbable": False, "qr_code_url": None},
    {"id": 115, "name": "男木島灯台", "name_kana": "おぎしまとうだい", "region": "近畿・中国・四国", "prefecture": "香川県", "latitude": 34.268, "longitude": 134.071, "description": "高松市沖の男木島に建つ白亜の灯台。瀬戸内海に浮かぶ島の灯台として人気の観光スポット。", "is_climbable": False, "qr_code_url": None},
    {"id": 116, "name": "鍋島灯台", "region": "近畿・中国・四国", "prefecture": "香川県", "latitude": 34.227, "longitude": 134.013, "is_climbable": False, "qr_code_url": None},
    {"id": 117, "name": "ウズ鼻灯台", "region": "近畿・中国・四国", "prefecture": "愛媛県", "latitude": 34.198, "longitude": 133.172, "is_climbable": False, "qr_code_url": None},
    {"id": 118, "name": "大下島灯台", "region": "近畿・中国・四国", "prefecture": "愛媛県", "latitude": 34.098, "longitude": 133.113, "is_climbable": False, "qr_code_url": None},
    {"id": 119, "name": "釣島灯台", "region": "近畿・中国・四国", "prefecture": "愛媛県", "latitude": 33.857, "longitude": 132.862, "is_climbable": False, "qr_code_url": None},
    {"id": 120, "name": "佐田岬灯台", "name_kana": "さだみさきとうだい", "region": "近畿・中国・四国", "prefecture": "愛媛県", "latitude": 33.344, "longitude": 132.003, "established_year": 1918, "description": "四国最西端の細長い佐田岬半島の先端に建つ灯台。1918年（大正7年）初点灯。豊後水道を往来する船の安全を守る。", "jcg_page_url": "https://www.kaiho.mlit.go.jp/06kanku/lighthouse/sadamisaki.html", "is_climbable": False, "qr_code_url": None},
    {"id": 121, "name": "室戸岬灯台", "name_kana": "むろとみさきとうだい", "region": "近畿・中国・四国", "prefecture": "高知県", "latitude": 33.257, "longitude": 134.178, "established_year": 1899, "description": "四国最南東端の室戸岬に建つ大型灯台。1899年（明治32年）初点灯。日本最大級の第1等フレネルレンズを備え、登れる灯台として人気。", "jcg_page_url": "https://www.kaiho.mlit.go.jp/05kanku/lighthouse/muroto.html", "is_climbable": True, "qr_code_url": None},
    {"id": 122, "name": "足摺岬灯台", "name_kana": "あしずりみさきとうだい", "region": "近畿・中国・四国", "prefecture": "高知県", "latitude": 32.715, "longitude": 133.003, "established_year": 1914, "description": "四国最南端の足摺岬に建つ白い灯台。1914年（大正3年）初点灯。ジョン万次郎ゆかりの地に立つ登れる灯台。", "jcg_page_url": "https://www.kaiho.mlit.go.jp/05kanku/lighthouse/ashizuri.html", "is_climbable": True, "qr_code_url": None},
    # ── 九州 ──────────────────────────────────────────────────────────────
    {"id": 123, "name": "部埼灯台", "region": "九州・沖縄", "prefecture": "福岡県", "latitude": 33.910, "longitude": 130.974, "is_climbable": False, "qr_code_url": None},
    {"id": 124, "name": "妙見埼灯台", "region": "九州・沖縄", "prefecture": "福岡県", "latitude": 33.908, "longitude": 130.790, "is_climbable": False, "qr_code_url": None},
    {"id": 125, "name": "津屋崎鼻灯台", "region": "九州・沖縄", "prefecture": "福岡県", "latitude": 33.802, "longitude": 130.471, "is_climbable": False, "qr_code_url": None},
    {"id": 126, "name": "筑前大島灯台", "region": "九州・沖縄", "prefecture": "福岡県", "latitude": 33.875, "longitude": 130.277, "is_climbable": False, "qr_code_url": None},
    {"id": 127, "name": "筑前相島灯台", "region": "九州・沖縄", "prefecture": "福岡県", "latitude": 33.801, "longitude": 130.382, "is_climbable": False, "qr_code_url": None},
    {"id": 128, "name": "波戸岬灯台", "region": "九州・沖縄", "prefecture": "佐賀県", "latitude": 33.580, "longitude": 129.930, "is_climbable": False, "qr_code_url": None},
    {"id": 129, "name": "大碆鼻灯台", "region": "九州・沖縄", "prefecture": "長崎県", "latitude": 33.407, "longitude": 129.532, "is_climbable": False, "qr_code_url": None},
    {"id": 130, "name": "対馬瀬鼻灯台", "region": "九州・沖縄", "prefecture": "長崎県", "latitude": 33.220, "longitude": 129.450, "is_climbable": False, "qr_code_url": None},
    {"id": 131, "name": "伊王島灯台", "region": "九州・沖縄", "prefecture": "長崎県", "latitude": 32.722, "longitude": 129.772, "is_climbable": False, "qr_code_url": None},
    {"id": 132, "name": "樺島灯台", "region": "九州・沖縄", "prefecture": "長崎県", "latitude": 32.540, "longitude": 129.840, "is_climbable": False, "qr_code_url": None},
    {"id": 133, "name": "大瀬埼灯台", "region": "九州・沖縄", "prefecture": "長崎県", "latitude": 32.730, "longitude": 128.850, "is_climbable": False, "qr_code_url": None},
    {"id": 134, "name": "口之津灯台", "region": "九州・沖縄", "prefecture": "長崎県", "latitude": 32.600, "longitude": 130.213, "is_climbable": False, "qr_code_url": None},
    {"id": 135, "name": "対馬棹埼灯台", "region": "九州・沖縄", "prefecture": "長崎県", "latitude": 34.681, "longitude": 129.323, "is_climbable": False, "qr_code_url": None},
    {"id": 136, "name": "豆酘埼灯台", "region": "九州・沖縄", "prefecture": "長崎県", "latitude": 34.073, "longitude": 129.211, "is_climbable": False, "qr_code_url": None},
    {"id": 137, "name": "三池港灯台", "region": "九州・沖縄", "prefecture": "熊本県", "latitude": 33.040, "longitude": 130.414, "is_climbable": False, "qr_code_url": None},
    {"id": 138, "name": "住吉灯台", "region": "九州・沖縄", "prefecture": "熊本県", "latitude": 32.649, "longitude": 130.630, "is_climbable": False, "qr_code_url": None},
    {"id": 139, "name": "湯島灯台", "region": "九州・沖縄", "prefecture": "熊本県", "latitude": 32.776, "longitude": 130.148, "is_climbable": False, "qr_code_url": None},
    {"id": 140, "name": "下大戸ノ鼻灯台", "region": "九州・沖縄", "prefecture": "熊本県", "latitude": 32.640, "longitude": 130.100, "is_climbable": False, "qr_code_url": None},
    {"id": 141, "name": "姫島灯台", "region": "九州・沖縄", "prefecture": "大分県", "latitude": 33.730, "longitude": 131.638, "is_climbable": False, "qr_code_url": None},
    {"id": 142, "name": "関埼灯台", "name_kana": "せきさきとうだい", "region": "九州・沖縄", "prefecture": "大分県", "latitude": 33.255, "longitude": 131.756, "established_year": 1901, "description": "豊後水道の入口、佐賀関半島の先端に建つ灯台。速吸の瀬戸と呼ばれる激流を行き交う船舶を導く。", "jcg_page_url": "https://www.kaiho.mlit.go.jp/06kanku/lighthouse/sekizaki.html", "is_climbable": False, "qr_code_url": None},
    {"id": 143, "name": "鶴御埼灯台", "region": "九州・沖縄", "prefecture": "大分県", "latitude": 32.940, "longitude": 132.072, "is_climbable": False, "qr_code_url": None},
    {"id": 144, "name": "細島灯台", "region": "九州・沖縄", "prefecture": "宮崎県", "latitude": 32.560, "longitude": 131.690, "is_climbable": False, "qr_code_url": None},
    {"id": 145, "name": "鞍埼灯台", "region": "九州・沖縄", "prefecture": "宮崎県", "latitude": 31.850, "longitude": 131.590, "is_climbable": False, "qr_code_url": None},
    {"id": 146, "name": "都井岬灯台", "name_kana": "といみさきとうだい", "region": "九州・沖縄", "prefecture": "宮崎県", "latitude": 31.379, "longitude": 131.156, "established_year": 1929, "description": "野生の岬馬（御崎馬）が生息する都井岬に建つ灯台。1929年（昭和4年）初点灯の登れる灯台で、太平洋を一望できる絶景スポット。", "jcg_page_url": "https://www.kaiho.mlit.go.jp/10kanku/lighthouse/toi.html", "is_climbable": True, "qr_code_url": None},
    {"id": 147, "name": "佐多岬灯台", "name_kana": "さたみさきとうだい", "region": "九州・沖縄", "prefecture": "鹿児島県", "latitude": 31.003, "longitude": 130.659, "established_year": 1871, "description": "本土最南端・佐多岬沖の小島に建つ灯台。1871年（明治4年）初点灯。日本で最も古い洋式灯台のひとつ。", "jcg_page_url": "https://www.kaiho.mlit.go.jp/10kanku/lighthouse/sata.html", "is_climbable": False, "qr_code_url": None},
    {"id": 148, "name": "薩摩長崎鼻灯台", "region": "九州・沖縄", "prefecture": "鹿児島県", "latitude": 31.009, "longitude": 130.723, "is_climbable": False, "qr_code_url": None},
    {"id": 149, "name": "屋久島灯台", "region": "九州・沖縄", "prefecture": "鹿児島県", "latitude": 30.368, "longitude": 130.495, "is_climbable": False, "qr_code_url": None},
    {"id": 150, "name": "長崎鼻灯台", "region": "九州・沖縄", "prefecture": "鹿児島県", "latitude": 32.165, "longitude": 130.018, "is_climbable": False, "qr_code_url": None},
    {"id": 151, "name": "釣掛埼灯台", "region": "九州・沖縄", "prefecture": "鹿児島県", "latitude": 31.711, "longitude": 130.170, "is_climbable": False, "qr_code_url": None},
    {"id": 152, "name": "笠利埼灯台", "region": "九州・沖縄", "prefecture": "鹿児島県", "latitude": 28.458, "longitude": 129.723, "is_climbable": False, "qr_code_url": None},
    # ── 沖縄 ──────────────────────────────────────────────────────────────
    {"id": 153, "name": "残波岬灯台", "name_kana": "ざんぱみさきとうだい", "region": "九州・沖縄", "prefecture": "沖縄県", "latitude": 26.395, "longitude": 127.676, "established_year": 1974, "description": "沖縄本島中部西海岸の残波岬に建つ灯台。1974年（昭和49年）初点灯。断崖絶壁の上に立つ沖縄最大級の登れる灯台。", "jcg_page_url": "https://www.kaiho.mlit.go.jp/11kanku/lighthouse/zanpa.html", "is_climbable": True, "qr_code_url": None},
    {"id": 154, "name": "久米島灯台", "region": "九州・沖縄", "prefecture": "沖縄県", "latitude": 26.336, "longitude": 126.754, "is_climbable": False, "qr_code_url": None},
    {"id": 155, "name": "知名埼灯台", "region": "九州・沖縄", "prefecture": "沖縄県", "latitude": 27.414, "longitude": 128.681, "is_climbable": False, "qr_code_url": None},
    {"id": 156, "name": "平安名埼灯台", "name_kana": "へんなさきとうだい", "region": "九州・沖縄", "prefecture": "沖縄県", "latitude": 24.776, "longitude": 125.449, "established_year": 1967, "description": "宮古島の東端、平安名埼に建つ灯台。1967年（昭和42年）初点灯の登れる灯台で、宮古海峡を行き交う船を見守る。", "jcg_page_url": "https://www.kaiho.mlit.go.jp/11kanku/lighthouse/henna.html", "is_climbable": True, "qr_code_url": None},
    {"id": 157, "name": "池間島灯台", "region": "九州・沖縄", "prefecture": "沖縄県", "latitude": 24.897, "longitude": 125.154, "is_climbable": False, "qr_code_url": None},
    {"id": 158, "name": "平久保埼灯台", "region": "九州・沖縄", "prefecture": "沖縄県", "latitude": 24.581, "longitude": 124.260, "is_climbable": False, "qr_code_url": None},
    {"id": 159, "name": "石垣御神埼灯台", "region": "九州・沖縄", "prefecture": "沖縄県", "latitude": 24.452, "longitude": 124.180, "jcg_page_url": "https://www.kaiho.mlit.go.jp/11kanku/lighthouse/ishigaki.html", "is_climbable": False, "qr_code_url": None},
    {"id": 160, "name": "西埼灯台", "name_kana": "いりさきとうだい", "region": "九州・沖縄", "prefecture": "沖縄県", "latitude": 24.203, "longitude": 123.681, "description": "与那国島西端に建つ灯台。日本最西端の有人島に位置し、台湾に最も近い日本の灯台。", "is_climbable": False, "qr_code_url": None},
]


def seed():
    db = SessionLocal()
    try:
        existing_count = db.query(Lighthouse).count()
        target_count = len(LIGHTHOUSES)

        if existing_count == target_count:
            print(f"灯台データは最新です ({existing_count} 件)")
            return

        print(f"灯台データを更新します: {existing_count} 件 → {target_count} 件")
        db.query(UserCard).delete()
        db.query(Lighthouse).delete()
        db.commit()

        for data in LIGHTHOUSES:
            lh = Lighthouse(**data)
            db.add(lh)

        db.commit()

        registered = sum(1 for lh in LIGHTHOUSES if lh.get("qr_code_url"))
        print(f"{target_count} 件の灯台データを投入しました。")
        print(f"  うち QRコードURL登録済み: {registered} 件")
        print(f"  うち QRコードURL未登録:   {target_count - registered} 件（現地訪問で追加予定）")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
