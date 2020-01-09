from elasticsearch import Elasticsearch
import pprint as ppr
import json

class ES_API:
    es = Elasticsearch(hosts="127.0.0.1", port=9200, http_auth=("elastic", "changeme"))   # 객체 생성
    @classmethod
    def srvHealthCheck(self):
        health = self.es.cluster.health()
        print (health)

    @classmethod
    def allIndex(self):
        # Elasticsearch에 있는 모든 Index 조회
        print (self.es.cat.indices())

    @classmethod
    def dataInsert(self):
        # ===============
        # 데이터 삽입
        # ===============
        with open("../json_doc_make/tst.json", "r", encoding="utf-8") as fjson:
            data = json.loads(fjson.read())
            for n, i in enumerate(data):
                doc = {"cont"   :i['cont'],
                       "mnagnnm":i["mnagnnm"],
                       "post"   :i["post"],
                       "rgdt"   :i["rgdt"],
                       "rgter"  :i["rgter"],
                       "tel"    :i["tel"],
                       "title"  :i["title"]}
                res = self.es.index(index="today19020301", doc_type="today", id=n+1, body=doc)
                print (res)

    @classmethod
    def searchAll(self, indx=None):
        # ===============
        # 데이터 조회 [전체]
        # ===============
        res = self.es.search(
            index = "today19020301", doc_type = "today",
            body = {
                "query":{"match_all":{}}
            }
        )
        print (json.dumps(res, ensure_ascii=False, indent=4))

    @classmethod
    def searchFilter(self):
        # ===============
        # 데이터 조회 []
        # ===============
        res = self.es.search(
            index = "today19020301", doc_type = "today",
            body = {
                "query": {"match":{"post":"산림교육문화과"}}
            }
        )
        ppr.pprint(res)

    @classmethod
    def createIndex(self, index, body):
        # ===============
        # 인덱스 생성
        # ===============
        self.es.indices.create(
            index = "today19020301",
            body = {
                "settings": {
                  "number_of_shards": 5
                },
                "mappings": {
                    "today":{
                        "properties": {
                            "cont":    {"type": "text"},
                            "mnagnnm": {"type": "text"},
                            "post":    {"type": "text"},
                            "rgdt":    {"type": "text"},
                            "rgter":   {"type": "text"},
                            "tel":     {"type": "text"},
                            "title":   {"type": "text"}
                        }
                    }
                }
            }
        )


ES_API.allIndex()
# ElaAPI.srvHealthCheck()
# ElaAPI.createIndex()
# ElaAPI.dataInsert()
# ElaAPI.searchAll()
# ElaAPI.searchFilter()

