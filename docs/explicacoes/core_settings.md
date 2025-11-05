# Explicação didática: `core/settings.py`

Este arquivo contém as configurações gerais do site — pense nele como o “painel de controle” do projeto. Alterações aqui mudam o comportamento de todo o sistema. A seguir explico, em linguagem simples, as partes mais importantes.

Resumo rápido (para não programadores)
- Propósito: definir como a aplicação se comporta (idioma, fuso horário, banco de dados, segurança básica, etc.).
- Quem usa: desenvolvedores e administradores ao configurar ou implantar o site.

O que tem de mais relevante
- SECRET_KEY: é uma chave secreta usada pelo sistema para coisas internas (sessões, segurança). Nunca deve ser publicada na internet. Em projetos reais, colocamos essa chave em um local seguro (não em arquivos públicos).
- DEBUG: quando `True` a aplicação mostra mensagens detalhadas de erro — útil para desenvolvedores, mas perigoso em produção. Em um site público, isso deve ficar `False`.
- ALLOWED_HOSTS: lista de endereços que o site aceita. Serve para evitar que outras pessoas repliquem o site num endereço diferente. Aqui há valores para desenvolvimento local e algumas variações usadas por ambientes de preview.
- CSRF_TRUSTED_ORIGINS: origens confiáveis para formulários; importante para segurança de envios via navegador.

Idioma e fuso
- `LANGUAGE_CODE = "pt-br"` e `TIME_ZONE = "America/Sao_Paulo"`: o site está configurado para português do Brasil e horário de São Paulo. Isso faz com que datas e textos padrão apareçam em português.

Banco de dados
- Atualmente usa um arquivo SQLite (`db.sqlite3`). Esse é um banco simples, típico para desenvolvimento e testes. Em produção costuma-se usar bancos mais robustos (Postgres, MySQL).

Arquivos estáticos
- `STATIC_URL = "static/"` indica onde o site busca arquivos como CSS e JavaScript.

Internacionalização (traduções)
- `LOCALE_PATHS` aponta para onde traduções customizadas podem ficar. Isso permite adaptar textos do sistema para outros idiomas.

Por que essas alterações no arquivo foram feitas (resumo técnico leve)
- O projeto passou a mostrar conteúdo em português (`pt-br`) e usar o fuso de São Paulo.
- Foi adicionada a configuração de `locale` e foi registrado o aplicativo `rota` de forma mais explícita para que apareça com um nome legível no painel.

Riscos e cuidados
- Não compartilhar o valor de `SECRET_KEY`.
- Não deixar `DEBUG = True` em sites públicos.
- Alterar `ALLOWED_HOSTS` com cuidado; se algo ficar faltando o site pode recusar conexões.

Se você quiser pedir uma mudança
- Diga qual texto/idioma ou fuso quer alterar e se o site ficará público.
- Para trocar de banco (por exemplo, migrar para Postgres) fale com um desenvolvedor — é uma mudança maior.

Onde ver o efeito
- Mudar o idioma/tempo altera como datas e mensagens aparecem no site.
- Mudar `DEBUG` muda o que aparece quando há erro (mensagens detalhadas vs páginas amigáveis).

Perguntas frequentes (não técnicas)
- "Posso editar esse arquivo?": Melhor pedir ao time técnico; algumas mudanças são seguras (idioma), outras exigem cuidado (chave secreta, debug, banco).
- "Se eu remover algo, o site quebra?": Sim, mudanças indevidas podem impedir o site de funcionar.

---
Arquivo original: `core/settings.py`

