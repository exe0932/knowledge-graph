# -*- coding: utf-8 -*-

# @Author : Eason_Chen

# @Time : 2023/3/13 上午 10:37
import os
import json
from py2neo import Graph, Node

class MedicalGraph:
    def __init__(self):
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        self.data_path = os.path.join(cur_dir, 'data/medical3.json')
        self.g = Graph("http://localhost:7474", auth=("neo4j", "ji32k7au4a83"))
        self.g.delete_all()  # 先清空数据库，按需执行

        self.project_dir = os.path.dirname(os.path.abspath(__file__))
        self.dict_save_dir = os.path.join(self.project_dir, 'dict')

    def draw_list(self, contents):
        if contents:
            for content in contents:
                return content
        return ''


    '''读取文件data_path'''
    def read_nodes(self):
        # 共9类节点
        visit_numbers = []                                          # 就诊号
        department_names = []                                       # 科室名称
        patient_names = []                                          # 患者名称

        '''
        clinic_numbers = []  # 门诊号
        id_numbers = []  # 身份证号
        patient_genders = []  # 患者性别
        ages = []  # 年龄
        '''

        visit_numbers_infos = []                                    # 就诊号码为中心节点

        doctor_ids = []                                             # 医生工号
        medical_payment_methods = []                                # 医疗付款方式
        main_diagnostic_codes = []                                  # 主要诊断编码
        main_diagnosis_names = []                                   # 主要诊断名称
        doctor_names = []                                           # 医生名称
        main_complaints = []                                        # 主诉
        contents_of_doctors_orders = []                             # 医嘱项目内容

        '''
        main_diagnosis_descriptions = []  # 主要诊断描述
        other_diagnoses_1s = []  # 其他诊断1
        other_diagnosis_1_codes = []  # 其他诊断1编码
        other_diagnoses_2s = []  # 其他诊断2
        other_diagnosis_2_codes = []  # 其他诊断2编码
        other_diagnoses_3s = []  # 其他诊断3
        other_diagnosis_3_codes = []  # 其他诊断3编码
        epidemiological_history_of_convid_19s = []  # 是否有新冠肺炎流行病学史
        physical_exam_descriptions = []  # 体格检查描述
        describes = []  # 描述
        history_of_present_illnesses = []  # 现病史
        past_historys = []  # 既往史
        '''

        # 细部节点关系
        rels_patient_name_visit_number = []                         # 患者名称(内容)-就诊号(数字) 关系；病人的就诊号
        rels_visit_number_department_name = []                      # 就诊号(数字)-科室名称(内容) 关系；就诊号对应看病的科室
        rels_department_name_main_diagnosis_name = []               # 科室名称(内容)-主要诊断名称(内容) 关系；疾病属于什么科室
        rels_main_diagnosis_name_diagnostic_codes = []              # 主要诊断名称(内容)-主要诊断编码(数字) 关系；该疾病的诊断编码
        rels_visit_department_doctor_name = []                      # 就诊号(数字)-医生名称(名字) 关系；当次就诊医生名
        rels_doctor_name_doctor_id = []                             # 医生名称(名字)-医生功号(数字) 关系；当次就诊医生工号
        rels_visit_medical_payment_method = []                      # 就诊号(数字)-医疗付款方式(自费或社保)检查 关系；当次就诊付款方式
        rels_main_complaint_diagnosis_name = []                     # 主诉(内容)-主要诊断名称(内容) 关系；病人描述的主诉推断疾病名称(主要诊断名称)
        rels_department_doctor_name = []                            # 科室名称(内容)-医生名称(名字) 关系；该科室对应哪些医生
        rels_main_diagnosis_name_contents_of_doctors_orders = []    # 主要诊断名称(内容)－医嘱项目内容(内容) 关系；医嘱内容属于推荐药物治疗方案

        '''
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
        rels_describe = []                                          #　描述(大节点名称)－描述(内容) 关系
        rels_main_complaint = []                                    #　主诉(大节点名称)－主诉(内容) 关系
        rels_history_of_present_illness = []                        #　现病史(大节点名称)－现病史(内容) 关系
        rels_past_history = []                                      #　既往史(大节点名称)－既往史(内容) 关系

        # 细部节点关系
        rels_patient_name_clinic = []                               # 患者名称(患者名称名称)－门诊号(大节点名称) 关系
        rels_clinic_visit_number = []                               # 门诊号(数字)－就诊号(大节点名称) 关系
        '''

        count = 0
        for data in open(self.data_path, 'r', encoding='utf-8'):  # 加入 encoding='utf-8'才不会报错
            visit_numbers_dict = {}
            count += 1
            print(count)
            data_json = json.loads(data)
            visit_number = data_json['就诊号']
            visit_numbers_dict['就诊号'] = visit_number
            visit_numbers.append(visit_number)
            visit_numbers_dict['科室名称'] = ''
            visit_numbers_dict['患者名称'] = ''
            visit_numbers_dict['医生工号'] = ''
            visit_numbers_dict['医疗付款方式'] = ''
            visit_numbers_dict['医生名称'] = ''
            visit_numbers_dict['主要诊断名称'] = ''
            visit_numbers_dict['主要诊断编码'] = ''
            visit_numbers_dict['主诉'] = ''

            # 尚未使用
            visit_numbers_dict['门诊号'] = ''
            visit_numbers_dict['身份证号'] = ''
            visit_numbers_dict['患者性别'] = ''
            visit_numbers_dict['年龄'] = ''
            visit_numbers_dict['主要诊断描述'] = ''
            visit_numbers_dict['其他诊断1'] = ''
            visit_numbers_dict['其他诊断1编码'] = ''
            visit_numbers_dict['其他诊断2'] = ''
            visit_numbers_dict['其他诊断2编码'] = ''
            visit_numbers_dict['其他诊断3'] = ''
            visit_numbers_dict['其他诊断3编码'] = ''
            visit_numbers_dict['是否有新冠肺炎流行病学史'] = ''
            visit_numbers_dict['体格检查描述'] = ''
            visit_numbers_dict['医嘱项目内容'] = ''
            visit_numbers_dict['描述'] = ''
            visit_numbers_dict['现病史'] = ''
            visit_numbers_dict['既往史'] = ''

            if '患者名称' in data_json:
                patient_name = data_json['患者名称']
                visit_numbers_dict['患者名称'] = patient_name
                patient_names.append(patient_name)
                rels_patient_name_visit_number.append([patient_name, visit_number])                                                 # 患者名称(内容)-就诊号(数字) 关系；病人的就诊号

            if '科室名称' in data_json:
                department_name, doctor_name = data_json['科室名称'], data_json['医生名称']
                visit_numbers_dict['科室名称'] = department_name
                department_names.append(department_name)
                rels_visit_number_department_name.append([visit_number, department_name])                                           # 就诊号(数字)-科室名称(内容) 关系；就诊号对应看病的科室
                rels_department_doctor_name.append([department_name, doctor_name])                                                  # 科室名称(内容)-医生名称(名字) 关系；该科室对应哪些医生

            if '主要诊断名称' in data_json:
                main_diagnosis_name, department_name = data_json['主要诊断名称'], data_json['科室名称']
                visit_numbers_dict['主要诊断名称'] = main_diagnosis_name
                main_diagnosis_names.append(main_diagnosis_name)
                rels_department_name_main_diagnosis_name.append([department_name, main_diagnosis_name])                             # 科室名称(内容)-主要诊断名称(内容) 关系；疾病属于什么科室

            if '主要诊断编码' in data_json:
                main_diagnostic_code, main_diagnosis_name = data_json['主要诊断编码'], data_json['主要诊断名称']
                visit_numbers_dict['主要诊断编码'] = main_diagnostic_code
                main_diagnostic_codes.append(main_diagnostic_code)
                rels_main_diagnosis_name_diagnostic_codes.append([main_diagnosis_name, main_diagnostic_code])                       # 主要诊断名称(内容)-主要诊断编码(数字) 关系；该疾病的诊断编码

            if '医生名称' in data_json:
                doctor_name = data_json['医生名称']
                visit_numbers_dict['医生名称'] = doctor_name
                doctor_names.append(doctor_name)
                rels_visit_department_doctor_name.append([visit_number, doctor_name])                                               # 就诊号(数字)-医生名称(名字) 关系；当次就诊医生名

            if '医生工号' in data_json:
                doctor_id, doctor_name = data_json['医生工号'], data_json['医生名称']
                visit_numbers_dict['医生工号'] = doctor_id
                doctor_ids.append(doctor_id)
                rels_doctor_name_doctor_id.append([doctor_name, doctor_id])                                                         # 医生名称(名字)-医生功号(数字)关系；当次就诊医生工号

            if '医疗付款方式' in data_json:
                medical_payment_method = data_json['医疗付款方式']
                visit_numbers_dict['医疗付款方式'] = medical_payment_method
                medical_payment_methods.append(medical_payment_method)
                rels_visit_medical_payment_method.append([visit_number, medical_payment_method])                                    # 就诊号(数字)-医疗付款方式(自费或社保)检查关系；当次就诊付款方式

            if '主诉' in data_json:
                main_complaint, main_diagnosis_name = data_json['主诉'], data_json['主要诊断名称']
                visit_numbers_dict['主诉'] = main_complaint
                main_complaints.append(main_complaint)
                rels_main_complaint_diagnosis_name.append([main_complaint, main_diagnosis_name])                                    # 主诉(内容)-主要诊断名称(内容) 关系；病人描述的主诉推断疾病名称(主要诊断名称)

            if '医嘱项目内容' in data_json:
                contents_of_doctors_order, main_diagnosis_name = self.draw_list(data_json['医嘱项目内容']), data_json['主要诊断名称']
                visit_numbers_dict['医嘱项目内容'] = contents_of_doctors_order
                if contents_of_doctors_order == '':
                    contents_of_doctors_orders.append('无医嘱项目内容')
                    rels_main_diagnosis_name_contents_of_doctors_orders.append([main_diagnosis_name, '无医嘱项目内容'])  # 主要诊断名称(内容)－医嘱项目内容(内容) 关系；医嘱内容属于推荐药物治疗方案
                else:
                    contents_of_doctors_orders.append(contents_of_doctors_order)
                    rels_main_diagnosis_name_contents_of_doctors_orders.append([main_diagnosis_name, contents_of_doctors_order])    # 主要诊断名称(内容)－医嘱项目内容(内容) 关系；医嘱内容属于推荐药物治疗方案


            visit_numbers_infos.append(visit_numbers_dict)
        return set(patient_names), set(department_names), set(main_diagnosis_names), set(main_diagnostic_codes), set(doctor_names), set(doctor_ids), set(medical_payment_methods), set(main_complaints), set(contents_of_doctors_orders), visit_numbers_infos, \
               rels_patient_name_visit_number, rels_visit_number_department_name, rels_department_name_main_diagnosis_name, \
               rels_main_diagnosis_name_diagnostic_codes, rels_visit_department_doctor_name, rels_doctor_name_doctor_id, rels_visit_medical_payment_method, rels_main_complaint_diagnosis_name, \
               rels_department_doctor_name, rels_main_diagnosis_name_contents_of_doctors_orders

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
    def create_visit_numbers_nodes(self, visit_numbers_infos):
        count = 0
        for visit_numbers_dict in visit_numbers_infos:
            node = Node("就诊号",
                        name=visit_numbers_dict['就诊号'],
                        门诊号=visit_numbers_dict['门诊号'],
                        科室名称=visit_numbers_dict['科室名称'],
                        患者名称=visit_numbers_dict['患者名称'],
                        身份证号=visit_numbers_dict['身份证号'],
                        患者性别=visit_numbers_dict['患者性别'],
                        年龄=visit_numbers_dict['年龄'],
                        医生工号=visit_numbers_dict['医生工号'],
                        医疗付款方式=visit_numbers_dict['医疗付款方式'],
                        主要诊断编码=visit_numbers_dict['主要诊断编码'],
                        主要诊断描述=visit_numbers_dict['主要诊断描述'],
                        主要诊断名称=visit_numbers_dict['主要诊断名称'],
                        医生名称=visit_numbers_dict['医生名称'],
                        其他诊断1=visit_numbers_dict['其他诊断1'], 其他诊断1编码=visit_numbers_dict['其他诊断1编码'],
                        其他诊断2=visit_numbers_dict['其他诊断2'], 其他诊断2编码=visit_numbers_dict['其他诊断2编码'],
                        其他诊断3=visit_numbers_dict['其他诊断3'], 其他诊断3编码=visit_numbers_dict['其他诊断3编码'],
                        是否有新冠肺炎流行病学史=visit_numbers_dict['是否有新冠肺炎流行病学史'],
                        体格检查描述=visit_numbers_dict['体格检查描述'],
                        医嘱项目内容=visit_numbers_dict['医嘱项目内容'],
                        描述=visit_numbers_dict['描述'], 主诉=visit_numbers_dict['主诉'],
                        现病史=visit_numbers_dict['现病史'],既往史=visit_numbers_dict['既往史'])
            self.g.create(node)
            count += 1
            print(count)
        return

    '''创建知识图谱实体节点类型schema'''
    def create_graphnodes(self):
        patient_names, department_names, main_diagnosis_names, main_diagnostic_codes, doctor_names, doctor_ids, medical_payment_methods, main_complaints, contents_of_doctors_orders,\
        visit_numbers_infos, rels_patient_name_visit_number, rels_visit_number_department_name, rels_department_name_main_diagnosis_name, \
        rels_main_diagnosis_name_diagnostic_codes, rels_visit_department_doctor_name, rels_doctor_name_doctor_id, rels_visit_medical_payment_method, rels_main_complaint_diagnosis_name, \
        rels_department_doctor_name, rels_main_diagnosis_name_contents_of_doctors_orders = self.read_nodes()
        self.create_visit_numbers_nodes(visit_numbers_infos)
        self.create_node('患者名称', patient_names)
        self.create_node('科室名称', department_names)
        self.create_node('主要诊断名称', main_diagnosis_names)
        self.create_node('主要诊断编码', main_diagnostic_codes)
        self.create_node('医生名称', doctor_names)
        self.create_node('医生工号', doctor_ids)
        self.create_node('医疗付款方式', medical_payment_methods)
        self.create_node('主诉', main_complaints)
        self.create_node('医嘱项目内容', contents_of_doctors_orders)

        '''
        # Clinic_numbers, Visit_numbers, Department_names, Patient_names, Id_numbers, Patient_genders, Ages, Doctor_ids, Medical_payment_methods, Main_diagnostic_codes, Main_diagnosis_descriptions, Main_diagnosis_names, Doctor_names, Other_diagnoses_1s, Other_diagnosis_1_codes, Other_diagnoses_2s, \
        # Other_diagnosis_2_codes, Other_diagnoses_3s, Other_diagnosis_3_codes, Epidemiological_history_of_convid_19s, Physical_exam_descriptions, Contents_of_doctors_orders, Describes, Main_complaints, History_of_present_illnesses, Past_historys, disease_infos, rels_clinic, rels_clinic_visit, \
        # rels_department, rels_patient_name, rels_id_number, rels_patient_gender, rels_age, rels_doctor_id, rels_medical_payment_method, rels_main_diagnostic_code, rels_main_diagnosis_description, rels_main_diagnosis_name, rels_doctor_name, rels_other_diagnoses_1, rels_other_diagnosis_1_code, rels_other_diagnoses_2, \
        # rels_other_diagnosis_2_code, rels_other_diagnoses_3, rels_other_diagnosis_3_code, rels_epidemiological_history_of_convid_19, rels_ephysical_exam_description, rels_contents_of_doctors_order, rels_describe, rels_main_complaint, rels_history_of_present_illness, rels_past_history, \
        # rels_patient_name_clinic, rels_clinic_visit_number, rels_visit_department = self.read_nodes_1()
        # self.create_node("病历表", ['病历表'], nums=1)
        # self.create_node("中心节点个名称", Medical_Records, nums=2)    # Node(node_name, name=node_name)
        # self.create_node('门诊号_', Clinic_numbers, nums=1)
        # self.create_node('就诊号_', Visit_numbers, nums=1)
        # self.create_node('身份证号_', Id_numbers, nums=1)
        # self.create_node('患者性别_', Patient_genders, nums=1)
        # self.create_node('年龄_', Ages, nums=1)
        # self.create_node('主要诊断描述_', Main_diagnosis_descriptions, nums=1)
        # self.create_node('其他诊断1_', Other_diagnoses_1s, nums=1)
        # self.create_node('其他诊断1编码_', Other_diagnosis_1_codes, nums=1)
        # self.create_node('其他诊断2_', Other_diagnoses_2s, nums=1)
        # self.create_node('其他诊断2编码_', Other_diagnosis_2_codes, nums=1)
        # self.create_node('其他诊断3_', Other_diagnoses_3s, nums=1)
        # self.create_node('其他诊断3编码_', Other_diagnosis_3_codes, nums=1)
        # self.create_node('是否有新冠肺炎流行病学史_', Epidemiological_history_of_convid_19s, nums=1)
        # self.create_node('体格检查描述_', Physical_exam_descriptions, nums=1)
        # self.create_node('描述_', Describes, nums=1)
        # self.create_node('现病史_', History_of_present_illnesses, nums=1)
        # self.create_node('既往史_', Past_historys, nums=1)
        '''
        return

    '''创建实体关系边'''
    def create_graphrels(self):
        patient_names, department_names, main_diagnosis_names, main_diagnostic_codes, doctor_names, doctor_ids, medical_payment_methods, main_complaints, contents_of_doctors_orders, \
        visit_numbers_infos, rels_patient_name_visit_number, rels_visit_number_department_name, rels_department_name_main_diagnosis_name, \
        rels_main_diagnosis_name_diagnostic_codes, rels_visit_department_doctor_name, rels_doctor_name_doctor_id, rels_visit_medical_payment_method, rels_main_complaint_diagnosis_name, \
        rels_department_doctor_name, rels_main_diagnosis_name_contents_of_doctors_orders = self.read_nodes()
        self.create_relationship('患者名称', '就诊号', rels_patient_name_visit_number, '就诊号', '患者名和当次看病就诊号')
        self.create_relationship('就诊号', '科室名称', rels_visit_number_department_name, '科室名称', '该就诊号看的科室名')
        self.create_relationship('科室名称', '主要诊断名称', rels_department_name_main_diagnosis_name, '疾病名称', '当次就医的疾病名称')
        self.create_relationship('主要诊断名称', '主要诊断编码', rels_main_diagnosis_name_diagnostic_codes, '所属编码', '主要诊断编码')
        self.create_relationship('就诊号', '医生名称', rels_visit_department_doctor_name, '医生名', '医生名')
        self.create_relationship('医生名称', '医生工号', rels_doctor_name_doctor_id, '工号', '医生工号')
        self.create_relationship('就诊号', '医疗付款方式', rels_visit_medical_payment_method, '付款方式', '付款方式')
        self.create_relationship('主诉', '主要诊断名称', rels_main_complaint_diagnosis_name, '所属疾病名', '所属疾病名')
        self.create_relationship('科室名称', '医生名称', rels_department_doctor_name, '配置医生', '配置医生名')
        self.create_relationship('主要诊断名称', '医嘱项目内容', rels_main_diagnosis_name_contents_of_doctors_orders, '医嘱项目内容', '医嘱项目内容')

        '''
        # Clinic_numbers, Visit_numbers, Department_names, Patient_names, Id_numbers, Patient_genders, Ages, Doctor_ids, Medical_payment_methods, Main_diagnostic_codes, Main_diagnosis_descriptions, Main_diagnosis_names, Doctor_names, Other_diagnoses_1s, Other_diagnosis_1_codes, Other_diagnoses_2s, \
        # Other_diagnosis_2_codes, Other_diagnoses_3s, Other_diagnosis_3_codes, Epidemiological_history_of_convid_19s, Physical_exam_descriptions, Contents_of_doctors_orders, Describes, Main_complaints, History_of_present_illnesses, Past_historys, disease_infos, rels_clinic, rels_clinic_visit, \
        # rels_department, rels_patient_name, rels_id_number, rels_patient_gender, rels_age, rels_doctor_id, rels_medical_payment_method, rels_main_diagnostic_code, rels_main_diagnosis_description, rels_main_diagnosis_name, rels_doctor_name, rels_other_diagnoses_1, rels_other_diagnosis_1_code, rels_other_diagnoses_2, \
        # rels_other_diagnosis_2_code, rels_other_diagnoses_3, rels_other_diagnosis_3_code, rels_epidemiological_history_of_convid_19, rels_ephysical_exam_description, rels_contents_of_doctors_order, rels_describe, rels_main_complaint, rels_history_of_present_illness, rels_past_history, \
        # rels_patient_name_clinic, rels_clinic_visit_number, rels_visit_department = self.read_nodes_1()
        # self.create_relationship('病历表', '中心节点个名称', rels_detail_items, '细分项', '细分项目', nums=2) # p = rels_detail_items[0][0],q = rels_detail_items[0][1]
        # self.create_relationship('门诊号', '门诊号_', rels_clinic, '门诊号码唯一ID', '门诊号码', nums=1)
        # self.create_relationship('患者名称_', '门诊号', rels_patient_name_clinic, 'include', 'include', nums=3)
        # self.create_relationship('身份证号', '身份证号_', rels_id_number, '身份证号码', '身份证号', nums=1)
        # self.create_relationship('患者性别', '患者性别_', rels_patient_gender, '属于', '患者性别', nums=1)
        # self.create_relationship('年龄', '年龄_', rels_age, '当年年龄', '年龄', nums=1)
        # self.create_relationship('医生工号', '医生工号_', rels_doctor_id, '医生工号', '医生工号', nums=1)
        # self.create_relationship('医疗付款方式', '医疗付款方式_', rels_medical_payment_method, '医疗付款方式', '医疗付款方式', nums=1)
        # self.create_relationship('主要诊断编码', '主要诊断编码_', rels_main_diagnostic_code, '主要诊断编码', '主要诊断编码', nums=1)
        # self.create_relationship('主要诊断描述', '主要诊断描述_', rels_main_diagnosis_description, '主要诊断描述', '主要诊断描述', nums=1)
        # self.create_relationship('其他诊断1', '其他诊断1_', rels_other_diagnoses_1, '其他诊断1', '其他诊断1')
        # self.create_relationship('其他诊断1编码', '其他诊断1编码_', rels_other_diagnosis_1_code, '其他诊断1编码', '其他诊断1编码', nums=1)
        # self.create_relationship('其他诊断2', '其他诊断2_', rels_other_diagnoses_2, '其他诊断2', '其他诊断2', nums=1)
        # self.create_relationship('其他诊断2编码', '其他诊断2编码_', rels_other_diagnosis_2_code, '其他诊断2编码', '其他诊断2编码', nums=1)
        # self.create_relationship('其他诊断3', '其他诊断3_', rels_other_diagnoses_3, '其他诊断3', '其他诊断3', nums=1)
        # self.create_relationship('其他诊断3编码', '其他诊断3编码_', rels_other_diagnosis_3_code, '其他诊断3编码', '其他诊断3编码', nums=1)
        # self.create_relationship('是否有新冠肺炎流行病学史', '是否有新冠肺炎流行病学史_', rels_epidemiological_history_of_convid_19, '是否有新冠肺炎流行病学史', '是否有新冠肺炎流行病学史', nums=1)
        # self.create_relationship('体格检查描述', '体格检查描述_', rels_ephysical_exam_description, '体格检查描述', '体格检查描述', nums=1)
        # self.create_relationship('描述', '描述_', rels_describe, '描述', '描述', nums=1)
        # self.create_relationship('现病史', '现病史_', rels_history_of_present_illness, '现病史', '现病史', nums=1)
        # self.create_relationship('既往史', '既往史_', rels_past_history, '既往史', '既往史', nums=1)
        '''

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

        if not os.path.exists(self.dict_save_dir):
            os.makedirs(self.dict_save_dir)

        patient_names, department_names, main_diagnosis_names, main_diagnostic_codes, doctor_names, doctor_ids, medical_payment_methods, main_complaints, contents_of_doctors_orders, \
        visit_numbers_infos, rels_patient_name_visit_number, rels_visit_number_department_name, rels_department_name_main_diagnosis_name, \
        rels_main_diagnosis_name_diagnostic_codes, rels_visit_department_doctor_name, rels_doctor_name_doctor_id, rels_visit_medical_payment_method, rels_main_complaint_diagnosis_name, \
        rels_department_doctor_name, rels_main_diagnosis_name_contents_of_doctors_orders = self.read_nodes()

        with open(os.path.join(self.dict_save_dir, 'patient_names.txt'), 'w+', encoding='utf-8') as f_patient_names:
            f_patient_names.write('\n'.join(list(patient_names)))

        with open(os.path.join(self.dict_save_dir, 'department_names.txt'), 'w+', encoding='utf-8') as f_department_names:
            f_department_names.write('\n'.join(list(department_names)))

        with open(os.path.join(self.dict_save_dir, 'main_diagnosis_names.txt'), 'w+', encoding='utf-8') as f_main_diagnosis_names:
            f_main_diagnosis_names.write('\n'.join(list(main_diagnosis_names)))

        with open(os.path.join(self.dict_save_dir, 'main_diagnostic_codes.txt'), 'w+', encoding='utf-8') as f_main_diagnostic_codes:
            f_main_diagnostic_codes.write('\n'.join(list(main_diagnostic_codes)))

        with open(os.path.join(self.dict_save_dir, 'doctor_names.txt'), 'w+', encoding='utf-8') as f_doctor_names:
            f_doctor_names.write('\n'.join(list(doctor_names)))

        with open(os.path.join(self.dict_save_dir, 'doctor_ids.txt'), 'w+', encoding='utf-8') as f_doctor_ids:
            f_doctor_ids.write('\n'.join(list(doctor_ids)))

        with open(os.path.join(self.dict_save_dir, 'medical_payment_methods.txt'), 'w+', encoding='utf-8') as f_medical_payment_methods:
            f_medical_payment_methods.write('\n'.join(list(medical_payment_methods)))

        with open(os.path.join(self.dict_save_dir, 'main_complaints.txt'), 'w+', encoding='utf-8') as f_main_complaints:
            f_main_complaints.write('\n'.join(list(main_complaints)))

        with open(os.path.join(self.dict_save_dir, 'contents_of_doctors_orders.txt'), 'w+', encoding='utf-8') as f_contents_of_doctors_orders:
            f_contents_of_doctors_orders.write('\n'.join(list(contents_of_doctors_orders)))

        return

if __name__ == '__main__':
    handler = MedicalGraph()
    # handler.export_data()
    handler.create_graphnodes()
    handler.create_graphrels()