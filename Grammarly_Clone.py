

from gramformer import Gramformer
import torch

def set_seed(seed):
  torch.manual_seed(seed)
  if torch.cuda.is_available():
    torch.cuda.manual_seed_all(seed)

gf = Gramformer(models = 2, use_gpu=False) # 0=detector, 1=highlighter, 2=corrector, 3=all

PATH = "/content/sample_data/gf.pth"

torch.save(gf, PATH)

gf_inference = torch.load(PATH)

influent_sentences = [
    
    "test",
]

for influent_sentence in influent_sentences:
    corrected_sentence = gf_inference.correct(influent_sentence)
    print("[Input] ", influent_sentence)
    print("[Correction] ",corrected_sentence[0])
    print("-" *100)

influent_sentences = [

    "test",
]   

for influent_sentence in influent_sentences:
    corrected_sentence = gf_inference.correct(influent_sentence)
    print("[Input] ", influent_sentence)
    print("[Highlight] ",gf.highlight(influent_sentence, corrected_sentence))
    print("[Correction] ",corrected_sentence[0])

    print("-" *100)



from colabcode import ColabCode
from fastapi import FastAPI

cc = ColabCode(port=12000, code=False)

app = FastAPI(title="OpenSource Grammarly API Alternative", description="with Gramformer & FastAPI", version="1.0")

# # Initialize logging
# my_logger = logging.getLogger()
# my_logger.setLevel(logging.DEBUG)
# logging.basicConfig(level=logging.DEBUG, filename='logs.log')

gf_inference = None

@app.on_event("startup")
def load_model():
    global gf_inference
    gf_inference = torch.load(PATH)

@app.post("/api/{sentence}")
async def get_predictions(sentence: str):
    try:
       # sentence = "This isn't how I like to ate food but that's what life give me"
        output_sentence = gf_inference.correct(sentence)
        return {"prediction": output_sentence[0]}
    except:
        my_logger.error("Something went wrong!")
        return {"prediction": "error"}

cc.run_app(app=app)

# model converted to python formm    