import os
from dotenv import load_dotenv
from benchmark import benchmark
from doc import FormDoc
from groq import Groq


def handler(event, context):
    return {"statusCode": 200, "body": "success"}


DIR = os.path.dirname(os.path.realpath(__file__))
# FORM_PATH = os.path.join(DIR, "../docs/alta_autonomos.pdf")
FORM_PATH = os.path.join(DIR, "../docs/consulta_de_fondos.pdf")
PIC_PATH = os.path.join(DIR, "../docs/dni.jpg")
OPT_PATH = os.path.join(DIR, "../docs/optimalOutput.json")
BENCH_PATH = os.path.join(DIR, "../docs/benchmark.xlsx")
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)
formDoc = FormDoc(FORM_PATH)

fields_to_fill = formDoc.get_fields_to_fill()


extracted_text = """REINO DE ESPAÑA
ES
DOCUMENTO NACIONAL DE IDENTIDAD
YA4000000
99999999R
DNI 99999999R
APELLIDOS
ESPAÑOLA
ESPAÑOLA
- TIMARI
CARMEN
SOY
NACIONALIDAD
NACIMENTO
F
ESP
ESPECIMEN
01 01 1980
CRISION
VALIDEZ
02 06 2021 02 06 2031
KUM SOPORTE
020631
CAA000000
from حساء
987654
DOCUMENTO NACIONAL or IDENTIDAD / NATIONAL IDENTITY CARD
DOMICILIO
AVDA DE MADRID S-N
MADRID
OOOOOAAS
MADRID
DNI
LUGAR DE NACIMIENTO
MADRID
MADRID
EQUIPO
HIJO/A DE
28391A6DK
JUAN / CARMEN
IDESPCAA000000499999999R<<
8001014F3106028ESP<<<<
<
ESPANOLA<ESPANOLA<<CARMEN<<"""

prompt = f"""
    Dado el texto obtenido abajo, quiero que rellenes los siguientes campos {fields_to_fill}.

    Tambien te doy mas informacion:
    - telefono 666666666
    - correo electronico: test@example.com
    - seccion: test 1
    - caja/legajo: test 1
    - expediente: test 1

    Hoy es 22 de marzo de 25

    Formato: el resultado tiene que ser un JSON como en el ejemplo con los campos rellenados, nada más. No me des nada más que no sea el JSON con los campos rellenados.

    Ejemplo:
    {{
        "nombre": ""
    }}

    Texto:
    {extracted_text}

"""
#model_name = "meta-llama/llama-4-scout-17b-16e-instruct"
#model_name = "meta-llama/llama-4-maverick-17b-128e-instruct"
model_name = "llama-3.3-70b-versatile"
#model_name = "qwen-qwq-32b"
chat_completion = client.chat.completions.create(
        messages=[
            {"role": "user", "content": [
                {"type": "text", "text": prompt},
            ]}
        ],
        model=model_name,
        temperature=0.6,
)
    
json_response = chat_completion.choices[0].message.content

print(f"Response from LLM: {json_response}")

EditedFields = formDoc.set_fields_to_fill(json_response) #Como he visto que aqui tienes parte del processing del Json que te devuelve el LLM he pillado solo los cambios que se aplican a partir de la respuesta del llm

benchmark.optimal(EditedFields ,fields_to_fill, OPT_PATH, BENCH_PATH, model_name)


# Create output directory if needed
output_dir = os.path.join(DIR, "../docs")
os.makedirs(output_dir, exist_ok=True)

# Save the filled PDF
output_path = os.path.join(output_dir, "consulta_de_fondos_filledTEST.pdf")
formDoc.save(output_path)
print(f"\nSuccessfully saved filled form to:\n{os.path.abspath(output_path)}")
