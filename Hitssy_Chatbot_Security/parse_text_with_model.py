import json
from rasa_nlu.model import Interpreter

model_directory = '/home/marlon/Hitssy_Security/project_code/11_building_a_chat_bot/models/nlu/default/model_20190304-190112'
nlu_interpreter = Interpreter.load(model_directory)

text = "What is the capital of Great Britain?"
data = nlu_interpreter.parse(text)
print(json.dumps(data, indent=2))