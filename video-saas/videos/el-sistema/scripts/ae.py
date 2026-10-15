"""Puente a After Effects sin pasar por el MCP de la sesión.

El servidor `fnf-after-effects-mcp` habla JSON-RPC por stdio, así que se puede
lanzar como proceso y hablarle directamente. Esto evita depender de que el
conector esté autorizado en la sesión.

Uso como módulo:

    from ae import AE
    with AE() as ae:
        print(ae.call('ae_project_info'))
        ae.batch([{'operation': 'comp.create', 'args': {...}}])
"""
from pathlib import Path
import json
import subprocess
import sys

SERVER = Path('/Users/alejandrorubiocamarero/Documents/ChatGPT/editor/video-saas/.runtime-ae/node_modules/fnf-after-effects-mcp/dist/index.js')


class AEError(RuntimeError):
    pass


class AE:
    def __init__(self, log: Path | None = None):
        self.proc = None
        self.id = 0
        self.log = log

    # ------------------------------------------------------------ ciclo de vida
    def __enter__(self):
        self.proc = subprocess.Popen(
            ['node', str(SERVER)],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, bufsize=1)
        self._rpc('initialize', {
            'protocolVersion': '2024-11-05',
            'capabilities': {},
            'clientInfo': {'name': 'ad5', 'version': '1.0'},
        })
        self._notify('notifications/initialized')
        return self

    def __exit__(self, *_):
        if self.proc:
            try:
                self.proc.stdin.close()
            except Exception:
                pass
            self.proc.terminate()
            try:
                self.proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.proc.kill()

    # ------------------------------------------------------------------- JSON-RPC
    def _send(self, msg):
        self.proc.stdin.write(json.dumps(msg) + '\n')
        self.proc.stdin.flush()

    def _notify(self, method, params=None):
        self._send({'jsonrpc': '2.0', 'method': method, 'params': params or {}})

    def _rpc(self, method, params=None):
        self.id += 1
        want = self.id
        self._send({'jsonrpc': '2.0', 'id': want, 'method': method,
                    'params': params or {}})
        while True:
            line = self.proc.stdout.readline()
            if not line:
                err = self.proc.stderr.read()
                raise AEError(f'el servidor terminó sin responder: {err[-800:]}')
            line = line.strip()
            if not line:
                continue
            try:
                msg = json.loads(line)
            except json.JSONDecodeError:
                continue                       # traza del servidor, no es respuesta
            if msg.get('id') != want:
                continue                       # notificación o respuesta ajena
            if 'error' in msg:
                raise AEError(json.dumps(msg['error'], ensure_ascii=False))
            return msg.get('result')

    # ----------------------------------------------------------------- herramientas
    def tools(self):
        return [t['name'] for t in self._rpc('tools/list')['tools']]

    def call(self, tool_name, **arguments):
        res = self._rpc('tools/call', {'name': tool_name, 'arguments': arguments})
        if self.log:
            with open(self.log, 'a') as fh:
                fh.write(json.dumps({'tool': tool_name, 'result': res},
                                    ensure_ascii=False) + '\n')
        if res.get('isError'):
            texts = [c.get('text', '') for c in res.get('content', [])]
            raise AEError(f'{tool_name}: ' + ' '.join(texts)[:1500])
        out = res.get('structuredContent')
        if out is None:
            texts = [c.get('text', '') for c in res.get('content', [])]
            joined = '\n'.join(texts)
            try:
                return json.loads(joined)
            except json.JSONDecodeError:
                return joined
        return out

    def batch(self, ops, stop_on_error=True):
        """Ejecuta un lote de operaciones, troceándolo para no saturar el puente."""
        results = []
        for i in range(0, len(ops), 120):
            chunk = ops[i:i + 120]
            results.append(self.call('ae_do', operation='batch.run',
                                     args={'ops': chunk, 'stopOnError': stop_on_error}))
        return results


if __name__ == '__main__':
    with AE() as ae:
        names = ae.tools()
        print(f'{len(names)} herramientas:', ', '.join(names))
        print()
        info = ae.call('ae_project_info')
        print(json.dumps(info, ensure_ascii=False, indent=1)[:1500])
