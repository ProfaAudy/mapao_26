import pandas as pd
import json
import os
import glob

sources_dir = r'I:\Meu Drive\PROATI\Boletim\sources'
output_path = r'I:\Meu Drive\PROATI\Boletim\data\data.js'

def extract_file_data(file_path):
    try:
        df = pd.read_excel(file_path, header=None)
        
        turma_name = str(df.iloc[5, 1]).strip()
        tipo_fechamento = str(df.iloc[6, 1]).strip()
        
        # Determina o índice do bimestre baseado no fechamento da planilha
        tipo_lower = tipo_fechamento.lower()
        bim_index = 1
        if "segundo" in tipo_lower:
            bim_index = 2
        elif "terceiro" in tipo_lower:
            bim_index = 3
        elif "quarto" in tipo_lower:
            bim_index = 4
        
        class_data = {
            "metadata": {
                "ano": str(df.iloc[1, 1]).strip(),
                "diretoria": str(df.iloc[2, 1]).strip(),
                "escola": str(df.iloc[3, 1]).strip(),
                "tipo_ensino": str(df.iloc[4, 1]).strip(),
                "turma": turma_name,
                "tipo_fechamento": tipo_fechamento,
            },
            "subjects": [],
            "students": []
        }
        
        # Linhas de cabeçalho: linha 10 nomes das matérias, linha 11 subcabeçalhos (Nº, M, F, AC)
        subject_row = df.iloc[10]
        for i in range(2, len(subject_row) - 4, 4):
            name = str(subject_row[i]).replace('\n', ' ').strip()
            if name and name != 'nan' and name != 'TOTAL':
                class_data["subjects"].append({
                    "name": name,
                    "col_idx": i
                })
                
        # Linhas dos alunos: a partir da linha 12
        for idx in range(12, len(df)):
            row = df.iloc[idx]
            name = str(row[0]).strip()
            if not name or name == 'nan' or name == 'Aulas Dadas:' or name == 'Legenda' or name == ' ' or name == '':
                break
                
            student = {
                "name": name,
                "situacao": str(row[1]).strip(),
                "grades": [],
                "total_faltas": str(row[len(row)-4]).strip(),
                "frequencia": str(row[len(row)-3]).strip()
            }
            
            for sub in class_data["subjects"]:
                col = sub["col_idx"]
                grade_val = str(row[col+1]).strip() if str(row[col+1]).strip() != 'nan' else '-'
                
                grades_dict = {
                    "subject": sub["name"],
                    "numero": str(row[col]).strip(),
                    "bim1": "-",
                    "bim2": "-",
                    "bim3": "-",
                    "bim4": "-",
                    "final": "-",
                    "faltas": str(row[col+2]).strip(),
                    "ausencia_compensada": str(row[col+3]).strip()
                }
                # Preenche apenas o bimestre correspondente desta planilha
                grades_dict[f"bim{bim_index}"] = grade_val
                
                student["grades"].append(grades_dict)
            class_data["students"].append(student)
        return class_data, bim_index
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None, None

def main():
    merged_classes = {}
    files = glob.glob(os.path.join(sources_dir, "*.xlsx"))
    
    parsed_files = []
    for file in files:
        print(f"Processing {os.path.basename(file)}...")
        data, bim_index = extract_file_data(file)
        if data:
            parsed_files.append((data, bim_index))
            
    # Ordena pelo bimestre para garantir que o 1º bimestre seja processado antes do 2º, etc.
    parsed_files.sort(key=lambda x: x[1])
    
    for class_data, bim_index in parsed_files:
        turma = class_data["metadata"]["turma"]
        
        if turma not in merged_classes:
            merged_classes[turma] = class_data
            merged_classes[turma]["_highest_bim"] = bim_index
        else:
            existing_class = merged_classes[turma]
            
            # Se for um bimestre mais recente ou igual, atualiza metadados e estatísticas gerais
            if bim_index >= existing_class["_highest_bim"]:
                existing_class["metadata"]["tipo_fechamento"] = class_data["metadata"]["tipo_fechamento"]
                existing_class["_highest_bim"] = bim_index
                
            # Mescla disciplinas novas se houver
            existing_subjects = {s["name"] for s in existing_class["subjects"]}
            for sub in class_data["subjects"]:
                if sub["name"] not in existing_subjects:
                    existing_class["subjects"].append(sub)
                    
            # Mescla dados dos alunos
            existing_students = {s["name"]: s for s in existing_class["students"]}
            
            for new_student in class_data["students"]:
                name = new_student["name"]
                if name in existing_students:
                    est = existing_students[name]
                    
                    # Atualiza informações gerais com o bimestre mais recente
                    if bim_index >= existing_class["_highest_bim"]:
                        est["total_faltas"] = new_student["total_faltas"]
                        est["frequencia"] = new_student["frequencia"]
                        est["situacao"] = new_student["situacao"]
                        
                    # Mescla notas das matérias
                    est_grades = {g["subject"]: g for g in est["grades"]}
                    for new_grade in new_student["grades"]:
                        sub_name = new_grade["subject"]
                        val = new_grade[f"bim{bim_index}"]
                        
                        if sub_name in est_grades:
                            # Atualiza a nota do bimestre correspondente
                            est_grades[sub_name][f"bim{bim_index}"] = val
                            # Atualiza também faltas e AC mais recentes da matéria
                            est_grades[sub_name]["faltas"] = new_grade["faltas"]
                            est_grades[sub_name]["ausencia_compensada"] = new_grade["ausencia_compensada"]
                        else:
                            est["grades"].append(new_grade)
                else:
                    existing_class["students"].append(new_student)
                    
    # Remove chave temporária e consolida lista
    all_classes = []
    for turma, class_data in merged_classes.items():
        class_data.pop("_highest_bim", None)
        all_classes.append(class_data)
        
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("const BOLETIM_DATA = ")
        json.dump(all_classes, f, ensure_ascii=False, indent=4)
        f.write(";")
    print(f"Successfully extracted and merged {len(all_classes)} classes to data.js")

if __name__ == "__main__":
    main()
