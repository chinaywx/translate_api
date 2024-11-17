from Crypto.Cipher import AES
from Crypto.Hash import MD5
import base64
from requests import session
from utils import get_useragent
import time
import random
import json


class YoudaoTranslater:
    def __init__(self) -> None:
        self.sess = session()
        # self.sess.proxies = {
        #     "http": "http://127.0.0.1:10809",
        #     "https": "http://127.0.0.1:10809",
        # }
        self.sess.headers = {
            "User-Agent": get_useragent(),
            "origin": "https://fanyi.youdao.com",
            "referer": "https://fanyi.youdao.com/",
        }
        self.sess.cookies.set(
            "OUTFOX_SEARCH_USER_ID_NCOO",
            f"{random.randint(100000000, 999999999)}.{random.randint(100000000, 999999999)}",
        )
        self.sess.cookies.set(
            "OUTFOX_SEARCH_USER_ID",
            f"{random.randint(100000000, 999999999)}@{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}",
        )
        params = {
                     "keyid": "webfanyi-key-getter",
                 } | self.__base_body("asdjnjfenknafdfsdfsd")
        res = self.sess.get("https://dict.youdao.com/webtranslate/key", params=params)
        t = res.json()
        self.key = t["data"]["secretKey"]

    def get_lan_list(self) -> dict:
        res = self.sess.get(
            "https://api-overmind.youdao.com/openapi/get/luna/dict/luna-front/prod/langType"
        )
        return res.json()["data"]["value"]["textTranslate"]

    def __sticTime(self) -> str:
        return str(int(time.time() * 1000))

    def __sign(self, t: str, key: str) -> str:
        return (
            MD5.new(
                f"client=fanyideskweb&mysticTime={t}&product=webfanyi&key={key}".encode()
            )
            .digest()
            .hex()
        )

    def __base_body(self, key: str) -> dict:
        t = self.__sticTime()
        return {
            "sign": self.__sign(t, key),
            "client": "fanyideskweb",
            "product": "webfanyi",
            "appVersion": "1.0.0",
            "vendor": "web",
            "pointParam": "client,mysticTime,product",
            "mysticTime": t,
            "keyfrom": "fanyi.web",
        }

    def __decode(self, src: str) -> dict:
        key = b"ydsecret://query/key/B*RGygVywfNBwpmBaZg*WT7SIOUP2T0C9WHMZN39j^DAdaZhAnxvGcCY6VYFwnHl"
        iv = b"ydsecret://query/iv/C@lZe2YzHtZ2CYgaXKSVfsb7Y4QWHjITPPZ0nQp87fBeJ!Iv6v^6fvi2WN@bYpJ4"
        cryptor = AES.new(
            MD5.new(key).digest()[:16], AES.MODE_CBC, MD5.new(iv).digest()[:16]
        )
        res = cryptor.decrypt(base64.urlsafe_b64decode(src))
        txt = res.decode("utf-8")
        return json.loads(txt[: txt.rindex("}") + 1])

    def translate(self, src: str, fromLan: str = "auto", toLan: str = "auto"):
        data = {
                   "i": src,
                   "from": fromLan,
                   "to": toLan,
                   "dictResult": True,
                   "keyid": "webfanyi",
               } | self.__base_body(self.key)
        res = self.sess.post("https://dict.youdao.com/webtranslate", data=data)
        return self.__decode(res.text)


