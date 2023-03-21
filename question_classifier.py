# -*- coding: utf-8 -*-
import io
# @Author : Eason_Chen

# @Time : 2023/3/20 下午 02:19

import os
import ahocorasick

class QuestionClassifier:
    def __init__(self):
        cur_dir = '\\'.join(os.path.abspath(__file__).split('\\')[:-1])

        # 特征词路径
        self.department_names_path = os.path.join(cur_dir, 'dict/department_names.txt')
        self.doctor_ids_path = os.path.join(cur_dir, 'dict/doctor_ids.txt')
        self.doctor_names_path = os.path.join(cur_dir, 'dict/doctor_names.txt')
        self.main_diagnosis_names_path = os.path.join(cur_dir, 'dict/main_diagnosis_names.txt')
        self.main_diagnostic_codes_path = os.path.join(cur_dir, 'dict/main_diagnostic_codes.txt')
        self.medical_payment_methods_path = os.path.join(cur_dir, 'dict/medical_payment_methods.txt')
        self.patient_names_path = os.path.join(cur_dir, 'dict/patient_names.txt')

        # 加载特征词
        self.department_names_wds = [i.strip() for i in open(self.department_names_path, encoding="utf-8") if i.strip()]    # encoding="utf-8"
        self.doctor_ids_wds = [i.strip() for i in open(self.doctor_ids_path, encoding="utf-8") if i.strip()]    # encoding="utf-8"
        self.doctor_names_wds = [i.strip() for i in open(self.doctor_names_path, encoding="utf-8") if i.strip()]    # encoding="utf-8"
        self.main_diagnosis_names_wds = [i.strip() for i in open(self.main_diagnosis_names_path, encoding="utf-8") if i.strip()]    # encoding="utf-8"
        self.main_diagnostic_codes_wds = [i.strip() for i in open(self.main_diagnostic_codes_path, encoding="utf-8") if i.strip()]    # encoding="utf-8"
        self.medical_payment_methods_wds = [i.strip() for i in open(self.medical_payment_methods_path, encoding="utf-8") if i.strip()]    # encoding="utf-8"
        self.patient_names_wds = [i.strip() for i in open(self.patient_names_path, encoding="utf-8") if i.strip()]    # encoding="utf-8"

        self.region_words = set(self.department_names_wds + self.doctor_ids_wds + self.doctor_names_wds + self.main_diagnosis_names_wds + self.main_diagnostic_codes_wds + self.medical_payment_methods_wds + self.patient_names_wds)
        # 构造领域actree
        self.region_tree = self.build_actree(list(self.region_words))

        # 构建词典
        self.wdtype_dict = self.build_wdtype_dict()

        # 问句疑问词
        self.belong_qwds = ['要看什么科', '属于', '什么科', '科室', '属于什么科室', '属于什么科']

        print('model init finished ......')

        return

    '''分类主函数'''
    def classify(self, question):
        data = dict()
        medical_dict = self.check_medical(question)
        if not medical_dict:
            return {}
        data['args'] = medical_dict
        # 收集问句当中所涉及到的实体类型
        types = []
        for type_ in medical_dict.values():
            print(type_)
            types += type_
        question_type = 'others'

        question_types = []

        # 已知主要诊断名称，推荐科室
        if self.check_words(self.belong_qwds, question) and ('main_diagnosis_names' in types):
            question_type = 'main_diagnosis_names_department_names'
            question_types.append(question_type)

        # 将多疙分类结果进行合并处理，组装成一个字典
        data['question_types'] = question_types

        return data

    '''构造词对应的类型'''
    def build_wdtype_dict(self):
        wd_dict = dict()
        for wd in self.region_words:
            wd_dict[wd] = []
            if wd in self.department_names_wds:
                wd_dict[wd].append('department_names')
            if wd in self.doctor_ids_wds:
                wd_dict[wd].append('doctor_ids')
            if wd in self.doctor_names_wds:
                wd_dict[wd].append('doctor_names')
            if wd in self.main_diagnosis_names_wds:
                wd_dict[wd].append('main_diagnosis_names')
            if wd in self.main_diagnostic_codes_wds:
                wd_dict[wd].append('main_diagnostic_codes')
            if wd in self.medical_payment_methods_wds:
                wd_dict[wd].append('medical_payment_methods')
            if wd in self.patient_names_wds:
                wd_dict[wd].append('patient_names')
        return wd_dict

    '''构造actree，加速过滤'''
    def build_actree(self, wordlist):
        actree = ahocorasick.Automaton()
        for index, word in enumerate(wordlist):
            actree.add_word(word, (index, word))
        actree.make_automaton()
        return actree

    '''问句过滤'''
    def check_medical(self, question):
        region_wds = list()
        for i in self.region_tree.iter(question):
            wd = i[1][1]
            region_wds.append(wd)
        stop_wds = []
        for wd1 in region_wds:
            for wd2 in region_wds:
                if wd1 in wd2 and wd1 != wd2:
                    stop_wds.append(wd1)
        final_wds = [i for i in region_wds if i not in stop_wds]
        final_dict = {i: self.wdtype_dict.get(i) for i in final_wds}

        return final_dict

    '''基于特征词进行分类'''
    def check_words(self, wds, sent):
        for wd in wds:
            print(wd)
            if wd in sent:
                return True
        return False


if __name__ == '__main__':
    handler = QuestionClassifier()
    # handler.check_medical('急性鼻炎')
    # handler.classify('急性鼻炎') #急性鼻炎要看什么科
    while 1:
        question = input('input an question:')
        data = handler.classify(question)
        print(data)