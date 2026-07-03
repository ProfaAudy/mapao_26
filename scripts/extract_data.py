import pandas as pd
import json
import os
import glob

sources_dir = r'I:\Meu Drive\PROATI\Boletim\sources'
output_path = r'I:\Meu Drive\PROATI\Boletim\data\data.js'

def to_int(val):
    if not val or str(val).strip() in ['-', 'nan', '']:
        return 0
    try:
        clean_val = str(val).split('.')[0].strip()
        return int(clean_val)
    except Exception:
        return 0

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
        
        # Identifica as colunas de cabeçalho da linha 11
        row11 = list(df.iloc[11])
        tf_idx = len(row11) - 4
        fre_idx = len(row11) - 1  # Por padrão tenta a última coluna: Fre An(%)
        fre_bim_idx = len(row11) - 3  # Por padrão tenta a coluna: Fre(%)
        
        for idx_col, val in enumerate(row11):
            val_str = str(val).strip()
            if val_str == 'TF':
                tf_idx = idx_col
            elif val_str == 'Fre An(%)':
                fre_idx = idx_col
            elif val_str == 'Fre(%)':
                fre_bim_idx = idx_col

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
                
            freq_bim_val = str(row[fre_bim_idx]).strip()
            if not freq_bim_val or freq_bim_val.lower() in ['nan', '']:
                freq_bim_val = '-'
                
            student = {
                "name": name,
                "situacao": str(row[1]).strip(),
                "grades": [],
                "total_faltas": str(row[tf_idx]).strip(),
                "frequencia": str(row[fre_idx]).strip(),
                "freq_bim1": "-",
                "freq_bim2": "-",
                "freq_bim3": "-",
                "freq_bim4": "-"
            }
            # Atribui no bimestre correspondente
            student[f"freq_bim{bim_index}"] = freq_bim_val
            
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
                    
                    # Atualiza informações gerais com o bimestre mais recente (frequência e situação)
                    if bim_index >= existing_class["_highest_bim"]:
                        est["frequencia"] = new_student["frequencia"]
                        est["situacao"] = new_student["situacao"]
                        
                    # Acumula o total de faltas do aluno somando as do bimestre atual com as anteriores
                    est["total_faltas"] = str(to_int(est["total_faltas"]) + to_int(new_student["total_faltas"]))
                    
                    # Mescla as frequências bimestrais
                    est[f"freq_bim{bim_index}"] = new_student[f"freq_bim{bim_index}"]
                        
                    # Mescla notas das matérias e soma suas faltas/AC
                    est_grades = {g["subject"]: g for g in est["grades"]}
                    for new_grade in new_student["grades"]:
                        sub_name = new_grade["subject"]
                        val = new_grade[f"bim{bim_index}"]
                        
                        if sub_name in est_grades:
                            # Atualiza a nota do bimestre correspondente
                            est_grades[sub_name][f"bim{bim_index}"] = val
                            # Soma as faltas e AC do bimestre para cada matéria
                            est_grades[sub_name]["faltas"] = str(to_int(est_grades[sub_name]["faltas"]) + to_int(new_grade["faltas"]))
                            est_grades[sub_name]["ausencia_compensada"] = str(to_int(est_grades[sub_name]["ausencia_compensada"]) + to_int(new_grade["ausencia_compensada"]))
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
