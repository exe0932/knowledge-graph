# -*- coding: utf-8 -*-

# @Author : Eason_Chen

# @Time : 2023/2/28 下午 02:22
import os
import json
from py2neo import Graph,Node

class MedicalGraph:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        self.data_path = os.path.join(cur_dir, 'data/medical3.json')
        self.data_path_1 = os.path.join(cur_dir, 'data/medical4.json')
        # self.g = Graph("http://localhost:7474", username="neo4j", password="ji32k7au4a83") # 版本問題ValueError: The following settings are not supported: {'username': 'neo4j'}
        self.g = Graph("http://localhost:7474", auth=("neo4j", "ji32k7au4a83"))
        self.g.delete_all()  # 先清空数据库，按需执行

    def formula_1(self, datas, dicts):
        lis1 = list()
        for data in datas:
            lis1.append(data)
        return lis1

    '''读取文件data_path_1'''
    def read_nodes(self):
        medical_records = []       # 病历表
        disease_infos_1 = []       # 大实体名称节点
        rels_detail_items = []     # 连接细部项目
        for data_1 in open(self.data_path_1, 'r', encoding='utf-8'):  # 加入 encoding='utf-8'才不会报错
            disease_dict_1 = {}
            data_json = json.loads(data_1)
            medical_record = data_json['name']
            medical_records.append(medical_record)
            disease_dict_1['name'] = medical_record                   # 添加病历表到 dict 保留尚未用到
            for medical_record_ in medical_records:
                rels_detail_items.append(['病历表', medical_record_])  # 节点上的名字与另一个节点上的名字连接
            disease_infos_1.append(disease_dict_1)
        return set(medical_records), disease_infos_1, rels_detail_items

    '''读取文件data_path'''
    def read_nodes_1(self):
        # 共７类节点
        clinic_numbers = []      # 门诊号
        visit_numbers = []       # 就诊号
        department_names = []    # 科室名称
        patient_names = []       # 患者名称
        id_numbers = []          # 身份证号
        patient_genders = []     # 患者性别
        ages = []                # 年龄

        disease_infos = []      # 疾病信息

        doctor_ids = []                              # 医生工号
        medical_payment_methods = []                 # 医疗付款方式
        main_diagnostic_codes = []                   # 主要诊断编码
        main_diagnosis_descriptions = []             # 主要诊断描述
        main_diagnosis_names = []                    # 主要诊断名称
        doctor_names = []                            # 医生名称
        other_diagnoses_1s = []                      # 其他诊断1
        other_diagnosis_1_codes = []                 # 其他诊断1编码
        other_diagnoses_2s = []                      # 其他诊断2
        other_diagnosis_2_codes = []                 # 其他诊断2编码
        other_diagnoses_3s = []                      # 其他诊断3
        other_diagnosis_3_codes = []                 # 其他诊断3编码
        epidemiological_history_of_convid_19s = []   # 是否有新冠肺炎流行病学史
        physical_exam_description = []              # 体格检查描述
        contents_of_doctors_orders = []             # 医嘱项目内容
        describe = []                               # 描述
        main_complaint = []                         # 主诉
        history_of_present_illness = []             # 现病史
        past_history = []                           # 既往史


        # 构建节点实体关系
        rels_clinic = []                                            # 门诊号(大节点名称)-门诊号(数字) 关系
        rels_clinic_visit = []                                      # 就诊号(大节点名称)-就诊号(数字) 关系
        rels_department = []                                        #　科室(大节点名称)－科室(细部科室名称) 关系
        rels_patient_name = []                                      # 疾病(大节点名称)－疾病(细部疾病名称) 关系
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


        count = 0
        for data in open(self.data_path, 'r', encoding='utf-8'):    # 加入 encoding='utf-8'才不会报错
            disease_dict = {}
            count += 1
            # print(count)
            data_json = json.loads(data)
            print(data_json)
            disease_dict['门诊号'] = ''
            disease_dict['就诊号'] = ''
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

            if '门诊号' in data_json:
                clinic_number = data_json['门诊号']
                clinic_numbers.append(clinic_number)           # 添加门诊号
                disease_dict['门诊号'] = clinic_number          # 添加门诊号到 dict 保留尚未用到
                for clinic_number in clinic_numbers:
                    rels_clinic.append(['门诊号', clinic_number])

            if '就诊号' in data_json:
                visit_number = data_json['就诊号']
                visit_numbers.append(visit_number)
                disease_dict['就诊号'] = visit_number
                for visit_number_ in visit_numbers:
                    rels_clinic_visit.append(['就诊号', visit_number_])

            if '科室名称' in data_json:
                department_name = data_json['科室名称']
                department_names.append(department_name)
                disease_dict['科室名称'] = department_name
                for department_name_ in department_names:
                    rels_department.append(['科室名称', department_name_])

            if '患者名称' in data_json:
                patient_name = data_json['患者名称']
                patient_names.append(patient_name)
                disease_dict['患者名称'] = patient_name
                for patient_name_ in patient_names:
                    rels_patient_name.append(['患者名称', patient_name_])

            if '身份证号' in data_json:
                id_number = data_json['身份证号']
                id_numbers.append(id_number)
                disease_dict['身份证号'] = id_number
                for id_number_ in id_numbers:
                    rels_id_number.append(['身份证号', id_number_])

            if '患者性别' in data_json:
                patient_gender = data_json['患者性别']
                patient_genders.append(patient_gender)
                disease_dict['患者性别'] = patient_gender
                for patient_gender_ in patient_genders:
                    rels_patient_gender.append(['患者性别', patient_gender_])

            if '年龄' in data_json:
                age = data_json['年龄']
                ages.append(age)
                disease_dict['年龄'] = age
                for age_ in ages:
                    rels_age.append(['年龄', age_])

            if '医生工号' in data_json:
                doctor_id = data_json['医生工号']
                doctor_ids.append(doctor_id)
                disease_dict['医生工号'] = doctor_id
                for doctor_id_ in doctor_ids:
                    rels_doctor_id.append(['医生工号', doctor_id_])

            if '医疗付款方式' in data_json:
                medical_payment_method = data_json['医疗付款方式']
                medical_payment_methods.append(medical_payment_method)
                disease_dict['医疗付款方式'] = medical_payment_method
                for medical_payment_method_ in medical_payment_methods:
                    rels_medical_payment_method.append(['医疗付款方式', medical_payment_method_])

            if '主要诊断编码' in data_json:
                main_diagnostic_code = data_json['主要诊断编码']
                main_diagnostic_codes.append(main_diagnostic_code)
                disease_dict['主要诊断编码'] = main_diagnostic_code
                for main_diagnostic_code_ in main_diagnostic_codes:
                    rels_main_diagnostic_code.append(['主要诊断编码', main_diagnostic_code_])

            if '主要诊断描述' in data_json:
                main_diagnosis_description = data_json['主要诊断描述']
                main_diagnosis_descriptions.append(main_diagnosis_description)
                disease_dict['主要诊断描述'] = main_diagnosis_description
                for main_diagnosis_description_ in main_diagnosis_descriptions:
                    rels_main_diagnosis_description.append(['主要诊断描述', main_diagnosis_description_])

            if '主要诊断名称' in data_json:
                main_diagnosis_name = data_json['主要诊断名称']
                main_diagnosis_names.append(main_diagnosis_name)
                disease_dict['主要诊断名称'] = main_diagnosis_name
                for main_diagnosis_name_ in main_diagnosis_names:
                    rels_main_diagnosis_name.append(['主要诊断名称', main_diagnosis_name_])

            if '医生名称' in data_json:
                doctor_name = data_json['医生名称']
                doctor_names.append(doctor_name)
                disease_dict['医生名称'] = doctor_name
                for doctor_name_ in doctor_names:
                    rels_doctor_name.append(['医生名称', doctor_name_])

            if '其他诊断1' in data_json:
                other_diagnoses_1 = data_json['其他诊断1']
                other_diagnoses_1s += other_diagnoses_1
                # other_diagnoses_1s.append(other_diagnoses_1)
                disease_dict['其他诊断1'] = other_diagnoses_1
                for other_diagnoses_1_ in other_diagnoses_1s:
                    rels_other_diagnoses_1.append(['其他诊断1', other_diagnoses_1_])

            if '其他诊断1编码' in data_json:
                other_diagnosis_1_code = data_json['其他诊断1编码']
                other_diagnosis_1_codes += other_diagnosis_1_code
                # other_diagnosis_1_codes.append(other_diagnosis_1_code)
                disease_dict['其他诊断1编码'] = other_diagnosis_1_code
                for other_diagnosis_1_code_ in other_diagnosis_1_codes:
                    rels_other_diagnosis_1_code.append(['其他诊断1编码', other_diagnosis_1_code_])

            if '其他诊断2' in data_json:
                other_diagnoses_2 = data_json['其他诊断2']
                other_diagnoses_2s += other_diagnoses_2
                # other_diagnoses_2s.append(other_diagnoses_2)
                disease_dict['其他诊断2'] = other_diagnoses_2
                for other_diagnoses_2_ in other_diagnoses_2s:
                    rels_other_diagnoses_2.append(['其他诊断2', other_diagnoses_2_])

            if '其他诊断2编码' in data_json:
                other_diagnosis_2_code = data_json['其他诊断2编码']
                other_diagnosis_2_codes += other_diagnosis_2_code
                # other_diagnosis_2_codes.append(other_diagnosis_2_code)
                disease_dict['其他诊断2编码'] = other_diagnosis_2_code
                for other_diagnosis_2_code_ in other_diagnosis_2_codes:
                    rels_other_diagnosis_2_code.append(['其他诊断2编码', other_diagnosis_2_code_])

            if '其他诊断3' in data_json:
                other_diagnoses_3 = data_json['其他诊断3']
                other_diagnoses_3s += other_diagnoses_3
                # other_diagnoses_3s.append(other_diagnoses_3)
                disease_dict['其他诊断3'] = other_diagnoses_3
                for other_diagnoses_3_ in other_diagnoses_3s:
                    rels_other_diagnoses_3.append(['其他诊断3', other_diagnoses_3_])

            if '其他诊断3编码' in data_json:
                other_diagnosis_3_code = data_json['其他诊断3编码']
                other_diagnosis_3_codes += other_diagnosis_3_code
                # other_diagnosis_3_codes.append(other_diagnosis_3_code)
                disease_dict['其他诊断3编码'] = other_diagnosis_3_code
                for other_diagnosis_3_code_ in other_diagnosis_3_codes:
                    rels_other_diagnosis_3_code.append(['其他诊断3编码', other_diagnosis_3_code_])
            ##
            if '是否有新冠肺炎流行病学史' in data_json:
                epidemiological_history_of_convid_19 = data_json['是否有新冠肺炎流行病学史']
                epidemiological_history_of_convid_19s += epidemiological_history_of_convid_19
                # epidemiological_history_of_convid_19s.append(epidemiological_history_of_convid_19)
                disease_dict['是否有新冠肺炎流行病学史'] = epidemiological_history_of_convid_19
                for epidemiological_history_of_convid_19_ in epidemiological_history_of_convid_19s:
                    rels_epidemiological_history_of_convid_19.append(['是否有新冠肺炎流行病学史', epidemiological_history_of_convid_19_])

            disease_infos.append(disease_dict)

            #
            # if 'cure_department' in data_json:
            #     cure_department = data_json['cure_department']
            #     if len(cure_department) == 1:
            #         rels_category.append([disease, cure_department[0]])
            #     if len(cure_department) == 2:
            #         big = cure_department[0]
            #         small = cure_department[1]
            #         rels_department.append([small, big])
            #         rels_category.append([disease, small])
            #
            #     disease_dict['cure_department'] = cure_department
            #     departments += cure_department
            #
            # if 'common_drug' in data_json:
            #     common_drug = data_json['common_drug']
            #     for drug in common_drug:
            #         rels_commonddrug.append([disease, drug])
            #     drugs += common_drug
            #
            # if 'recommand_drug' in data_json:
            #     recommand_drug = data_json['recommand_drug']
            #     drugs += recommand_drug
            #     for drug in recommand_drug:
            #         rels_recommanddrug.append([disease, drug])
            #
            # if 'not_eat' in data_json:
            #     not_eat = data_json['not_eat']
            #     for _not in not_eat:
            #         rels_noteat.append([disease, _not])
            #
            #     foods += not_eat
            #     do_eat = data_json['do_eat']
            #     for _do in do_eat:
            #         rels_doeat.append([disease, _do])
            #
            #     foods += do_eat
            #     recommand_eat = data_json['recommand_eat']
            #
            #     for _recommand in recommand_eat:
            #         rels_recommandeat.append([disease, _recommand])
            #     foods += recommand_eat
            #
            # if 'check' in data_json:
            #     check = data_json['check']
            #     for _check in check:
            #         rels_check.append([disease, _check])
            #     checks += check
            # if 'drug_detail' in data_json:
            #     drug_detail = data_json['drug_detail']
            #     producer = [i.split('(')[0] for i in drug_detail]
            #     rels_drug_producer += [[i.split('(')[0], i.split('(')[-1].replace(')', '')] for i in drug_detail]
            #     producers += producer
            # disease_infos.append(disease_dict)
        return set(clinic_numbers), set(visit_numbers), set(department_names), set(patient_names), set(id_numbers), set(patient_genders), set(ages), set(doctor_ids), set(medical_payment_methods), set(main_diagnostic_codes), set(main_diagnosis_descriptions), set(main_diagnosis_names), \
               set(doctor_names), set(other_diagnoses_1s), set(other_diagnosis_1_codes), set(other_diagnoses_2s), set(other_diagnosis_2_codes), set(other_diagnoses_3s), set(other_diagnosis_3_codes), set(epidemiological_history_of_convid_19s), disease_infos, rels_clinic, rels_clinic_visit, \
               rels_department, rels_patient_name, rels_id_number, rels_patient_gender, rels_age, rels_doctor_id, rels_medical_payment_method, rels_main_diagnostic_code, rels_main_diagnosis_description, rels_main_diagnosis_name, rels_doctor_name, rels_other_diagnoses_1, rels_other_diagnosis_1_code, \
               rels_other_diagnoses_2, rels_other_diagnosis_2_code, rels_other_diagnoses_3, rels_other_diagnosis_3_code, rels_epidemiological_history_of_convid_19

    '''建立节点'''
    def create_node(self, label, nodes):
        count = 0
        for node_name in nodes:
            node = Node(label, name=node_name)
            self.g.create(node)
            count += 1
            print(count, len(nodes))
        return

    '''创建知识图谱中心疾病的节点'''
    def create_diseases_nodes(self, disease_infos):
        count = 0
        for disease_dict in disease_infos:
            node = Node("Target", name=disease_dict['name'])
            # node = Node("Target", name= disease_dict['name'], 门诊号=disease_dict['门诊号'], 就诊号=disease_dict['就诊号'], 科室名称=disease_dict['科室名称'], 患者名称=disease_dict['患者名称'], 身份证号=disease_dict['身份证号'],
            #             患者性别=disease_dict['患者性别'], 年龄=disease_dict['年龄'], 医生工号=disease_dict['医生工号'], 医疗付款方式=disease_dict['医疗付款方式'], 主要诊断编码=disease_dict['主要诊断编码'],
            #             主要诊断描述=disease_dict['主要诊断描述'], 主要诊断名称=disease_dict['主要诊断名称'], 医生名称=disease_dict['医生名称'], 其他诊断1=disease_dict['其他诊断1'], 其他诊断1编码=disease_dict['其他诊断1编码'],
            #             其他诊断2=disease_dict['其他诊断2'], 其他诊断2编码=disease_dict['其他诊断2编码'], 其他诊断3=disease_dict['其他诊断3'], 是否有新冠肺炎流行病学史=disease_dict['是否有新冠肺炎流行病学史'],
            #             体格检查描述=disease_dict['体格检查描述'], 医嘱项目内容=disease_dict['医嘱项目内容'], 描述=disease_dict['描述'], 主诉=disease_dict['主诉'], 现病史=disease_dict['现病史'],
            #             既往史=disease_dict['既往史'])
            self.g.create(node)
            count += 1
            print(count)
        return

    '''创建知识图谱实体节点类型schema'''
    def create_graphnodes(self):
        Medical_Records, disease_infos_1, rels_detail_items = self.read_nodes()
        Clinic_numbers, Visit_numbers, Department_names, Patient_names, Id_numbers, Patient_genders, Ages, Doctor_ids, Medical_payment_methods, Main_diagnostic_codes, Main_diagnosis_descriptions, Main_diagnosis_names, Doctor_names, Other_diagnoses_1s, Other_diagnosis_1_codes, Other_diagnoses_2s, \
        Other_diagnosis_2_codes, Other_diagnoses_3s, Other_diagnosis_3_codes, Epidemiological_history_of_convid_19s, disease_infos, rels_clinic, rels_clinic_visit, rels_department, rels_patient_names, \
        rels_id_number, rels_patient_gender, rels_age, rels_doctor_id, rels_medical_payment_method, rels_main_diagnostic_code, rels_main_diagnosis_description, rels_main_diagnosis_name, rels_doctor_name, rels_other_diagnoses_1, rels_other_diagnosis_1_code, rels_other_diagnoses_2, \
        rels_other_diagnosis_2_code, rels_other_diagnoses_3, rels_other_diagnosis_3_code, rels_epidemiological_history_of_convid_19 = self.read_nodes_1()
        self.create_node("总项目", ['病历表'])
        self.create_node("细分项目", Medical_Records)
        self.create_node('门诊号', Clinic_numbers)
        self.create_node('就诊号', Visit_numbers)
        self.create_node('科室名称', Department_names)
        self.create_node('患者名称', Patient_names)
        self.create_node('身份证号', Id_numbers)
        self.create_node('患者性别', Patient_genders)
        self.create_node('年龄', Ages)
        self.create_node('医生工号', Doctor_ids)
        self.create_node('医疗付款方式', Medical_payment_methods)
        self.create_node('主要诊断编码', Main_diagnostic_codes)
        self.create_node('主要诊断描述', Main_diagnosis_descriptions)
        self.create_node('主要诊断名称', Main_diagnosis_names)
        self.create_node('医生名称', Doctor_names)
        self.create_node('其他诊断1', Other_diagnoses_1s)
        self.create_node('其他诊断1编码', Other_diagnosis_1_codes)
        self.create_node('其他诊断2', Other_diagnoses_2s)
        self.create_node('其他诊断2编码', Other_diagnosis_2_codes)
        self.create_node('其他诊断3', Other_diagnoses_3s)
        self.create_node('其他诊断3编码', Other_diagnosis_3_codes)
        self.create_node('是否有新冠肺炎流行病学史', Epidemiological_history_of_convid_19s)
        return


    '''创建实体关系边'''
    def create_graphrels(self):
        Medical_Records, disease_infos_1, rels_detail_items = self.read_nodes()
        Clinic_numbers, Visit_numbers, Department_names, Patient_names, Id_numbers, Patient_genders, Ages, Doctor_ids, Medical_payment_methods, Main_diagnostic_codes, Main_diagnosis_descriptions, Main_diagnosis_names, Doctor_names, Other_diagnoses_1s, Other_diagnosis_1_codes, Other_diagnoses_2s, \
        Other_diagnosis_2_codes, Other_diagnoses_3s, Other_diagnosis_3_codes, Epidemiological_history_of_convid_19s, disease_infos, rels_clinic, rels_clinic_visit, rels_department, rels_patient_names, \
        rels_id_number, rels_patient_gender, rels_age, rels_doctor_id, rels_medical_payment_method, rels_main_diagnostic_code, rels_main_diagnosis_description, rels_main_diagnosis_name, rels_doctor_name, rels_other_diagnoses_1, rels_other_diagnosis_1_code, rels_other_diagnoses_2, \
        rels_other_diagnosis_2_code, rels_other_diagnoses_3, rels_other_diagnosis_3_code, rels_epidemiological_history_of_convid_19 = self.read_nodes_1()
        self.create_relationship('总项目', '细分项目', rels_detail_items, '细分项', '细分项目')
        self.create_relationship('细分项目', '门诊号', rels_clinic, '门诊号码唯一ID', '门诊号码')
        self.create_relationship('细分项目', '就诊号', rels_clinic_visit, '每次看病的就诊号', '就诊记录')
        self.create_relationship('细分项目', '科室名称', rels_department, '科室名称', '科室名称')
        self.create_relationship('细分项目', '患者名称', rels_patient_names, '患者名称', '患者名称')
        self.create_relationship('细分项目', '身份证号', rels_id_number, '身份证号', '身份证号')
        self.create_relationship('细分项目', '患者性别', rels_patient_gender, '患者性别', '患者性别')
        self.create_relationship('细分项目', '年龄', rels_age, '年龄', '年龄')
        self.create_relationship('细分项目', '医生工号', rels_doctor_id, '医生工号', '医生工号')
        self.create_relationship('细分项目', '医疗付款方式', rels_medical_payment_method, '医疗付款方式', '医疗付款方式')
        self.create_relationship('细分项目', '主要诊断编码', rels_main_diagnostic_code, '主要诊断编码', '主要诊断编码')
        self.create_relationship('细分项目', '主要诊断描述', rels_main_diagnosis_description, '主要诊断描述', '主要诊断描述')
        self.create_relationship('细分项目', '主要诊断名称', rels_main_diagnosis_name, '主要诊断名称', '主要诊断名称')
        self.create_relationship('细分项目', '医生名称', rels_doctor_name, '医生名', '医生名称')
        self.create_relationship('细分项目', '其他诊断1', rels_other_diagnoses_1, '其他诊断1', '其他诊断1')
        self.create_relationship('细分项目', '其他诊断1编码', rels_other_diagnosis_1_code, '其他诊断1编码', '其他诊断1编码')
        self.create_relationship('细分项目', '其他诊断2', rels_other_diagnoses_2, '其他诊断2', '其他诊断2')
        self.create_relationship('细分项目', '其他诊断2编码', rels_other_diagnosis_2_code, '其他诊断2编码', '其他诊断2编码')
        self.create_relationship('细分项目', '其他诊断3', rels_other_diagnoses_3, '其他诊断3', '其他诊断3')
        self.create_relationship('细分项目', '其他诊断3编码', rels_other_diagnosis_3_code, '其他诊断3编码', '其他诊断3编码')
        self.create_relationship('细分项目', '是否有新冠肺炎流行病学史', rels_epidemiological_history_of_convid_19, '是否有新冠肺炎流行病学史', '是否有新冠肺炎流行病学史')

    '''创建实体关联边'''
    def create_relationship(self, start_node, end_node, edges, rel_type, rel_name):
        count = 0
        # 去重处理
        set_edges = []
        for edge in edges:
            set_edges.append('###'.join(edge))
        all = len(set(set_edges))
        for edge in set(set_edges):
            edge = edge.split('###')
            p = edge[0]
            q = edge[1]
            query = "match(p:%s),(q:%s) where p.name='%s'and q.name='%s' create (p)-[rel:%s{name:'%s'}]->(q)" % (
                start_node, end_node, p, q, rel_type, rel_name)
            try:
                self.g.run(query)
                count += 1
                print(rel_type, count, all)
            except Exception as e:
                print(e)
        return

    '''导出数据'''
    def export_data(self):
        Drugs, Foods, Checks, Departments, Producers, Symptoms, Diseases, disease_infos, rels_check, rels_recommandeat, rels_noteat, rels_doeat, rels_department, rels_commonddrug, rels_drug_producer, rels_recommanddrug, rels_symptom, rels_acompany, rels_category = self.read_nodes()
        f_drug = open('drug.txt', 'w+')
        f_food = open('food.txt', 'w+')
        f_check = open('check.txt', 'w+')
        f_department = open('department.txt', 'w+')
        f_producer = open('producer.txt', 'w+')
        f_symptom = open('symptoms.txt', 'w+')
        f_disease = open('disease.txt', 'w+')

        f_drug.write('\n'.join(list(Drugs)))
        f_food.write('\n'.join(list(Foods)))
        f_check.write('\n'.join(list(Checks)))
        f_department.write('\n'.join(list(Departments)))
        f_producer.write('\n'.join(list(Producers)))
        f_symptom.write('\n'.join(list(Symptoms)))
        f_disease.write('\n'.join(list(Diseases)))

        f_drug.close()
        f_food.close()
        f_check.close()
        f_department.close()
        f_producer.close()
        f_symptom.close()
        f_disease.close()

        return



if __name__ == '__main__':
    handler = MedicalGraph()
    #handler.export_data()
    handler.create_graphnodes()
    handler.create_graphrels()
