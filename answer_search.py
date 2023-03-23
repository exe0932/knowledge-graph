# -*- coding: utf-8 -*-

# @Author : Eason_Chen

# @Time : 2023/3/23 上午 10:13

from py2neo import Graph

class AnswerSearcher:
    def __init__(self):
        # self.g = Graph("http://localhost:7474", username="neo4j", password="ji32k7au4a83") # 版本問題ValueError: The following settings are not supported: {'username': 'neo4j'}
        self.g = Graph("http://localhost:7474", auth=("neo4j", "ji32k7au4a83"))
        self.num_limit = 20

    '''执行cypher查询，并返回相应的结果'''
    def search_main(self, sqls):
        print("sqls", sqls)
        final_answers = list()
        for sql_ in sqls:
            print("sql_", sql_)
            question_type = sql_['question_type']
            queries = sql_['sql']
            answers = list()
            for query in queries:
                print("query", query)
                ress = self.g.run(query).data()
                print(ress)
                answers += ress
            final_answers = self.answer_prettify(question_type, answers)

        return

    '''根据对应的qustion_type，调用相应的回复模板'''
    def answer_prettify(self, question_type, answers):
        final_answer = []
        if not answers:
            return ''


if __name__ == '__main__':
    searcher = AnswerSearcher()
    a = [{'question_type': 'main_diagnosis_names_department_names', 'sql': [
        "MATCH (m:科室名称)-[r:疾病名称]->(n:主要诊断名称) where n.name = '急性鼻炎' return m.name, r.name, n.name"]}]
    searcher.search_main(a)