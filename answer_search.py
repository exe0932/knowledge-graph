# -*- coding: utf-8 -*-

# @Author : Eason_Chen

# @Time : 2023/3/23 上午 10:13

from py2neo import Graph

class AnswerSearcher:
    def __init__(self):
        # self.g = Graph("http://localhost:7474", username="neo4j", password="ji32k7au4a83") # 版本問題ValueError: The following settings are not supported: {'username': 'neo4j'}
        self.g = Graph("http://localhost:7474", auth=("neo4j", "ji32k7au4a83"))
        self.num_limit = 100

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

        elif question_type == 'main_complaints_diagnosis_names':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '根据病人描述的 : {0}，专业医生推断的疾病名称为 : {1}'.format(subject, ';'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'department_names_doctor_names':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}有以下这些医生可以选择 : {1}'.format(subject, '、'.join(list(set(desc))[:self.num_limit]))

        elif question_type == 'main_diagnosis_names_contents_of_doctors_orders':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            final_answer = '{0}的医嘱内容(推荐治疗方案) : {1}'.format(subject, '、'.join(list(set(desc))[:self.num_limit]))

        return final_answer


if __name__ == '__main__':
    searcher = AnswerSearcher()
    a = [{'question_type': 'main_diagnosis_names_department_names', 'sql': ["MATCH (m:科室名称)-[r:疾病名称]->(n:主要诊断名称) where n.name = '急性鼻炎' return m.name, r.name, n.name"]}]
    # a = [{'question_type': 'department_names_doctor_names', 'sql': ["MATCH (m:科室名称)-[r:配置医生]->(n:医生名称) where m.name = '急诊外科' return m.name, r.name, n.name"]}]
    searcher.search_main(a)
