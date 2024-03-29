# -*- coding: utf-8 -*-

# @Author : Eason_Chen

# @Time : 2023/3/21 下午 03:21

class QuestionPaser:

    '''构建实体节点'''
    def build_entitydict(self, args):
        entity_dict = {}
        for arg, types in args.items():
            for type in types:
                if type not in entity_dict:
                    entity_dict[type] = [arg]
                else:
                    entity_dict[type].append(arg)

        return entity_dict

    '''解析主函数'''
    def parser_main(self, res_classify):
        args = res_classify['args']
        entity_dict = self.build_entitydict(args)
        # print("entity_dict", entity_dict)
        question_types = res_classify['question_types']
        sqls = []
        for question_type in question_types:
            sql_ = {}
            sql_['question_type'] = question_type
            sql = []
            if question_type == 'main_diagnosis_names_department_names':
                sql = self.sql_transfer(question_type, entity_dict.get('main_diagnosis_names'))
                # print("sql", sql)
            elif question_type == 'main_complaints_diagnosis_names':
                sql = self.sql_transfer(question_type, entity_dict.get('main_complaints'))

            elif question_type == 'department_names_doctor_names':
                sql = self.sql_transfer(question_type, entity_dict.get('department_names'))

            elif question_type == 'main_diagnosis_names_contents_of_doctors_orders':
                sql = self.sql_transfer(question_type, entity_dict.get('main_diagnosis_names'))

            if sql:
                sql_['sql'] = sql

                sqls.append(sql_)

        return sqls

    '''针对不同的问题，分开进行处理'''
    def sql_transfer(self, question_type, entities):
        if not entities:
            return []

        # 查询语句
        sql = []
        # 已知主要诊断名称，查询推荐科室
        if question_type == 'main_diagnosis_names_department_names':
            sql = ["MATCH (m:科室名称)-[r:疾病名称]->(n:主要诊断名称) where n.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        # 根据主诉，推断疾病名称(主要诊断名称)
        elif question_type == 'main_complaints_diagnosis_names':
            sql = ["MATCH (m:主诉)-[r:所属疾病名]->(n:主要诊断名称) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        # 根据科室名称，寻找有哪些医生
        elif question_type == 'department_names_doctor_names':
            sql = ["MATCH (m:科室名称)-[r:配置医生]->(n:医生名称) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        # 根据疾病名称(主要诊断名称)，推荐吃什么药(医嘱)
        elif question_type == 'main_diagnosis_names_contents_of_doctors_orders':
            sql = ["MATCH (m:主要诊断名称)-[r:医嘱项目内容]->(n:医嘱项目内容) where m.name = '{0}' return m.name, r.name, n.name".format(i) for i in entities]

        return sql







if __name__ == '__main__':
    handler = QuestionPaser()
    a = handler.parser_main({'args': {'急性鼻炎': ['main_diagnosis_names']}, 'question_types': ['main_diagnosis_names_department_names']})
    # a = handler.parser_main({'args': {'急诊外科': ['department_names']}, 'question_types': ['department_names_doctor_names']})
    print(a)