if __name__ == "__main__":
    translater = YoudaoTranslater()
    
    text = """一种便携式拔草器，包括两根相互铰接的连接杆，所述连接杆的顶端固接有手柄，所述连接杆底端通过转轴连接有两个相对的夹板，所述转轴上设有限位块，所述两夹板的内侧设有相配对的锯齿，所述连接杆的铰接处固接有一根弹簧，所述连接杆为伸缩式连接杆。
本实用新型结构简单，操作方便；
省力、功效快、减轻劳动强度，能避免手被刺伤或划伤，无需蹲地操作；
可收缩，占用空间小，便于携带，连接杆与夹板之间的角度可调，不使用时，连接杆可折合，可收缩；
适用范围广泛，可适用不同身高的工作人员操作和不同长度的杂草。
本实用新型公开了一种新型拔草器，包括手把，所述手把的一侧内嵌有按钮，且手把的底端安装有伸缩柱，所述伸缩柱的前表面设置有连接孔，且伸缩柱的外表面套接有套筒，所述套筒的前表面设置有转动螺栓，且套筒的底端连接有脚踏板，所述套筒的内壁固定有固定杆，所述脚踏板的内部安装有轴承，所述轴承的内壁连接有转动板，所述转动板的内部安装有固定板，所述固定板的底端安装有爪刀。
本实用新型通过设置伸缩柱、套筒、连接孔与转动螺栓，可根据使用者的使用习惯，调整伸缩柱在套筒内的长度，调整完毕后，使用转动螺栓闯过连接孔将伸缩柱固定在套筒内壁，有效解决了无法根据个人习惯调整装置的长度的问题。
本实用新型提供一种新型除草夹，其结构由手柄、弹簧、固定块和锄身构成，两个手柄的顶端铰接，两个手柄内侧设置有弹簧；
一个手柄的上端外侧固定有固定块，固定块与锄身的顶端铰接，通过紧固旋钮固定。
本实用新型的一种新型除草夹和现有技术相比，具有设计合理、结构简单、易于加工，使用方便等特点，便于农业操作时进行除草使用，有效的提高了除草效率，降低了农民的劳动强度，而且本除草夹还具有锄头的作用，具有一物多用的优点。
本实用新型为一种钳式人力拔棉柴机，它由钳口、操纵手柄，滚轮组成。
操纵手柄上装有手柄角度、开度调节孔，起始弹簧。
该装置在棉田拔棉柴时，钳口夹住棉柴杆以后，用力下压操纵手柄，就可以将棉柴拔起。
劳动强度小、省力、不需强壮劳动力。
一种便捷式手提间苗器，属于农业器具制造技术领域，采用直杆、定片、捏把、拉线杆、动片、回位杆和提手构成，直杆的后端装有手把，捏把通过上轴连接在直杆的后端处，动片与定片通过下轴连接，回位杆与直杆之间连接有拉簧。
操作时，动片和定片之间的开口对准需要间掉的禾苗，捏紧捏把，使动片与定片合拢，将禾苗从田地拔出。
本实用新型操作方便，能够有效地降低劳动强度，间苗速度快，可行性强，结构简单。
本实用新型涉及一种农用工具，特别是一种玉米间苗夹，包括主夹杆和副夹杆，主夹杆和副夹杆通过铰轴连接形成一个夹钳，主夹杆和副夹杆上端为把手，主夹杆下端安装有底板，底板表面有波纹，底板下端连接有尖铲；
所述的副夹杆下端安装夹板，夹板与底板相对的一面安装有多个齿。
本实用新型提供的玉米间苗夹，先把主夹杆的尖铲插入到玉米苗的根部，翘动玉米苗的根，然后夹板与底板合拢，将根部已经活动的玉米苗夹持住拔起，提高了间苗的效率、减轻了劳动强度。
所述的副夹杆(2)下端安装夹板(4)，夹板(4)与底板(6)相对的一面安装有多个齿(5)，所述的主夹杆(1)上安装有距离测量杆(8)。
本实用新型涉及烟杆拨除专用工具，其特征在于烟杆拨除专用工具由鳄齿卡口(1)、力臂杆(2)、支撑杆(3)、底座(4)、手柄杆(5)和支撑轴(6)组成，鳄齿卡口(1)安装在力臂杆(2)上，力臂杆(2)连接在手柄杆(5)上，力臂杆(2)和手柄杆(5)连接处通过支撑轴(6)活连接在支撑杆(3)上，支撑杆(3)底部设有底座(4)。
本实用新型与现有技术相比有如下优点：设备轻便灵活，单手可拿起，适用于丘陵和山区的烟田，能够省力高效的将烟杆拔除。
本实用新型结构简单，主要用于田地里面杂草的拔除使用，无需弯腰，降低劳动强度，增加工作效率，且本实用新型设置了辅助夹板，使得在使用时不会因为接触面积过小而拉断杂草的情况。
除草者只要按下手柄，推杆推动支撑片折页，两片支撑片撑起，弹簧扩张，撑开杂草夹，然后将杂草夹插入杂草根部泥土，拔出手柄同时推杆上升，支撑片收起，杂草夹收紧，夹住杂草，拔出手柄就可以拔除杂草，除草者不弯腰、不费力就可以拔除杂草。"""
    result = translater.translate(text, toLan="en")
    a=[i[0]['tgt'].strip() for i in result['translateResult']]
    print('\n'.join(a))
