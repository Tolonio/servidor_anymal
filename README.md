# Anymal-Tradução
# Instalação
Ir para o Dowloads:

```
cd Downloads/
```

Clonar o repositório:

```
git clone https://github.com/Tolonio/Anymal-Tradu-o.git
``` 

Garantir que existe a pasta no anymal:

```
ssh integration@anymal-<nomedoanymal>-npc "mkdir -p /home/integration/servidor_anymal"
```

Use o scp -r para clonar todo os arquivos do git para o anymal:

```
scp -r ./Anymal-Tradu-o/* integration@anymal-<nomedoanymal>-npc:/home/integration/servidor_anymal
```

Acessar o ssh do anymal:

```
ssh integration@anymal-<nomedoanymal>-npc
```


Dentro do anymal navegue:

```
cd /home/integration/servidor_anymal
```

Rode o comando para criar o ambiente virtual:
```
python3 -m venv venv
```

Ativar o ambiente virtual:

```
source venv/bin/activate
```

Rode:
```
sudo apt update

sudo apt install -y \
    libcairo2 \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libgdk-pixbuf-2.0-0 \
    shared-mime-info
```

Instale:
```
python3 -m pip install flask deep-translator lxml weasyprint

```

Rode:
```
cd codigos\para\o\anymal/:
```

Inicie o servidor:
```
python3 servidor_web.py
```

Criar o serviço:

```
sudo nano /etc/systemd/system/servidor_anymal.service
```

Cole:

```
[Unit]
Description=Servidor Web do Tradutor ANYmal
After=network.target

[Service]
Type=simple

User=integration
Group=integration

WorkingDirectory=/home/integration/servidor_anymal

Environment="PATH=/home/integration/servidor_anymal/venv/bin"
Environment="PYTHONUNBUFFERED=1"

ExecStart=/home/integration/servidor_anymal/venv/bin/python3 /home/integration/servidor_anymal/servidor_web.py

Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```


Reinicie o serviço:

```
sudo systemctl daemon-reload
```

Rode o enable do serviço:

```
sudo systemctl enable servidor_anymal.service
```


Rodê o start do serviço:

```
sudo systemctl start servidor_anymal.service
```

Isso é opcional para ver o status do serviço:

```
sudo systemctl status servidor_anymal.service

```
