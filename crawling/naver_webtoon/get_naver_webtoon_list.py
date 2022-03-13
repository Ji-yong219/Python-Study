from requests import get
from bs4 import BeautifulSoup as bs

days_dic = {
    "월": "mon",
    "화": "tue",
    "수": "wed",
    "목": "thu",
    "금": "fri",
    "토": "sat",
    "일": "sun"
}

URL = "https://comic.naver.com/webtoon/weekdayList"

for kor_day, en_day in days_dic.items():
    FULL_URL = f"{URL}?week={en_day}"
    
    rsp = get(FULL_URL)
    soup = bs(rsp.text, "html.parser")

    LIs = soup.select("ul[class=img_list] > li")

    dic = {}
    size = len(LIs)
    for idx, LI in enumerate(LIs, 1):
        per = round(idx/size*100, 1)
        print(
            f"{kor_day}요일 {size}개 중 {idx}번째 크롤링 중... {per}%",
            end = "\r"
        )

        title = LI.select("div[class=thumb] > a")[0].attrs["title"]
        author = LI.select("dd[class=desc] > a")[0].text
        score = LI.select("span[class=star] + strong")[0].text

        dic[title] = {
            "author": author,
            "score": float(score)
        }
    
    sorted_list = sorted(
                      dic.items(),
                      key = lambda x: x[1]["score"],
                      reverse = True
                  )

    with open(f"naver_webtoon_{kor_day}.txt", "w", encoding="utf8") as f:
        for title, data in sorted_list:
            f.write(f"""{title} | {data["author"]} | {data["score"]}\n""")
