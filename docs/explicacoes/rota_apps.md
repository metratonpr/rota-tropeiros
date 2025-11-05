# Explicação didática: `rota/apps.py`

O arquivo `rota/apps.py` contém metadados simples sobre o aplicativo `rota`. Em Django, um "app" é uma parte do projeto que cuida de uma funcionalidade (neste caso, rotas e horários). Este arquivo diz ao sistema como identificar esse app.

Resumo rápido (não técnico)
- Propósito: fornecer um nome amigável para o aplicativo e definir um comportamento padrão.
- Quem usa: desenvolvedores e o painel administrativo (aparece como um título legível).

O que foi alterado
- `verbose_name = "Sistema de Rotas e Horários"`: isso é um rótulo mais amigável que aparece nas telas administrativas em vez do nome técnico "rota". Ajuda pessoas que não são programadoras a entenderem do que se trata.

Por que isso é útil
- Usabilidade: administradores e mantenedores veem nomes descritivos no painel, reduzindo confusão.

Riscos e cuidados
- Essa alteração é segura e não afeta os dados. Ela só muda como o app é exibido para quem administra o sistema.

Se quiser alterar
- Para mudar o rótulo, peça ao time técnico para editar esse arquivo. É uma mudança simples.

---
Arquivo original: `rota/apps.py`

