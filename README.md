# CCTV Alert Server

Servidor WebSocket para detecção de pessoas em tempo real usando YOLO e OpenCV.

## 🖥️ Sobre o Projeto

Este servidor faz parte de um Trabalho de Conclusão de Curso (TCC) e tem como objetivo detectar pessoas em câmeras CCTV usando modelos YOLO, enviando alertas em tempo real via WebSocket para aplicações cliente.

## ✨ Funcionalidades

- 🤖 **Detecção de Pessoas**: Usando modelos YOLO (YOLOv8, YOLO11, YOLO12)
- 📹 **Multi-câmeras**: Suporte para múltiplas câmeras simultaneamente
- 🌐 **WebSocket**: Comunicação em tempo real com clientes
- 📊 **API REST**: Endpoint para listar câmeras disponíveis
- 🔍 **Filtro Visão Noturna**: Processamento opcional para ambientes escuros
- 📷 **Captura Base64**: Imagens codificadas para transmissão via JSON

## 🛠️ Tecnologias Utilizadas

- **FastAPI** - Framework web moderno e rápido
- **WebSocket** - Comunicação em tempo real
- **YOLO (Ultralytics)** - Detecção de objetos em tempo real
- **OpenCV** - Processamento de imagens e vídeo
- **Uvicorn** - Servidor ASGI de alta performance

## 📋 Pré-requisitos

- Python 3.8 ou superior
- Câmeras conectadas ao sistema (USB/IP)
- Modelos YOLO (.pt files)

## 🚀 Instalação

1. Clone o repositório:
```bash
git clone <url-do-repositorio>
cd Servidor
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute o servidor:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## ⚙️ Configuração

### Câmeras Disponíveis
Edite o arquivo `app/main.py` para configurar as câmeras:
```python
camera_ids = [0, 1]  # IDs das câmeras (0=webcam, 1=câmera USB, etc.)
```

### Modelos YOLO
O servidor suporta diferentes modelos YOLO:
- `yolov8n.pt` - Mais rápido, menor precisão
- `yolo11m.pt` - Balanceado
- `yolo12s.pt` - Mais preciso (padrão)

Altere em `app/yolo_service.py`:
```python
self.model = YOLO("yolo12s.pt")  # Escolha o modelo
```

### Limiar de Confiança
Ajuste a sensibilidade da detecção em `app/yolo_service.py`:
```python
confidence_threshold = 0.5  # 0.0 a 1.0 (mais alto = mais restritivo)
```

## 🏗️ Estrutura do Projeto

```
app/
├── main.py              # Servidor FastAPI e rotas
├── websocket_handler.py # Gerenciamento de conexões WebSocket
└── yolo_service.py      # Serviço de detecção YOLO
requirements.txt         # Dependências Python
*.pt                     # Modelos YOLO
```

## 📡 API Endpoints

### REST API
- `GET /cameras` - Lista câmeras disponíveis

### WebSocket
- `ws://localhost:8000/ws/{camera_id}` - Conexão para câmera específica

## 📊 Protocolo de Comunicação

### Mensagem de Conexão (enviada ao conectar):
```json
{
  "type": "connection",
  "camera": "0",
  "status": "connected",
  "message": "Câmera 0 conectada com sucesso"
}
```

### Mensagem de Detecção (enviada quando pessoa é detectada):
```json
{
  "type": "detection",
  "date": "12/01/2025",
  "time": "14:30:25",
  "timezone": "UTC-03:00",
  "image_base64": "data:image/jpeg;base64,/9j/4AAQSkZJRgABA...",
  "camera": "0"
}
```

## 🔧 Funcionalidades Avançadas

### Visão Noturna
Para ativar o filtro de visão noturna, descomente em `yolo_service.py`:
```python
# Descomente esta linha:
frame = self.apply_night_vision_filter(frame)
```

### Logs
O servidor gera logs detalhados sobre:
- Conexões de clientes
- Detecções de pessoas
- Erros de câmera
- Performance do YOLO

## 🚀 Execução

```bash
# Desenvolvimento (com reload automático)
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Produção
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 📝 Logs de Exemplo

```
INFO: Novo cliente conectado na câmera 0 via WebSocket
INFO: YOLO rodou sobre o frame da câmera 0.
INFO: Câmera 0: Pessoa detectada! Coordenadas: [245 123 456 789]
INFO: Câmera 0: Pessoa detectada. Enviando snapshot...
```

## 🔍 Troubleshooting

### Câmera não encontrada
- Verifique se a câmera está conectada
- Teste diferentes IDs (0, 1, 2...)
- Verifique permissões de acesso à câmera

### Modelo YOLO não carrega
- Verifique se o arquivo .pt existe
- Baixe modelos do [Ultralytics](https://github.com/ultralytics/ultralytics)

### Performance baixa
- Use modelo mais leve (yolov8n.pt)
- Reduza resolução da câmera
- Ajuste confidence_threshold

## 👨‍💻 Autor

Desenvolvido por Ricardo Andrade.