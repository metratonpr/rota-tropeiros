# Roteiro do projeto — estado atual e sequência recomendada de edição

Objetivo: fornecer um roteiro claro, não técnico, do que foi feito até agora neste projeto e a sequência correta
para edições futuras. Inclui também indicação dos arquivos alterados e explicações profissionais inseridas.

1) Resumo do que foi feito até aqui
- Projeto: aplicação Django simples para gerenciar rotas, paradas e horários.
- Alterações recentes realizadas:
  - `core/settings.py`: internacionalização configurada para Português do Brasil, fuso horário definido para
    `America/Sao_Paulo`, `LOCALE_PATHS` adicionado, e o app `rota` foi registrado com `RotaConfig`.
  - `rota/admin.py`: cabeçalhos do painel administrativo traduzidos para Português, ações em lote adicionadas
    (marcar ativo/inativo), e inlines configurados para facilitar a edição de horários por rota/parada.
  - `rota/apps.py`: `verbose_name` definido como "Sistema de Rotas e Horários" para melhorar a leitura do
    painel administrativo.
  - Foram adicionados arquivos explicativos em `docs/explicacoes/` com linguagem didática para não-programadores.

2) Estado atual (o que está pronto)
- Estrutura básica do Django pronta (arquivo `manage.py`, app `rota`, templates e estáticos iniciais).
- Área administrativa configurada e personalizada (títulos, ações, inlines).
- Configurações básicas ajustadas para ambiente de desenvolvimento em Português.
- Documentação de apoio criada em `docs/explicacoes/`.

3) Sequência recomendada para edição de arquivos (passo a passo)

Passo 0 — Preparação
- Antes de começar, crie um ponto de restauração (backup) do banco `db.sqlite3` e garanta um ambiente
  de desenvolvimento (virtualenv/venv) com dependências instaladas.

Passo 1 — Configurações gerais
- Arquivo: `core/settings.py`
- Motivo: mudanças aqui impactam todo o sistema (idioma, banco, segurança). Sempre edite com cautela.
- Ações típicas: ajustar `DEBUG`, `ALLOWED_HOSTS`, configurar banco para produção, definir variáveis
  de e-mail.

Passo 2 — Metadados do app
- Arquivo: `rota/apps.py`
- Motivo: altera como o app é exibido no painel administrativo; baixo risco.

Passo 3 — Modelos de dados (se necessário)
- Arquivo: `rota/models.py`
- Motivo: mudanças nas models alteram o esquema de dados; sempre criar/rodar migrações (`manage.py makemigrations` e `migrate`) e testar.

Passo 4 — Administração
- Arquivo: `rota/admin.py`
- Motivo: interface de gestão dos dados. Ajuste colunas, filtros, ações e inlines conforme necessidade. Teste com uma conta administrativa.

Passo 5 — Views e Templates
- Arquivos: `rota/views.py`, `templates/rota/*.html`, `static/rota/*`
- Motivo: alterações aqui afetam o que os visitantes veem. Teste navegando pelo site após mudanças.

Passo 6 — Testes e Qualidade
- Arquivo: `rota/tests.py` e demais testes
- Motivo: adicione testes unitários para cobrir mudanças principais. Execute `python manage.py test`.

Passo 7 — Deploy e produção
- Motivo: quando tudo estiver testado, preparar variáveis de ambiente, trocar banco se necessário, e garantir
  que `DEBUG = False` e `SECRET_KEY` esteja armazenada fora do código-fonte (variáveis de ambiente/secret manager).

4) Comentários profissionais inseridos nos arquivos
- `core/settings.py`: bloco explicativo no topo indicando riscos (SECRET_KEY, DEBUG), sequência segura
  de edição e notas sobre idioma e fuso.
- `rota/admin.py`: cabeçalho explicativo sobre propósito do arquivo, impacto e sequência segura para alterações.
- `rota/apps.py`: comentário descrevendo `verbose_name` e impacto (apenas usabilidade no admin).

5) Próximos passos sugeridos (prioridade)
1. Revisar `rota/models.py` (se houver mudanças planejadas) e criar testes que cubram funcionalidades críticas.
2. Preparar um ambiente de staging com `DEBUG = False` e configurar `ALLOWED_HOSTS` para testar deploy.
3. Se for publicar, mover `SECRET_KEY` para variáveis de ambiente e considerar trocar SQLite por Postgres.

