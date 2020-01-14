import time
from elasticsearch import Elasticsearch
import pprint as ppr
import json

from env import CONF_PATH


class ES_API:
    es = Elasticsearch(hosts="127.0.0.1", port=9200, http_auth=("jonathan", "dkssud.tptkddk"))   # 객체 생성

    @classmethod
    def __init__(cls, index_name=None):
        if index_name is not None:
            cls.index_name = index_name
        else:
            cls.index_name = "hello_my_world"

    @classmethod
    def srvHealthCheck(cls):
        health = cls.es.cluster.health()
        print (health)

    @classmethod
    def allIndex(cls):
        # Elasticsearch에 있는 모든 Index 조회
        print (cls.es.cat.indices())

    @classmethod
    def dataInsert(cls, code, market, name, df):
        # ===============
        # 데이터 삽입
        # ===============
        print(cls.index_name)
        # return
        for i in range(len(df)):
            key = df.index[i]
            dt = int(time.mktime(key.timetuple()))
            ll = df.iloc[i].to_json()
            doc = json.loads(ll)
            doc['code'] = code
            doc['market'] = market
            doc['name'] = name
            doc['date'] = int(time.mktime(key.timetuple()))*1000
            res = cls.es.index(index=cls.index_name, id=f'{code}-{dt}', body=doc)


    @classmethod
    def searchAll(cls, indx=None):
        # ===============
        # 데이터 조회 [전체]
        # ===============
        res = cls.es.search(
            index = cls.index_name, doc_type = "today",
            body = {
                "query":{"match_all":{}}
            }
        )
        print (json.dumps(res, ensure_ascii=False, indent=4))

    @classmethod
    def searchFilter(cls):
        # ===============
        # 데이터 조회 []
        # ===============
        res = cls.es.search(
            index = cls.index_name, doc_type = "today",
            body = {
                "query": {"match":{"post":"산림교육문화과"}}
            }
        )
        ppr.pprint(res)

    @classmethod
    def createIndex(cls, index, body):
        # ===============
        # 인덱스 생성
        # ===============
        with open(f'{CONF_PATH}/index.json', 'r') as f:
            body = json.load(f)

        print(body)
        cls.es.indices.create(
            index = cls.index_name,
            body = body
        )

    @classmethod
    def deleteIndex(cls):
        # ===============
        # 인덱스 생성
        # ===============

        cls.es.indices.delete(
            index = cls.index_name
        )


# ES_API.allIndex()
# ES_API.srvHealthCheck()
# ES_API().createIndex(None, None)
# ES_API().deleteIndex(None, None)
# ES_API.dataInsert()
# ES_API.searchAll()
# ES_API.searchFilter()

