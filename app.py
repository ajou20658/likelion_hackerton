from flask import Flask
from flask import request
from flask import Response
from flask import jsonify
import re
from krwordrank.word import KRWordRank
from krwordrank.hangle import normalize
from operator import itemgetter

app = Flask(__name__)


def preprocess_text(fname):
    with open(fname, encoding='utf-8') as f:
        docs = f.read()
        docs = docs.split('\n')  # 줄바꿈을 기준으로 리스트로 분리

        # "... " 이후의 내용을 제거한 후 전처리
        processed_docs = []
        for doc in docs:
            if " … " in doc:
                doc = doc.split(" … ")[0]
            doc = re.sub(r'[^\w\s]', '', doc).replace('\n', '')
            doc = re.sub(r'\b\d+[a-zA-Z가-힣]+\b', '', doc)
            doc = re.sub(r'[은는이가을를면]+\b','',doc)
            
            processed_docs.append(doc)
        return processed_docs

@app.route('/req',methods=['GET'])
def reqToServer():
    try:
        url = request.args.get('uri')
        print(url)
        fname = url
        texts=preprocess_text(fname)
    except:
        print('[Error] : Failed to access url')
        return None
    try:
        wordrank_extractor = KRWordRank(
            min_count = 5, # 단어의 최소 출현 빈도수 (그래프 생성 시)
            max_length = 10, # 단어의 최대 길이
            verbose = True
        )
        beta = 0.85    # PageRank의 decaying factor beta
        max_iter = 10

        keywords, rank, graph = wordrank_extractor.extract(texts, beta, max_iter)
        #keywords는 dict자료형 key:value 로 되어있음 

        common_keyword={"서울","부산","경기","강원","광주","전국","조기","지난","참가자들","피해","현장","대비","2023","있는","따르","오후","오전","경찰","열린","사건","따르면","받는",
                        "혐의","있다","예고","밝혔다","위한","위해","것으로","국내","해외","국외","한국","게임",
                        "글로벌","개발","공식","기업","고객","공식","대표","매출","브랜드","상반기","서비스","세계","스마트폰","올해","출시","케이스","패키지","함께","후보자",
                        "공개","기술","나선","분당","시리즈","시장","전년","전략적","전문","제25회","초청해","진행","인사","방송","모바일","마련된","YTN","vip","뉴스","신규","연구","영상",
                        "캐릭터","페이지에","검증","관련","미국","오픈","특별","이벤트","제품","준비","구축","제공","영업이익","영업","이익","콘텐츠","가운데","금융","기준","대한","사업",
                        "사장","상승","실적","아파트","연결","오른","이어","최대","최소","정부","지원","최근","투자","판매","개최","구속","남성","여성","대원들","동영상","사고","앞에서","지원","참가한",
                        "영향","다시","국제","슈퍼","열리","열리는","영향","해제","하와","인파","규모","만에","발생","회의","더불어민","동영상기사","상병","수사","원내","의원","장관","하고","혁신","경제","기록했다고",
                        "누락","단지","대상","발표","부사장","부회장","수출","이번","자회사","적자","지역","운전자","지역","중심으로","라이브","제6호","예능","오늘","동영상기","특파원","문제","대형","업데이트",
                        "실시","나선다","동기","맞아","연속","감소","인근에서","지나간","모두","최다","속보","추가","확진"
                        }
        filtered = {word: r for word, r in sorted(keywords.items(), key=itemgetter(1), reverse=True) if word not in common_keyword}
        filtered = dict(list(filtered.items())[:30])

        # for word, r in sorted(keywords.items(), key=lambda x:x[1], reverse=True)[:30]:
        #     if word in common_keyword:
        #         continue
        #     print('%8s:\t%.4f' % (word, r))
        
        return filtered
    except:
        print('[Error] : Logic Error')
        return None

if __name__ == '__main__':
    app.run(debug=True)

