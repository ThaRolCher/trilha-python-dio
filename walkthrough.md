# Detalhes das Alterações - Rota de Diagnóstico e Sistema Bancário

## 1. Rota de Diagnóstico (FastAPI)

Adicionei a rota de diagnóstico solicitada (`/health`) aos dois arquivos principais do FastAPI no espaço de trabalho e verifiquei que todos os testes e a execução do código funcionam perfeitamente sem problemas.

### Alterações Realizadas

#### API dio-blog
Arquivo modificado: [main.py (dio-blog)](file:///c:/Users/Chericoni/DIO-python-backend-developer/trilha-python-dio/13%20-%20APIs%20Ass%C3%ADncronas%20com%20FastAPI/dio-blog/src/main.py#L80-L90):
Adicionada a rota `/health`:
```python
@app.get("/health", tags=["Diagnóstico"])
async def health_check():
    """Retorna o estado de funcionamento da API."""
    return {
        "status": "online",
        "ambiente": "desenvolvimento",
        "database_status": "conectado"
    }
```

Adicionado o arquivo de teste [test_health.py](file:///c:/Users/Chericoni/DIO-python-backend-developer/trilha-python-dio/13%20-%20APIs%20Ass%C3%ADncronas%20com%20FastAPI/dio-blog/tests/integration/test_health.py):
```python
from fastapi import status
from httpx import AsyncClient


async def test_health_check_success(client: AsyncClient):
    # Quando
    response = await client.get("/health")

    # Então
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "status": "online",
        "ambiente": "desenvolvimento",
        "database_status": "conectado"
    }
```

#### API desafio
Arquivo modificado: [main.py (desafio)](file:///c:/Users/Chericoni/DIO-python-backend-developer/trilha-python-dio/13%20-%20APIs%20Ass%C3%ADncronas%20com%20FastAPI/desafio/src/main.py#L70-L80):
Adicionada a mesma rota `/health`.

### Resultados da Verificação

1. **Testes Automatizados para a API dio-blog**:
   Executado o `pytest` na pasta `dio-blog`. Todos os 19 testes passaram com sucesso (incluindo o novo teste de integração do health check).
2. **Verificação Manual para a API desafio**:
   Executada uma verificação programática usando o cliente do FastAPI no ambiente virtual do `desafio` para validar o retorno do endpoint `/health`:
   ```
   ROUTE RESPONSE: {'status': 'online', 'ambiente': 'desenvolvimento', 'database_status': 'conectado'}
   ```

---

## 2. Desafio do Sistema Bancário em Python

Criei e configurei a nova subpasta com a implementação completa e profissional do sistema bancário interativo no terminal.

### Alterações Realizadas

- Criada a pasta: [DIO_python_AI_backend_developer](file:///c:/Users/Chericoni/DIO-python-backend-developer/trilha-python-dio/DIO_python_AI_backend_developer)
- Criado o arquivo de código-fonte: [sistema_bancario.py](file:///c:/Users/Chericoni/DIO-python-backend-developer/trilha-python-dio/DIO_python_AI_backend_developer/sistema_bancario.py) contendo tratamento de erros robusto para entradas não numéricas e fluxo lógico consolidado.
- Criado o arquivo de documentação técnica: [README.md](file:///c:/Users/Chericoni/DIO-python-backend-developer/trilha-python-dio/DIO_python_AI_backend_developer/README.md) descrevendo as regras de negócio, limites operacionais e instruções de uso.

### Resultados da Verificação

Foi executado um teste de integração de console automatizado via subprocesso no Python simulando as operações do menu:
- Aporte inicial (Depósito) de R$ 100.00: efetuado com sucesso.
- Retirada (Saque) de R$ 50.00: efetuada com sucesso.
- Geração de extrato detalhado: apresentou as duas transações formatadas e o saldo correto de R$ 50.00.
- Encerramento: encerrado sem nenhuma exceção.

---

## 3. Otimização do Sistema Bancário com Funções Python

Criei e configurei a nova pasta com a implementação refatorada do sistema bancário estruturada em funções com tipos específicos de argumentos.

### Alterações Realizadas

- Criada a pasta: [DIO - otimizando o sistema bancario com funções python](file:///c:/Users/Chericoni/DIO-python-backend-developer/trilha-python-dio/DIO%20-%20otimizando%20o%20sistema%20bancario%20com%20fun%C3%A7%C3%B5es%20python)
- Criado o arquivo de código-fonte: [sistema_bancario_otimizado.py](file:///c:/Users/Chericoni/DIO-python-backend-developer/trilha-python-dio/DIO%20-%20otimizando%20o%20sistema%20bancario%20com%20fun%C3%A7%C3%B5es%20python/sistema_bancario_otimizado.py) que refatora as operações em funções específicas com mapeamento rigoroso de parâmetros (*positional-only*, *keyword-only* e posicional/nomeado híbrido) e tratamento de erros de conversão numérica.
- Criado o arquivo de documentação técnica: [README.md](file:///c:/Users/Chericoni/DIO-python-backend-developer/trilha-python-dio/DIO%20-%20otimizando%20o%20sistema%20bancario%20com%20fun%C3%A7%C3%B5es%20python/README.md) explicando detalhadamente as novas assinaturas das funções, cadastros de clientes e contas.

### Resultados da Verificação

Foi executado um teste de integração de terminal automatizado simulando:
1. Cadastro de novo cliente (`Maria Silva`).
2. Criação de nova conta corrente associada a esse cliente.
3. Listagem de contas correntes cadastradas.
4. Depósito de R$ 200.00.
5. Saque de R$ 100.00.
6. Exibição do extrato e verificação do saldo de R$ 100.00.
7. Saída limpa do terminal.

O programa executou sem nenhuma falha, demonstrando total compatibilidade operacional.

---

## 4. Sistema Bancário em Programação Orientada a Objetos com Python

Criei e configurei a nova pasta com a implementação orientada a objetos (POO) estruturada a partir de um modelo de classes UML.

### Alterações Realizadas

- Criada a pasta: [Sistema Bancário em POO com Python](file:///c:/Users/Chericoni/DIO-python-backend-developer/trilha-python-dio/Sistema%20Banc%C3%A1rio%20em%20POO%20com%20Python)
- Criado o arquivo de código-fonte: [sistema_bancario_poo.py](file:///c:/Users/Chericoni/DIO-python-backend-developer/trilha-python-dio/Sistema%20Banc%C3%A1rio%20em%20POO%20com%20Python/sistema_bancario_poo.py) contendo a arquitetura UML implementada por classes (`Cliente`, `PessoaFisica`, `Conta`, `ContaCorrente`, `Historico`, `Transacao`, `Deposito`, `Saque`). Corrigido o formato de hora para suportar a plataforma Windows sem erros.
- Criado o arquivo de documentação técnica: [README.md](file:///c:/Users/Chericoni/DIO-python-backend-developer/trilha-python-dio/Sistema%20Banc%C3%A1rio%20em%20POO%20com%20Python/README.md) explicando a relação de herança e encapsulamento das classes no modelo bancário.

### Resultados da Verificação

Foi executado um teste de integração de terminal simulando as operações do menu:
1. Cadastro de novo cliente Pessoa Física (`Maria Silva`).
2. Abertura de Conta Corrente associada ao CPF cadastrado.
3. Listagem de contas correntes cadastradas.
4. Execução de um Depósito no valor de R$ 300.00 associando o depósito à classe correspondente.
5. Execução de um Saque no valor de R$ 100.00 validando limites de conta e saques na classe filha `ContaCorrente`.
6. Exibição do extrato e verificação de saldo final consolidado de R$ 200.00 com data/hora formatada no histórico.
7. Saída segura.

O programa funcionou perfeitamente em todas as interações.

---

## 5. Sistema Bancário em POO com Python e Datetime

Criei e configurei a nova pasta com a implementação orientada a objetos (POO) estendida com limites temporais e formatação de datas.

### Alterações Realizadas

- Criada a pasta: [sist_bancario_POO_python_datetime](file:///c:/Users/Chericoni/DIO-python-backend-developer/trilha-python-dio/sist_bancario_POO_python_datetime)
- Criado o arquivo de código-fonte: [sist_bancario_POO_python_datetime.py](file:///c:/Users/Chericoni/DIO-python-backend-developer/trilha-python-dio/sist_bancario_POO_python_datetime/sist_bancario_POO_python_datetime.py) contendo a validação de limite diário de 10 transações e contagem de saques diários.
- Criado o arquivo de documentação técnica: [README.md](file:///c:/Users/Chericoni/DIO-python-backend-developer/trilha-python-dio/sist_bancario_POO_python_datetime/README.md) detalhando as novas restrições operacionais e a modelagem UML adaptada.

### Resultados da Verificação

Foi executado um teste automatizado simulando:
1. Cadastro de novo cliente Pessoa Física (`João Teste`).
2. Criação de Conta Corrente associada.
3. Execução de 10 depósitos consecutivos com sucesso.
4. Tentativa de efetuar a 11ª transação, validando o bloqueio preventivo e a exibição da mensagem de erro de limite de transações diárias excedido.
5. Verificação do formato de data e hora (`dd-mm-aaaa hh:mm:ss`) em todas as transações registradas no histórico.
6. Validação do saldo final (R$ 1000.00).

O programa passou com sucesso em todas as verificações simuladas.

---

## 6. Sistema Bancário com Decoradores de Auditoria

Criei e configurei a nova pasta com a implementação estendida com decoradores de auditoria para persistência de logs em arquivo.

### Alterações Realizadas

- Criada a pasta: [sist_bancario_decoradores](file:///c:/Users/Chericoni/DIO-python-backend-developer/trilha-python-dio/sist_bancario_decoradores)
- Criado o arquivo de código-fonte: [sist_bancario_decoradores.py](file:///c:/Users/Chericoni/DIO-python-backend-developer/trilha-python-dio/sist_bancario_decoradores/sist_bancario_decoradores.py) implementando o decorador `@log_transacao` e `__repr__` nas classes `PessoaFisica` e `ContaCorrente`.
- Criado o arquivo de logs: [log.txt](file:///c:/Users/Chericoni/DIO-python-backend-developer/trilha-python-dio/sist_bancario_decoradores/log.txt) registrando eventos e auditoria em uma nova linha com data, hora, nome da função, argumentos e valores retornados.
- Criada a documentação técnica: [README.md](file:///c:/Users/Chericoni/DIO-python-backend-developer/trilha-python-dio/sist_bancario_decoradores/README.md) explicando a implementação de auditoria.

### Resultados da Verificação

Foi executado um teste automatizado simulando a criação de cliente/conta, depósitos, saques e verificação de logs:
1. Confirmada a gravação de logs de auditoria correspondentes para todas as funções interativas do sistema.
2. Validado o formato do timestamp `[AAAA-MM-DD HH:MM:SS]`.
3. Validado o formato de linha única em cada log, garantindo que representações complexas de objetos não quebrem a estrutura do arquivo.
4. Verificada a persistência em modo de acréscimo (append).

O programa passou com sucesso em todas as verificações simuladas.


