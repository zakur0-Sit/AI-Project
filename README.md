# Timetable

## Descrierea proiectului

Acest proiect implementează un sistem pentru crearea unui orar respectând constrângerile definite de utilizatori. Include funcționalități pentru definirea resurselor, adăugarea constrângerilor și verificarea fezabilității orarului.


## Funcționalități

#### Definirea Resurselor:
Profesori, grupe de studenți, intervale orare, săli disponibile, cursuri și seminarii.

#### Adăugarea Constrângerilor:
Constrângeri definite în limbaj natural (ex: indisponibilitate, ordine între cursuri și seminarii, limite globale etc.).
Suport pentru constrângeri hard și soft.

#### Validarea Fezabilității:
Verificarea satisfacției tuturor constrângerilor.
Generarea unui orar valid sau identificarea constrângerilor nesatisfiabile.

#### Input Flexibil:
Datele și constrângerile pot fi citite dintr-un program vizual, de la un prompt.

#### Output:
Orarul generat este salvat într-un fișier de output (output.txt) și este afișat și prin intermediul interfeței pentru ușurință.


## Structura Fișierelor

- **`main.py`**  
  Punctul principal de intrare al aplicației. Inițializează sistemul, conține algoritmul principal pentru crearea orarului și workflow-ul principal.

- **`/unavailability_model`**  
  Conține modelul fine-tuned pentru NLP processing

- **`nlp_training.py`**  
  Conține logica pentru antrenarea modelului NLP, folosit pentru interpretarea restricțiilor în limbaj natural.

- **`nlp_text_processing.py`**  
  Procesează textul utilizatorilor pentru a extrage entități precum zile, intervale orare și alte constrângeri.

- **`output_data/output.txt`**  
  Aici este orarul generat în format text

- **`constraints.json`**  
  Conține constrângerile generate cu ajutorul interfeței, generată în **`constraints_ui.py`**

- **`utils/teachers.json`**  
  Apar constrângerile generate de procesarea NLP folosind ce au comentat fiecare dintre utilizatori și se află deja în fișierul **`constraints.json`**  

- **`teachers.json`**  
  Apar constrângerile generate de procesarea NLP folosind ce au comentat fiecare dintre utilizatori și se află deja în fișierul **`constraints.json`**  

- **`utils/CourseEntry.py și utils/CourseEntryConstraints.py`**  
  Conțin modelarea constrângerilor hard și soft

