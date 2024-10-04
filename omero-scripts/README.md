# Ambiente de desenvolvimento de funcionalidades OMERO LNBio

## Requisitos
- Git
- Python
- omero-py

## Criação do ambiente
- Utilizando gerenciadores de ambiente (conda, mamba, micromamba) crie o ambiente onde irá instalar as dependências para instalar o OMERO e verificar se Python está executando  
- Bibliotecas externas do ZeroC são necessárias para executar o OMERO  

   - Windows: https://github.com/glencoesoftware/zeroc-ice-py-linux-x86_64/releases/download/20240202/zeroc_ice-3.6.5-cp310-cp310-manylinux_2_28_x86_64.whl
   - Linux: https://github.com/glencoesoftware/zeroc-ice-py-linux-x86_64/releases/download/20240202/zeroc_ice-3.6.5-cp310-cp310-manylinux_2_28_x86_64.whl

```sh
> micromamba create -n myenv python=3.10
> micromamba activate myenv
> python -V
Python 3.10.14
> pip install https://github.com/glencoesoftware/zeroc-ice-py-win-x86_64/releases/download/20240325/zeroc_ice-3.6.5-cp310-cp310-win_amd64.whl
> pip install omero-py
```

## Acesso ao OMERO CLI
```sh
(myenv)> omero
omero> login
Server: omero-server.org
Username: user.name
Password:
Created session for user.name@omero-server.org:4064. Idle timeout: 10 min. Current group: GROUP_A
```

## Desenvolvimento de scripts
O cliente OMERO.insight e OMERO.web podem executar scripts desenvolvidos utilizando o pacote `omero-py` que foi instalado é possível desenvolver e testar novos scripts de forma interativa na máquina local.

- Crie um arquivo `Ping_Pong.py` com o código abaixo

```python
# Ping_Pong.py
from omero import scripts
from omero.gateway import BlitzGateway
from omero.rtypes import rlong, rstring

def run_script():
    dataTypes = [rstring('Long')]

    client = scripts.client(
      "PingPong.py", "Simple ping script",
        
      scripts.Long(
          "A", optional=False, grouping="1",
          description="Choose source of images (only Plate supported)",
          values=dataTypes),

      scripts.String(
          "B", optional=False, grouping="2",
          description="List of Plates IDs to process.")
    )
    
    keys = client.getInputKeys()
    print("Keys found:")
    print(keys)
    for key in keys:
        client.setOutput(key, client.getInput(key))

    try:
        conn = BlitzGateway(client_obj=client)
        print("Sucess")
        client.setOutput("Message", rstring("Success"))

    finally:
        print("End session")
        client.closeSession()

if __name__ == "__main__":
    run_script()
```

- Executando todos os passos anteriores de acesso ao OMERO, o script desenvolvido pode ser testado usando a linha de comando

```
(myenv)> omero script run C:\\path\\to\\Ping_Pong.py
Enter value for "A": 10
Enter value for "B": 20
Keys found:
['A', 'B'] 
Sucess     
End session
```

- Assim que concluído o desenvolvimento, carregue o script para o servidor do omero
```
(myenv)> omero script upload --official Ping_Pong.py
```
