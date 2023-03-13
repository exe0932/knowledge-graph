# -*- coding: utf-8 -*-

# @Author : Eason_Chen

# @Time : 2023/3/13 上午 10:37
import os
import json
from py2neo import Graph,Node

class MedicalGraph:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        self.data_path = os.path.join(cur_dir, 'data/medical5.json')
        self.g = Graph("http://localhost:7474", auth=("neo4j", "ji32k7au4a83"))
        self.g.delete_all()  # 先清空数据库，按需执行

        '''读取文件data_path'''

    def read_nodes(self):
        # 共７类节点
        clinic_numbers = []  # 门诊号
        visit_numbers = []  # 就诊号
        department_names = []  # 科室名称
        patient_names = []  # 患者名称
        id_numbers = []  # 身份证号
        patient_genders = []  # 患者性别
        ages = []  # 年龄

        visit_numbers_infos = []  # 就诊号码为中心节点

        doctor_ids = []  # 医生工号
        medical_payment_methods = []  # 医疗付款方式
        main_diagnostic_codes = []  # 主要诊断编码
        main_diagnosis_descriptions = []  # 主要诊断描述
        main_diagnosis_names = []  # 主要诊断名称
        doctor_names = []  # 医生名称
        other_diagnoses_1s = []  # 其他诊断1
        other_diagnosis_1_codes = []  # 其他诊断1编码
        other_diagnoses_2s = []  # 其他诊断2
        other_diagnosis_2_codes = []  # 其他诊断2编码
        other_diagnoses_3s = []  # 其他诊断3
        other_diagnosis_3_codes = []  # 其他诊断3编码
        epidemiological_history_of_convid_19s = []  # 是否有新冠肺炎流行病学史
        physical_exam_descriptions = []  # 体格检查描述
        contents_of_doctors_orders = []  # 医嘱项目内容
        describes = []  # 描述
        main_complaints = []  # 主诉
        history_of_present_illnesses = []  # 现病史
        past_historys = []  # 既往史


        # 构建节点实体关系
        rels_clinic = []                                            # 门诊号(大节点名称)-门诊号(数字) 关系
        rels_clinic_visit = []                                      # 就诊号(大节点名称)-就诊号(数字) 关系
        rels_department = []                                        # 科室(大节点名称)－科室(细部科室名称) 关系
        rels_patient_name = []                                      # 患者名称(大节点名称)－患者名称(患者名称名称) 关系
        rels_id_number = []                                         # 身份证号(大节点名称)－身份证号(个人身份证号码) 关系
        rels_patient_gender = []                                    # 患者性别(大节点名称)－患者性别(细分性别，可能男女中性?) 关系
        rels_age = []                                               # 年龄(大节点名称)－年龄(数字) 关系
        rels_doctor_id = []                                         # 医生功号(大节点名称)－医生功号(数字) 关系
        rels_medical_payment_method = []                            # 医疗付款方式(大节点名称)－医疗付款方式(自费或社保)检查关系
        rels_main_diagnostic_code = []                              # 主要诊断编码(大节点名称)－主要诊断编码(数字) 关系
        rels_main_diagnosis_description = []                        # 主要诊断描述(大节点名称)－主要诊断描述(内容) 关系
        rels_main_diagnosis_name = []                               # 主要诊断名称(大节点名称)－主要诊断名称(内容) 关系
        rels_doctor_name = []                                       #　医生名称(大节点名称)－医生名称(名字) 关系
        rels_other_diagnoses_1 = []                                 #　其他诊断1(大节点名称)－其他诊断1(内容) 关系
        rels_other_diagnosis_1_code = []                            #　其他诊断1编码(大节点名称)－其他诊断1编码(数字) 关系
        rels_other_diagnoses_2 = []                                 #　其他诊断2(大节点名称)－其他诊断2(内容) 关系
        rels_other_diagnosis_2_code = []                            #　其他诊断2编码(大节点名称)－其他诊断2编码(数字) 关系
        rels_other_diagnoses_3 = []                                 #　其他诊断3(大节点名称)－其他诊断3(内容) 关系
        rels_other_diagnosis_3_code = []                            #　其他诊断3编码(大节点名称)－其他诊断3编码(数字) 关系
        rels_epidemiological_history_of_convid_19 = []              #　其他诊断3编码(大节点名称)－其他诊断3编码(数字) 关系
        rels_ephysical_exam_description = []                        #　体格检查描述(大节点名称)－体格检查描述(内容) 关系
        rels_contents_of_doctors_order = []                         #　医嘱项目内容(大节点名称)－医嘱项目内容(内容) 关系
        rels_describe = []                                          #　描述(大节点名称)－描述(内容) 关系
        rels_main_complaint = []                                    #　主诉(大节点名称)－主诉(内容) 关系
        rels_history_of_present_illness = []                        #　现病史(大节点名称)－现病史(内容) 关系
        rels_past_history = []                                      #　既往史(大节点名称)－既往史(内容) 关系

        # 细部节点关系
        rels_patient_name_clinic = []                               # 患者名称(患者名称名称)－门诊号(大节点名称) 关系
        rels_clinic_visit_number = []                               # 门诊号(数字)－就诊号(大节点名称) 关系
        rels_visit_department = []                                  # 就诊号(数字)－科室(大节点名称) 关系

        count = 0
        for data in open(self.data_path, 'r', encoding='utf-8'):  # 加入 encoding='utf-8'才不会报错
            disease_dict = {}
            count += 1
            # print(count)
            data_json = json.loads(data)
            visit_number = data_json['就诊号']
            disease_dict['就诊号'] = visit_number
            disease_dict['门诊号'] = ''
            disease_dict['科室名称'] = ''
            disease_dict['患者名称'] = ''
            disease_dict['身份证号'] = ''
            disease_dict['患者性别'] = ''
            disease_dict['年龄'] = ''
            disease_dict['医生工号'] = ''
            disease_dict['医疗付款方式'] = ''
            disease_dict['主要诊断编码'] = ''
            disease_dict['主要诊断描述'] = ''
            disease_dict['主要诊断名称'] = ''
            disease_dict['医生名称'] = ''
            disease_dict['其他诊断1'] = ''
            disease_dict['其他诊断1编码'] = ''
            disease_dict['其他诊断2'] = ''
            disease_dict['其他诊断2编码'] = ''
            disease_dict['其他诊断3'] = ''
            disease_dict['是否有新冠肺炎流行病学史'] = ''
            disease_dict['体格检查描述'] = ''
            disease_dict['医嘱项目内容'] = ''
            disease_dict['描述'] = ''
            disease_dict['主诉'] = ''
            disease_dict['现病史'] = ''
            disease_dict['既往史'] = ''


if __name__ == '__main__':
    handler = MedicalGraph()
    #handler.export_data()
    handler.create_graphnodes()
    handler.create_graphrels()