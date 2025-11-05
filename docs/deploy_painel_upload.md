# Deploy via painel (apenas upload de arquivos)

Este guia explica, em linguagem simples, como publicar este projeto Django em um servidor cujo painel
de controle só permite enviar arquivos (upload) e configurar algumas opções básicas. Há várias formas de
painéis (cPanel, Plesk, painel de hospedagem própria). Aqui estão instruções genéricas e seguras para
quem não é programador.

IMPORTANTE: Cada provedor tem limites diferentes. Se alguma etapa não for possível no painel, peça ao
suporte do provedor que execute o passo indicado (por exemplo, ativar mod_wsgi ou criar um banco de dados).

Visão geral (o que você precisa fazer)
- Preparar o projeto localmente (no seu computador).
- Gerar os arquivos estáticos prontos (CSS/JS/imagens) e o banco de dados inicial, se não puder executar
  comandos no servidor.
- Fazer upload dos arquivos do projeto para o painel.
- Configurar no painel o apontamento WSGI (se o painel oferecer suporte a apps Python) e definir variáveis
  de ambiente, especialmente `SECRET_KEY`, `DEBUG=False` e `ALLOWED_HOSTS`.

Opções principais (escolha a que se aplica ao seu painel)
1) Painel com suporte a aplicações Python (recomendado)
2) Painel que só serve arquivos estáticos (não recomendado para Django)
3) Painel com FTP/SFTP e suporte limitado (midway)

1) Painel com suporte a aplicações Python (o ideal)

Resumo: muitos painéis modernos permitem criar uma "aplicação Python" e apontar o WSGI. Nesses casos
você só precisa enviar os arquivos e configurar virtualenv e variáveis de ambiente via painel.

Passos detalhados (passo a passo simples):

a) Preparar localmente (no seu computador)
- No seu PC, abra o projeto e crie um arquivo `requirements.txt` com todas as dependências:

  - No terminal, dentro do virtualenv do projeto:

    ```bash
    pip freeze > requirements.txt
    ```

- Verifique `core/settings.py`: idealmente o projeto deve ler `SECRET_KEY` e `DEBUG` de variáveis de
  ambiente. Se isso não estiver implementado, crie um arquivo `secret_key.txt` com a chave e faça upload
  para o painel (veja mais adiante onde colocá-lo com segurança).

b) Preparar banco e arquivos estáticos (se você não puder rodar comandos no servidor)
- Se o painel NÃO permite executar `manage.py migrate` no servidor, você pode:
  - Executar `python manage.py migrate` localmente e enviar o arquivo `db.sqlite3` resultante para o servidor.
    Atenção: isso funciona para projetos pequenos e se o provedor aceita SQLite; nem todos aceitam.
  - Alternativa (melhor): pedir ao painel para criar um banco Postgres/MySQL e colocar as credenciais no
    painel; então peça ao suporte que execute as migrações, ou use SSH/console fornecido pelo painel para
    executar `manage.py migrate`.

- Gerar arquivos estáticos locais e enviar ao servidor:

  ```bash
  python manage.py collectstatic --noinput
  ```

  Em seguida, faça upload da pasta `static/` gerada para o local do servidor que serve arquivos estáticos
  (alguns painéis têm uma seção para arquivos estáticos).

c) Upload dos arquivos do projeto
- Faça upload da pasta do projeto (todos os arquivos `.py`, `templates/`, `static/` gerado, `manage.py`, etc.)
  para a área indicada pelo painel.

d) Configurar a aplicação Python no painel
- Crie/ative um virtualenv via painel (ou peça ao suporte). Instale dependências: `pip install -r requirements.txt`.
- Aponte o WSGI para `core/wsgi.py` (caminho relativo ao local onde você mandou os arquivos).
- Defina as variáveis de ambiente no painel:
  - `DJANGO_SETTINGS_MODULE=core.settings`
  - `SECRET_KEY` = (valor seguro, não subir no código)
  - `DEBUG=False`
  - `ALLOWED_HOSTS` = domínio do site (ex.: `meusite.exemplo`) — alguns painéis pedem isso em formato JSON;
    se não suportarem, edite `core/settings.py` temporariamente para incluir o host, e depois volte para usar
    variável de ambiente.

e) Permissões e logs
- Verifique logs do painel / Apache para erros. Se algo falhar, mostre os logs ao suporte técnico.

2) Painel que só serve arquivos estáticos

- Se o painel só permite servir HTML/CSS/JS (sem suporte a Python/WSGI), não é possível executar Django
  no servidor — você precisará de um provedor com suporte a Python ou usar um serviço especializado (Heroku,
  Render, Railway, um VPS ou um serviço de hospedagem com WSGI).

3) Painel com FTP/SFTP e suporte limitado

- Se você tem FTP/SFTP e o painel permite ativar uma aplicação Python mas não comandos via SSH, combine
  estas ações:
  - Gerar o `requirements.txt` e enviar ao painel.
  - Criar virtualenv via painel e instalar dependências (ou pedir ao suporte).
  - Executar migrações localmente e enviar `db.sqlite3` (se permitido) ou pedir ao suporte que execute
    `manage.py migrate` no servidor.

Checklist prático (para você entregar ao suporte ou usar no painel):
- [ ] `requirements.txt` gerado e enviado.
- [ ] `static/` gerado localmente com `collectstatic` e enviado para a pasta estática do servidor.
- [ ] `SECRET_KEY` configurado no painel (variável de ambiente) ou arquivo seguro fora da raiz pública.
- [ ] `DEBUG=False` configurado.
- [ ] `ALLOWED_HOSTS` incluindo o domínio.
- [ ] `core/wsgi.py` presente e apontado como WSGI entrypoint no painel.
- [ ] Banco configurado no painel (se for MySQL/Postgres), ou `db.sqlite3` enviado (apenas se o painel aceitar).

Boas práticas e segurança (em linguagem simples)
- Não envie `SECRET_KEY` em arquivos públicos ou em repositórios. Se for necessário enviar um arquivo com
  a chave, confirme com o suporte do painel onde deixá-lo fora do diretório público (nem sempre é possível).
- Sempre defina `DEBUG=False` em produção. Se você esquecer, o painel pode exibir mensagens técnicas ao público.
- Peça ao suporte para configurar backups regulares do banco.

O que eu posso preparar para facilitar (opções que eu posso fazer aqui)
- Gerar um `requirements.txt` com base no ambiente atual do projeto.
- Gerar os arquivos estáticos (`collectstatic`) e empacotar `static/` pronto para upload.
- Rodar migrações localmente e fornecer o arquivo `db.sqlite3` para upload (se essa for a sua opção).
- Criar um exemplo de `rota.conf` (Apache) completo para dar ao suporte, caso o painel use Apache/mod_wsgi.

Diga qual opção você prefere (por exemplo, "quero que você gere `requirements.txt` e o `static/` pronto");
eu preparo esses arquivos para você fazer upload no painel.
