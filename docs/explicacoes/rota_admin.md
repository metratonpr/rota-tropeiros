# Explicação didática: `rota/admin.py`

O arquivo `rota/admin.py` define como a equipe administrativa (os gestores do site) vê e gerencia dados através da interface de administração do Django. Pense nele como as configurações da tela de administração: quais colunas aparecem, ações rápidas e títulos.

Resumo rápido (não técnico)
- Propósito: melhorar a experiência de quem administra o conteúdo (por exemplo, adicionar rotas, paradas, horários).
- Quem usa: funcionários autorizados (pessoas com acesso administrativo), não visitantes do site.

O que você verá ao acessar a administração
- Cabeçalhos e títulos: o painel foi personalizado para mostrar nomes em Português (por exemplo, "Viação Rota dos Tropeiros - Administração").
- Ações rápidas: existem botões para "Marcar como ativo" e "Marcar como inativo" — isso permite ativar/desativar registros em massa (por exemplo, ocultar temporariamente uma parada).
- Informações listadas: ao ver uma rota ou uma parada, o painel mostra colunas úteis (como nome, endereço, se está ativa e a quantidade de horários).

Exemplo prático (sem termos técnicos)
- Imagine que uma parada está temporariamente fechada. Um administrador pode selecionar essa parada na lista e escolher "Marcar como inativo"; assim a parada deixa de aparecer onde o site mostra apenas locais ativos.

Elementos úteis para administradores
- Inlines (linhas incorporadas): quando estiver editando uma rota, você consegue ver e editar os horários daquela rota diretamente na mesma página — isso torna a manutenção mais rápida.
- Pesquisa e filtros: existem campos de busca e filtros (por exemplo, por endereço ou por ativo/inativo) para encontrar registros rapidamente.

Segurança e boas práticas
- Somente pessoas de confiança devem ter acesso à administração. Se alguém desconhecido acessar esse painel, pode modificar ou excluir informações importantes.
- Antes de fazer alterações em massa (muitos itens ao mesmo tempo), confirme com a equipe, pois ações são aplicadas a todos os itens selecionados.

Se algo não aparecer como esperado
- Verifique se você está logado com uma conta administrativa.
- Para mudanças mais profundas na forma como os dados aparecem, peça ao time técnico (essas mudanças exigem editar o código).

Onde olhar no site
- Esse arquivo não afeta o que os visitantes veem no site público; afeta somente a área administrativa.

---
Arquivo original: `rota/admin.py`

