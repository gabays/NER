# NER models trained with spaCy

## Install and run

```
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

run the script:

```
python run_ner.py 
```

## Parameters

You can choose the batch size [here](https://github.com/gabays/NER/blob/f1b24e21641524e13080550fe287584a06931f9c/run_ner.py#L49) and the number of workers [here](https://github.com/gabays/NER/blob/f1b24e21641524e13080550fe287584a06931f9c/run_ner.py#L110).

All models are attached to the [0.1 release](https://github.com/gabays/NER/blob/f1b24e21641524e13080550fe287584a06931f9c/run_ner.py#L110):
- [Simple CNN](https://github.com/gabays/NER/releases/download/0.1/ck-model-best-cnn.zip)
- [Camembert based](https://github.com/gabays/NER/releases/download/0.1/camembert_base.zip)

## Credits

[Simon Gabay](https://www.unige.ch/lettres/humanites-numeriques/equipe/collaborateurs/simon-gabay), UniGE
