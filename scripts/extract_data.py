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
        
        class_data = {
            "metadata": {
                "ano": str(df.iloc[1, 1]).strip(),
                "diretoria": str(df.iloc[2, 1]).strip(),
                "escola": str(df.iloc[3, 1]).strip(),
                "tipo_ensino": str(df.iloc[4, 1]).strip(),
                "turma": turma_name,
                "tipo_fechamento": str(df.iloc[6, 1]).strip(),
            },
            "subjects": [],
            "students": []
        }
        
        # Header rows: row 10 is subject names, row 11 is sub-headers (Nº, M, F, AC)
        subject_row = df.iloc[10]
        for i in range(2, len(subject_row) - 4, 4):
            name = str(subject_row[i]).replace('\n', ' ').strip()
            if name and name != 'nan' and name != 'TOTAL':
                class_data["subjects"].append({
                    "name": name,
                    "col_idx": i
                })
                
        # Student rows: from row 12 onwards
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
                student["grades"].append({
                    "subject": sub["name"],
                    "numero": str(row[col]).strip(),
                    "bim1": str(row[col+1]).strip() if str(row[col+1]).strip() != 'nan' else '-',
                    "bim2": "-",
                    "bim3": "-",
                    "bim4": "-",
                    "final": "-",
                    "faltas": str(row[col+2]).strip(),
                    "ausencia_compensada": str(row[col+3]).strip()
                })
            class_data["students"].append(student)
        return class_data
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

def main():
    all_classes = []
    files = glob.glob(os.path.join(sources_dir, "*.xlsx"))
    
    for file in files:
        print(f"Processing {os.path.basename(file)}...")
        data = extract_file_data(file)
        if data:
            all_classes.append(data)
            
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("const BOLETIM_DATA = ")
        json.dump(all_classes, f, ensure_ascii=False, indent=4)
        f.write(";")
    print(f"Successfully extracted {len(all_classes)} classes to data.js")

if __name__ == "__main__":
    main()
