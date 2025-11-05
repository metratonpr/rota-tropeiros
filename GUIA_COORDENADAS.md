# 🚌 Guia de Uso - Viação Rota dos Tropeiros

## 📍 Como Adicionar Rotas com Coordenadas de Castro-PR

### 1. Obter Coordenadas (Latitude e Longitude)

Você pode obter as coordenadas de qualquer local em Castro usando:

#### Opção A: Google Maps
1. Acesse https://www.google.com/maps
2. Busque o local em Castro (ex: "Praça Getúlio Vargas, Castro")
3. Clique com botão direito no local
4. Clique em "Lat, Long" (copia automaticamente)
5. Formato: `-24.7911, -50.0119`

#### Opção B: OpenStreetMap
1. Acesse https://www.openstreetmap.org
2. Busque o local em Castro
3. Clique com botão direito → "Mostrar endereço"
4. As coordenadas aparecem na URL

### 2. Adicionar Paradas no Admin

1. Acesse: `http://localhost:8000/admin/rota/parada/add/`

2. Preencha os campos:
   - **Endereço**: Ex: "Terminal Rodoviário de Castro"
   - **Latitude e Longitude**: Use o formato `-24.7911,-50.0119`
     - ⚠️ **IMPORTANTE**: Sem espaços, apenas vírgula entre os números
     - ✅ Correto: `-24.7911,-50.0119`
     - ❌ Errado: `-24.7911, -50.0119` (tem espaço)
   - **Ativo**: Marcar como ativo

3. Clique em "Salvar"

### 3. Criar uma Rota

1. Acesse: `http://localhost:8000/admin/rota/rota/add/`

2. Preencha:
   - **Nome**: Ex: "Linha Centro-Bairro"
   - **Ativo**: Marcar como ativo

3. Na seção "Horários nas Paradas", clique em "Adicionar outro":
   - **Parada**: Selecione a parada criada
   - **Horário**: Ex: 07:00
   - **Ativo**: Marcar como ativo

4. Adicione todas as paradas da rota em ordem

5. Clique em "Salvar"

### 4. Verificar no Mapa

1. Acesse: `http://localhost:8000/`
2. Role até a seção "Mapa das rotas"
3. Clique na aba da linha criada
4. O mapa mostrará a rota com os pontos!

---

## 🗺️ Coordenadas de Referência em Castro-PR

### Pontos Centrais
- **Centro de Castro**: `-24.7911,-50.0119`
- **Praça Getúlio Vargas**: `-24.7908,-50.0122`
- **Rodoviária**: `-24.7895,-50.0105`

### Bairros (estimativa - verificar coordenadas reais)
- **Bairro Norte**: `-24.7850,-50.0100`
- **Bairro Sul**: `-24.7970,-50.0130`
- **Bairro Leste**: `-24.7900,-50.0050`
- **Bairro Oeste**: `-24.7920,-50.0180`

---

## 📋 Exemplo Completo: Linha Centro-Bairro

### Passo 1: Criar 3 Paradas

**Parada 1: Terminal Central**
- Endereço: `Terminal Rodoviário de Castro`
- Lat/Long: `-24.7895,-50.0105`
- Ativo: ✅

**Parada 2: Praça Central**
- Endereço: `Praça Getúlio Vargas`
- Lat/Long: `-24.7908,-50.0122`
- Ativo: ✅

**Parada 3: Bairro Residencial**
- Endereço: `Bairro São Francisco`
- Lat/Long: `-24.7850,-50.0100`
- Ativo: ✅

### Passo 2: Criar a Rota

**Rota: Linha 01 - Centro**
- Nome: `Linha 01 - Centro`
- Ativo: ✅

**Horários:**
1. Terminal Rodoviário - 06:00 - Ativo ✅
2. Praça Getúlio Vargas - 06:10 - Ativo ✅
3. Bairro São Francisco - 06:20 - Ativo ✅

### Resultado

Ao acessar a página inicial:
- A linha aparecerá nas tabs de horários
- Ao clicar na linha, o mapa mostrará:
  - Linha verde conectando os 3 pontos
  - Marcadores azuis nas paradas
  - Popups ao clicar nos marcadores

---

## 🔧 Solução de Problemas

### ❌ Mapa não mostra a rota

**Problema**: Formato incorreto das coordenadas

**Solução**: 
- Verifique se não há espaços: `-24.7911,-50.0119` ✅
- Verifique se a vírgula está correta
- Latitude negativa (sul do Equador)
- Longitude negativa (oeste de Greenwich)

### ❌ Coordenadas aparecem fora de Castro

**Problema**: Ordem invertida (longitude, latitude)

**Solução**:
- Formato correto: `LATITUDE,LONGITUDE`
- Exemplo: `-24.7911,-50.0119` (lat primeiro)
- Não: `-50.0119,-24.7911` (errado!)

### ❌ Mapa vazio

**Solução**:
1. Verifique se a rota está marcada como **Ativo**
2. Verifique se as paradas estão marcadas como **Ativo**
3. Verifique se os horários estão marcados como **Ativo**
4. Limpe o cache do navegador (Ctrl+F5)

---

## 🌐 API de Mapas Gratuita Utilizada

### OpenStreetMap
- **Custo**: Gratuito
- **Limite**: Ilimitado para uso razoável
- **Qualidade**: Excelente para cidades brasileiras
- **Documentação**: https://www.openstreetmap.org

### Alternativas (se necessário)

#### Mapbox (opção premium)
- Gratuito até 50.000 visualizações/mês
- Melhor performance
- https://www.mapbox.com

#### Google Maps API (requer chave)
- Gratuito até $200/mês em créditos
- Requer cartão de crédito
- https://developers.google.com/maps

---

## 💡 Dicas

### Como obter coordenadas precisas
1. Use Google Maps para maior precisão
2. Clique exatamente no ponto de parada de ônibus
3. Copie as coordenadas e cole no campo

### Organização de linhas
- Use nomes claros: "Linha 01 - Centro", "Linha 02 - Bairro"
- Ordene as paradas pela sequência da rota
- Use horários reais das partidas

### Testes
1. Sempre teste no mapa após criar uma rota
2. Verifique se os pontos estão corretos
3. Ajuste coordenadas se necessário

---

## 📞 Suporte

Problemas com o sistema? Verifique:
1. Logs do Django no terminal
2. Console do navegador (F12)
3. Arquivo `views.py` linha 130+ (coordenadas padrão)
4. Arquivo `route-map.js` (lógica do mapa)

---

**Última atualização**: Novembro 2025  
**Sistema**: Viação Rota dos Tropeiros v1.0