6) Contato/Como orientar um leitor não técnico
- Se você é gestor e precisa mudar algo: descreva o que quer (ex.: "mudar idioma para PT-BR" ou "ocultar uma parada")
  e encaminhe ao time técnico. Para mudanças simples de texto (rótulos), podemos fazer direto; para alteracões de
  dados/infraestrutura, coordenar a execução com um desenvolvedor.

7) Deploy no Apache (passo a passo) — guia para não-programadores

Resumo: abaixo há uma sequência clara e mínima para colocar o projeto rodando em um servidor Apache
usando mod_wsgi. Essas instruções devem ser executadas por um administrador de servidor ou desenvolvedor.

Passos resumidos:
- Preparar servidor: instalar Python 3, pip e virtualenv; instalar Apache.
- Criar ambiente virtual dentro do diretório do projeto e instalar dependências com `pip install -r requirements.txt`.
- Ajustar `core/settings.py`: definir `DEBUG = False`, configurar `ALLOWED_HOSTS` com o domínio, e remover
  a `SECRET_KEY` do código (usar variável de ambiente no servidor).
- Executar `python manage.py migrate` para aplicar migrações.
- Executar `python manage.py collectstatic` para copiar arquivos estáticos (CSS/JS) para a pasta que o Apache serve.

Configuração Apache (resumo técnico para o time que vai executar):
- Instalar mod_wsgi (Ubuntu: `apt install libapache2-mod-wsgi-py3`).
- Criar arquivo de site, por exemplo `/etc/apache2/sites-available/rota.conf`, contendo:
  - `ServerName seusite.exemplo.com`
  - `WSGIDaemonProcess rota python-home=/caminho/para/venv python-path=/caminho/para/projeto`
  - `WSGIProcessGroup rota`
  - `WSGIScriptAlias / /caminho/para/projeto/core/wsgi.py`
  - `Alias /static/ /caminho/para/projeto/static/` e permissões `Require all granted` para esse alias.

Permissões e segurança:
- Verificar que o usuário do Apache (ex.: `www-data`) tenha permissão de leitura sobre o projeto e o virtualenv.
- Não dar permissões de escrita globais ao código-fonte; gravar uploads em pastas específicas com dono apropriado.

Ativação e verificação:
- Habilitar o site: `a2ensite rota.conf` e reiniciar Apache: `systemctl restart apache2`.
- Verificar logs em `/var/log/apache2/error.log` caso haja problemas.

Observações finais (para gestores não técnicos):
- Se não houver familiaridade com servidores, peça ao responsável de infraestrutura para executar esses passos.
- Solicite que o responsável valide `DEBUG = False` e a proteção das chaves antes de tornar o site público.
8) Quando você só pode RODAR CÓDIGO e NÃO PODE ALTERAR o servidor

Contexto: em alguns ambientes de hospedagem você tem permissão para executar comandos e manter
processos sob sua conta de usuário, mas não pode alterar configurações do servidor (Apache/nginx),
instalar pacotes globais ou editar arquivos de configuração do sistema. Abaixo estão opções práticas
e seguras para esse cenário, escritas para gestores e usuários não técnicos.

Resumo das opções possíveis (ordem de preferência):
- Opção A (se o servidor permite processos de usuário): executar a aplicação em um ambiente virtual
  (virtualenv) e rodar um servidor WSGI (gunicorn) no seu usuário; pedir ao provedor para encaminhar/abrir
  a porta/registrar o proxy reverso.
- Opção B (se não há possibilidade de encaminhar portas): usar o servidor de desenvolvimento apenas para
  testes internos (NÃO produção) ou usar um túnel reverso/SSH (apenas com suporte do provedor).
- Opção C (quando não é possível executar processos persistentes): gerar uma versão estática do site
  (exportar páginas estáticas) e subir apenas os arquivos estáticos/HTML.

Detalhamento passo-a-passo (Opção A — executar em virtualenv, recomendado quando possível)

1) Crie um ambiente virtual dentro da sua área (home) no servidor

  ```bash
  python3 -m venv ~/venv_rota
  source ~/venv_rota/bin/activate
  pip install -r /caminho/para/seu/projeto/requirements.txt
  ```

