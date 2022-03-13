from typing import Dict, List
from recommendation_system.candidate_layer.base import BaseCandidateModel


class DemoCandidateModel(BaseCandidateModel):
    def __init__(self):
        super().__init__()

    def get_candidates(self, user_features: Dict, top_k: int) -> List[Dict]:
        candidates = [
            {
                "title": "2021 PyCon TW x PyHug Meetup",
                "image_url": "https://pbs.twimg.com/media/E_Skh8MVQAUmPHm.jpg",
                "subtitle": "PyHug 簡介： 歡迎來到 PyHUG。我們是一群活動於新竹周邊的 Python 程式員。 我們會定期舉辦技術討論與程式設計的聚會。非常歡迎你加入我們！",
            },
            {
                "title": "#7 | FAANG 工作環境跟外面有什麼不一樣？想進入 FAANG 就要聽這集！- Kir Chou",
                "image_url": "https://i.imgur.com/GrMYBUa.png",
                "subtitle": "這次邀請到的來賓是正在日本 Google 工作的 Kir 跟我們分享他在兩間 FAANG 工作過的經驗。想知道 Kir 在 FAANG 擔任軟體工程師的時候怎麼使用 Python 以及在公司內部推動重要的專案？另外，聽說他沒有刷題就加入 FAANG？！Wow 懶得刷題的聽眾快來聽，這集聽到賺到！PyCast 終於回歸拉！主持人在今年大會過後忙到被 👻 抓走沒時間錄新節目QQ為了讓 PyCast 再次偉大，邀請 Apple Podcast 的聽眾動動手指給我們五星跟留言建議🙏🏼🙏🏼🙏🏼#faang #japan #swe #makepycastgreatagain",
            },
            {
                "title": "贊助商 - Berry AI",
                "image_url": "https://i.imgur.com/ktvzhsu.jpg",
                "subtitle": "Berry AI 是一間位於台北的 AI 新創，致力於運用電腦視覺技術幫助速食業者蒐集數據，改善現有營運流程。技術團隊由一群充滿熱情的 AI 及軟體工程師組成，分別來自海內外知名學術機構與大型科技公司。此外，我們得到台灣上市公司飛捷科技的注資與支持，該公司擁有多年為大型企業落地工業電腦的經驗，提供穩定的資金來源與客戶關係。如今，Berry AI 已與數間全球 Top-10 速食業者展開合作，業務與團隊都迅速擴張中。欲了解更多訊息，請瀏覽 berry-ai.com。",
            },
            {
                "title": "他媽的給我買票喔！",
                "image_url": "https://i.imgur.com/WYiNl3z.png",
                "subtitle": "公道價八萬一",
            },
        ]

        return candidates[:top_k]
