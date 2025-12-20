from flask import Flask, request, jsonify
from transformers import pipeline

@app.route('/')
def index():
    return "API de IA rodando! Use as rotas /resumir, /traduzir, /gerarmensagem, etc."
# Pipelines/modelos
resumidor = pipeline('summarization', model='csebuetnlp/mT5_multilingual_XLSum')
tradutor_en_pt = pipeline('translation_en_to_pt', model='Helsinki-NLP/opus-mt-en-pt')
tradutor_pt_en = pipeline('translation_pt_to_en', model='Helsinki-NLP/opus-mt-pt-en')
gerador = pipeline('text-generation', model='gpt2')
sentimento = pipeline('sentiment-analysis')
classificador = pipeline('zero-shot-classification', model='facebook/bart-large-mnli')
resposta_qa = pipeline('question-answering')
corretor = pipeline('fill-mask', model='bert-base-uncased')
palavras_chave = pipeline('ner', grouped_entities=True)
detector = pipeline('text-classification', model='papluca/xlm-roberta-base-language-detection')

@app.route('/resumir', methods=['POST'])
def resumir():
    data = request.get_json()
    texto = data['texto']
    resumo = resumidor(texto, max_length=80, min_length=20, do_sample=False)
    return jsonify({'resumo': resumo[0]['summary_text']})
@app.route('/traduzir_en_pt', methods=['POST'])
def traduzir_en_pt():
    data = request.get_json()
    texto = data['texto']
    traducao = tradutor_en_pt(texto, max_length=80)
    return jsonify({'traducao_pt': traducao[0]['translation_text']})
@app.route('/traduzir_pt_en', methods=['POST'])
def traduzir_pt_en():
    data = request.get_json()
    texto = data['texto']
    traducao = tradutor_pt_en(texto, max_length=80)
    return jsonify({'traducao_en': traducao[0]['translation_text']})
@app.route('/gerarmensagem', methods=['POST'])
def gerar_mensagem():
    data = request.get_json()
    tema = data['tema']
    mensagem = gerador(tema, max_length=50, num_return_sequences=1)
    return jsonify({'mensagem': mensagem[0]['generated_text']})
@app.route('/sentimento', methods=['POST'])
def analisar_sentimento():
    data = request.get_json()
    texto = data['texto']
    result = sentimento(texto)
    return jsonify({'sentimento': result[0]['label'], 'score': result[0]['score']})
@app.route('/classificar', methods=['POST'])
def classificar():
    data = request.get_json()
    texto = data['texto']
    candidatos = data.get('candidatos', ['esporte', 'notícia', 'negócios', 'entretenimento'])
    resultado = classificador(texto, candidatos)
return jsonify({'classe': resultado['labels'][0], 'scores': resultado['scores']})
@app.route('/responder', methods=['POST'])
def responder():
    data = request.get_json()
    contexto = data['contexto']
    pergunta = data['pergunta']
    resposta = resposta_qa(question=pergunta, context=contexto)
    return jsonify({'resposta': resposta['answer'], 'score': resposta['score']})
@app.route('/corrigir', methods=['POST'])
def corrigir():
    data = request.get_json()
    texto = data['texto']
    texto_mask = texto.replace('__', '[MASK]')
    sugestoes = corretor(texto_mask)
    return jsonify({'correcao': sugestoes[0]['sequence']})
@app.route('/palavraschave', methods=['POST'])
def extrair_palavras_chave():
    data = request.get_json()
    texto = data['texto']
    resultado = palavras_chave(texto)
    chaves = [ent['word'] for ent in resultado]
    return jsonify({'palavras_chave': chaves})
@app.route('/detectar_idioma', methods=['POST'])
def detectar_idioma():
    data = request.get_json()
    texto = data['texto']
    resultado = detector(texto)
    return jsonify({'idioma': resultado[0]['label'], 'confiança': resultado[0]['score']})
if _name_ == '_main_':
    app.run(host='0.0.0.0', port=10000)
