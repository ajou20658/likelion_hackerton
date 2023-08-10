from flask import Flask
from flask import request
from flask import Response
from flask import jsonify
import re
from krwordrank.word import KRWordRank
from krwordrank.hangle import normalize


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

        common_keyword={"서울","있는","따르","오후","오전","경찰","열린","사건","따르면","받는","혐의","있다","예고"}

        filtered = {word: r for word, r in keywords.items() if word not in common_keyword}
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