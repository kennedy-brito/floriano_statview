# 📊 Floriano StatView

Aplicação web desenvolvida com **Dash** e **Flask**, servida com **Gunicorn**, para visualização de dados estatísticos do município de Floriano-PI.

---

## 🚀 Requisitos

- Python 3.8 ou superior
- pip
- Virtualenv (opcional, mas recomendado)

---

## 📦 Instalação

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/floriano-statview.git
cd floriano-statview

# 2. Crie um ambiente virtual (opcional)
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# .\venv\Scripts\activate  # Windows

# 3. Instale as dependências
pip install -r requirements.txt
```

---

### Execução com Gunicorn:

```bash
gunicorn --workers 4 --bind 0.0.0.0:8050 run:app
```

- Acesse em `localhost`
---

## 🧠 Dicas

- Use `.env` com `python-dotenv` para variáveis sensíveis.
- Para deploy real, use Gunicorn + Nginx.
- Estilize sua aplicação com o conteúdo da pasta `assets`.

