"""Interface Web local do LightWeek. Execute: python app.py."""
import inspect
import json
import math
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs
from sistema_recarga import Sessao, busca_sequencial, insertion_sort, calcular_estatisticas

ROOT = Path(__file__).parent
sessoes = []  # Objetos da classe Sessao; dados mantidos em memória.


def criar_sessao(dados):
    id_sessao = int(dados['id'])
    if str(id_sessao) != str(dados['id']) or id_sessao < 1:
        raise ValueError('O ID deve ser um inteiro positivo.')
    if busca_sequencial(sessoes, id_sessao) != -1:
        raise ValueError('Já existe uma sessão com esse ID.')
    veiculo = str(dados['veiculo']).strip()
    if not veiculo or len(veiculo) > 60:
        raise ValueError('Informe um veículo com até 60 caracteres.')
    numeros = [float(str(dados[c]).replace(',', '.')) for c in ('energia_kwh', 'tempo_minutos', 'tarifa_kwh')]
    if any(not math.isfinite(v) or v < 0 or v > 1000000 for v in numeros):
        raise ValueError('Energia, tempo e tarifa devem ser números entre 0 e 1.000.000.')
    data = str(dados['data'])
    datetime.strptime(data, '%Y-%m-%d')
    if dados['status'] not in ('Finalizada', 'Em andamento'):
        raise ValueError('Status inválido.')
    if dados['tipo_carregador'] not in ('Lento - 7,4 kW', 'Rápido - 22 kW', 'Ultrarrápido - 50 kW'):
        raise ValueError('Carregador inválido.')
    nova = Sessao(id_sessao, veiculo, dados['tipo_carregador'], *numeros, data, dados['status'])
    sessoes.append(nova)
    return vars(nova)


class Handler(BaseHTTPRequestHandler):
    def enviar(self, dados, status=200):
        body = json.dumps(dados, ensure_ascii=False, allow_nan=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        url = urlparse(self.path)
        if url.path == '/api/sessoes':
            self.enviar({'sessoes': [vars(s) for s in sessoes], 'estatisticas': calcular_estatisticas(sessoes)})
        elif url.path == '/api/busca':
            try:
                alvo = int(parse_qs(url.query)['id'][0])
                pos = busca_sequencial(sessoes, alvo)
                self.enviar({'sessao': vars(sessoes[pos]) if pos != -1 else None,
                             'comparacoes': pos + 1 if pos != -1 else len(sessoes)})
            except (ValueError, KeyError):
                self.enviar({'erro': 'Informe um ID inteiro.'}, 400)
        elif url.path == '/api/codigo':
            self.enviar({'estrutura': inspect.getsource(Sessao), 'busca': inspect.getsource(busca_sequencial),
                         'ordenacao': inspect.getsource(insertion_sort), 'integracao': inspect.getsource(criar_sessao),
                         'estatisticas': inspect.getsource(calcular_estatisticas)})
        elif url.path in ('/', '/style.css', '/app.js'):
            name = 'index.html' if url.path == '/' else url.path[1:]
            body = (ROOT / 'web' / name).read_bytes()
            self.send_response(200)
            self.send_header('Content-Type', {'html': 'text/html', 'css': 'text/css', 'js': 'text/javascript'}[name.split('.')[-1]] + '; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self.enviar({'erro': 'Não encontrado'}, 404)

    def do_POST(self):
        # Aplicação didática local: recusa chamadas vindas de outra origem.
        origin = self.headers.get('Origin')
        if origin and origin != 'http://' + self.headers.get('Host', ''):
            return self.enviar({'erro': 'Origem não permitida'}, 403)
        try:
            length = int(self.headers.get('Content-Length', '0'))
            if length > 10000:
                raise ValueError('Requisição muito grande.')
            dados = json.loads(self.rfile.read(length))
            if self.path == '/api/sessoes':
                self.enviar(criar_sessao(dados), 201)
            elif self.path == '/api/ordenar':
                criterio = int(dados['criterio'])
                if criterio not in (1, 2, 3, 4) or not isinstance(dados['crescente'], bool):
                    raise ValueError('Critério inválido.')
                insertion_sort(sessoes, criterio, dados['crescente'])
                self.enviar({'ok': True})
            else:
                self.enviar({'erro': 'Não encontrado'}, 404)
        except (ValueError, KeyError, TypeError, OverflowError) as exc:
            self.enviar({'erro': str(exc)}, 400)


if __name__ == '__main__':
    import sys
    import webbrowser
    from threading import Timer
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    server = ThreadingHTTPServer(('127.0.0.1', port), Handler)
    url = f'http://127.0.0.1:{port}'
    print(f'LightWeek pronto: {url}', flush=True)
    print('Mantenha esta janela aberta. Para encerrar: Ctrl+C.', flush=True)
    if '--abrir' in sys.argv:
        Timer(1, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