2) Ajuste variáveis de ambiente (no shell ou no painel, se houver)

  ```bash
  export DJANGO_SETTINGS_MODULE=core.settings
  export SECRET_KEY='sua_chave_secreta_aqui'   # melhor: configurar via painel
  export DEBUG=False
  export ALLOWED_HOSTS='["seu.dominio.exemplo"]'
  ```

3) Rodar migrações e coletar estáticos (uma única vez ou quando houver mudança)

  ```bash
  python manage.py migrate
  python manage.py collectstatic --noinput
  ```

4) Iniciar um servidor WSGI em segundo plano (ex.: gunicorn)

  ```bash
  pip install gunicorn
  # iniciar gunicorn ligado à sua conta em uma porta interna
  gunicorn core.wsgi:application --bind 127.0.0.1:8000 --workers 3 &
  ```

5) Encaminhamento / exposição do serviço

- Se o provedor aceitar, peça que façam um proxy reverso (Apache/nginx) do domínio para `127.0.0.1:8000`.
- Se não for possível, verifique se o painel permite mapear portas externas para processos do usuário.

Caveats importantes (linguagem simples)
- Mesmo funcionando, rodar gunicorn/servers sob a sua conta depende de como o provedor permite roteamento
  (port mapping) e processos persistentes. Sem suporte do provedor, o site não ficará acessível publicamente.
- Manter processos em background sem gestor de processos (supervisor/systemd) pode resultar em aplicações
  que param após logout ou reinício. Pergunte ao provedor sobre processos persistentes.

Opção B — Apenas para testes (NÃO usar em produção)

- Você pode usar o servidor de desenvolvimento do Django se for apenas para testes internos.

  ```bash
  python manage.py runserver 0.0.0.0:8000
  ```

- Importante: o `runserver` não é seguro para ambientes públicos e deve ser usado só localmente ou para
  demonstrações internas.

Opção C — Exportar páginas estáticas (quando não há execução persistente)

- Se não existe forma de ter um processo rodando, considere transformar o site em um conjunto de páginas
  estáticas (HTML) onde for possível. Isso remove funcionalidades dinâmicas (login, buscas em banco),
  mas permite publicar conteúdo estático (informações públicas, horários que mudam pouco).
- Ferramentas/abordagem: criar um comando de gerenciamento que renderize templates para arquivos HTML e
  enviar esses arquivos via painel.

Fluxo recomendado para equipes não técnicas
- Primeiro: confirmar com o provedor o que exatamente você pode fazer (executar processos? mapear portas?
  criar variáveis de ambiente?).
- Segundo: se puder rodar processos persistentes, siga a Opção A e peça ao provedor o ajuste de proxy/rede.
- Terceiro: se não for possível, discuta a Opção C (exportar estático) ou migrar para um host que aceite
  aplicações Python (serviço PaaS ou VPS).

Comandos úteis (copiar/colar)

```bash
# criar virtualenv, ativar e instalar deps
python3 -m venv ~/venv_rota
source ~/venv_rota/bin/activate
pip install -r requirements.txt

# migrar e coletar estáticos
python manage.py migrate
python manage.py collectstatic --noinput

# iniciar gunicorn (exemplo)
gunicorn core.wsgi:application --bind 127.0.0.1:8000 --workers 3 &
```

Se quiser, eu posso:
- Gerar `requirements.txt` aqui no repositório;
- Rodar `collectstatic` e empacotar `static/` pronto para upload;
- Rodar as migrações localmente e fornecer `db.sqlite3` para upload (se essa for sua escolha).

--

---
Arquivos de apoio criados:
- `docs/explicacoes/core_settings.md` — explicação didática de `core/settings.py`.
- `docs/explicacoes/rota_admin.md` — explicação didática de `rota/admin.py`.
- `docs/explicacoes/rota_apps.md` — explicação didática de `rota/apps.py`.

Se quiser, posso:
- Gerar um `README` resumido do diretório `docs/` com links para cada explicação;
- Abrir um Pull Request com essas mudanças para revisão;
- Adicionar checklist de pré-deploy (backup, migrações, variáveis de ambiente).
