# Know Your Fan

O **Know Your Fan** é uma aplicação desenvolvida com **Streamlit** voltada para o cadastro e gerenciamento de informações de fãs de eSports. Ela permite validar documentos, armazenar informações pessoais e de interesses, além de exibir a lista de fãs cadastrados.

## Funcionalidades

- **Cadastro de Fãs**: Insira dados pessoais, documentos e informações relacionadas a interesses em eSports.
- **Validação de Documentos**: Utilize **Tesseract OCR** para validar informações em documentos (PDF, JPG, PNG).
- **Listagem de Fãs Cadastrados**: Exiba os dados armazenados em um arquivo CSV.
- **Armazenamento Seguro**: Os dados são salvos localmente em um arquivo `dados_fas.csv`.

---

## **Aviso Importante**

⚠️ **Disclaimer**: Esta aplicação **não está completa**. Algumas funcionalidades planejadas ainda não foram implementadas ou estão com limitações:

1. **Validação de Documentos**: A validação de documentos com uso de IA é falha. Atualmente, o código utiliza ferramentas OCR como o Tesseract, mas mecanismos mais robustos de validação e leitura automática de informações ainda precisam ser aprimorados.
   
2. **Vinculação de Redes Sociais**: A funcionalidade de vincular redes sociais ao perfil do usuário, incluindo a leitura de interações, páginas seguidas e atividades relacionadas a organizações de eSports, como a FURIA, não está implementada. Isso ocorre devido a dificuldades técnicas na configuração das contas de desenvolvedor para as respectivas plataformas (Instagram, Twitter, TikTok).

---

## Pré-requisitos

Antes de rodar o projeto, certifique-se de que você possui os seguintes itens instalados:

- Python 3.9 ou superior.
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) e [Poppler](https://poppler.freedesktop.org/).
- Gerenciador de pacotes `pip`.
- [Streamlit](https://docs.streamlit.io/) para interface.

---

## Instalação

### Passo 1: Clonar o Repositório

Clone o repositório contendo o código do projeto:

```bash
git clone https://github.com/seu-usuario/know-your-fan.git
cd know-your-fan
```

### Passo 2: Criar Ambiente Virtual

Crie um ambiente virtual para isolar as dependências:

```bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate     # Windows
```

### Passo 3: Instalar Dependências

Instale as bibliotecas necessárias listadas no arquivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

Se o arquivo `requirements.txt` não existir, instale manualmente as bibliotecas utilizadas:

```bash
pip install streamlit opencv-python-headless numpy pandas pytesseract pillow pdf2image python-dotenv
```

### Passo 4: Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto e configure os caminhos para o Tesseract OCR e o Poppler, como no exemplo abaixo:

```
dir_tesseract=C:/Program Files/Tesseract-OCR/tesseract.exe
dir_poppler=C:/Program Files/poppler-xx/bin
```

> **Nota**: Ajuste os caminhos conforme a localização das ferramentas no seu sistema.

### Passo 5: Instalar Tesseract OCR e Poppler

#### Tesseract OCR

1. Faça o download e instale o [Tesseract OCR](https://github.com/tesseract-ocr/tesseract).
2. Certifique-se de adicionar o caminho para o executável do Tesseract no `.env`.

#### Poppler

1. Faça o download do [Poppler](https://poppler.freedesktop.org/).
2. Extraia os arquivos e adicione o caminho para o diretório `bin` no `.env`.

---

## Como Executar

1. Certifique-se de que o ambiente virtual está ativado.
2. Execute o script principal com o comando:

```bash
streamlit run app.py
```

3. O Streamlit abrirá o navegador padrão com a interface da aplicação.

---

## Estrutura do Projeto

```plaintext
.
├── app.py                 # Código principal da aplicação.
├── validador.py           # Funções para validação de CPF e links sociais.
├── .env                   # Arquivo de configuração de variáveis.
├── dados_fas.csv          # Dados cadastrados (gerado automaticamente).
├── requirements.txt       # Dependências do projeto.
└── README.md              # Documentação do projeto.
```

---

## Tecnologias Utilizadas

- **Streamlit**: Para criar a interface gráfica da aplicação.
- **Tesseract OCR**: Para reconhecimento de texto em imagens e PDFs.
- **OpenCV**: Para pré-processamento de imagens.
- **Pandas**: Para manipulação de dados em formato CSV.
- **dotenv**: Para gerenciamento de variáveis de ambiente.
- **PDF2Image**: Para converter PDFs em imagens.

---

## Possíveis Erros

### 1. `pytesseract.pytesseract.tesseract_cmd is not set`
- Certifique-se de que o caminho correto para o executável do Tesseract está configurado no `.env`.

### 2. `FileNotFoundError: Poppler is not installed`
- Certifique-se de que o Poppler está instalado e configurado corretamente no `.env`.

### 3. Problemas com Validação de CPF
- O CPF pode ser considerado inválido se o formato estiver incorreto. Utilize `validador.py` para verificar.

---

## Contribuições

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do repositório.
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`).
3. Faça commit das alterações (`git commit -m "Adiciona nova feature"`).
4. Faça um push para a branch (`git push origin feature/nova-feature`).
5. Abra um Pull Request.

---

## Licença

Este projeto é licenciado sob a [MIT License](LICENSE).