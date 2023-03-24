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
        # print("sqls", sqls)
        final_answers = list()
        for sql_ in sqls:
            # print("sql_", sql_)
            question_type = sql_['question_type']
            queries = sql_['sql']
            # print("queries", queries)
            answers = list()
            for query in queries:
                # print("query", query)
                ress = self.g.run(query).data()
                # print("ress", ress)
                answers += ress
            final_answer = self.answer_prettify(question_type, answers)
            # print("final_answer", final_answer)
            if final_answer:
                final_answers.append(final_answer)
        return final_answers

    '''根据对应的qustion_type，调用相应的回复模板'''
    def answer_prettify(self, question_type, answers):
        final_answer = list()
        if not answers:
            return ''
        if question_type == 'main_diagnosis_names_department_names':
            desc = [i['m.name'] for i in answers]
            # print(desc)
            subject = answers[0]['n.name']
            final_answer = '{0}的症状建议挂的科室有:{1}'.format(subject, ';'.join(list(set(desc))[:self.num_limit]))
            # print("final_answer", final_answer)
        return final_answer


if __name__ == '__main__':
    searcher = AnswerSearcher()
    # a = [{'question_type': 'main_diagnosis_names_department_names', 'sql': [
    #     "MATCH (m:科室名称)-[r:疾病名称]->(n:主要诊断名称) where n.name = '急性鼻炎' return m.name, r.name, n.name"]}]
    # searcher.search_main(a)
