# Gamings API

Aplicação web para buscar e filtrar jogos gratuitos usando a FreeToGame API.

## Funcionalidades

- Busca de jogos por gênero com resultados em tempo real
- Dropdown com todos os gêneros disponíveis
- Busca personalizada por nome de jogo
- Interface responsiva e moderna

## Tecnologias

- Python + Streamlit (interface web)
- FreeToGame API
- Requests

## Instalação

```bash
git clone https://github.com/httpkmile/APIGamings-.git
cd APIGamings
pip install -r requirements.txt
streamlit run app.py
```

## Como Usar

1. Selecione um gênero no dropdown ou digite um gênero personalizado
2. Digite um nome de jogo para busca específica (opcional)
3. Os resultados aparecem automaticamente ao digitar

## API Endpoints

- `https://www.freetogame.com/api/games` - Todos os jogos
- `https://www.freetogame.com/api/games?genre={genre}&id={id}` - Busca filtrada

---

**Nota**: Requer conexão com internet para acessar a FreeToGame API.
