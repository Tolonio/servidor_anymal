from flask import Flask, render_template, send_file, request, abort, jsonify #tilizado para criar o servidor HTTP e gerir as rotas (URLs) do painel de controle
import os #navegação nas pastas do SSD do ANYmal
from processador_relatorio import (
    gerar_relatorio_nativo, 
    listar_diretorio_nativo, 
    status_progresso, 
    atualizar_progresso,
    PASTA_REMOTA
)

app = Flask(__name__)

@app.route('/api/progresso')
def rota_progresso():
    return jsonify(status_progresso)

@app.route('/')
def index():
    caminho_atual = request.args.get('path', PASTA_REMOTA)
    if not caminho_atual: caminho_atual = '/'
    
    itens = listar_diretorio_nativo(caminho_atual)
    if itens is None: return "Caminho não encontrado no robô.", 404

    parent_dir = os.path.dirname(caminho_atual.rstrip('/'))
    if not parent_dir: parent_dir = '/'
        
    # Agora o Flask procura o arquivo HTML na pasta 'templates'
    return render_template('index.html', itens=itens, caminho_atual=caminho_atual, parent_dir=parent_dir, pasta_base=PASTA_REMOTA)

@app.route('/baixar_arquivo')
def baixar_arquivo():
    caminho = request.args.get('path')
    if caminho and os.path.exists(caminho):
        return send_file(caminho, as_attachment=True)
    abort(404)

@app.route('/traduzir_missao')
def traduzir_missao():
    caminho_missao = request.args.get('path')
    if not caminho_missao: abort(400)
    
    atualizar_progresso(0, "Iniciando processo...")
    
    try:
        memoria_zip = gerar_relatorio_nativo(caminho_missao)
        nome_pasta = os.path.basename(caminho_missao.rstrip('/'))
        return send_file(memoria_zip, as_attachment=True, download_name=f"Relatorio_PDF_{nome_pasta}_PT.zip", mimetype='application/zip')
    except Exception as e:
        atualizar_progresso(100, "Erro!")
        return f"<h2>Erro de processamento:</h2><p>{str(e)}</p>", 500

if __name__ == '__main__':
    print("=== Servidor Nativo Iniciado na porta 5050 ===")
    app.run(host='0.0.0.0', port=5050, debug=False, threaded=True)
