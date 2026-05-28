# Sistema Bancário com Decoradores de Auditoria em Python

Este projeto estende o sistema bancário orientado a objetos (POO) integrado com controle de data e hora, adicionando uma camada de rastreamento de ações e auditoria de segurança. Isso é realizado por meio da implementação de um decorador de funções que intercepta e persiste o histórico de execução no sistema de arquivos.

---

## Funcionalidades de Auditoria

### 1. Interceptador de Execução (Decorador)
Foi desenvolvido o decorador `@log_transacao`, encarregado de capturar de forma transparente metadados cruciais da execução de qualquer funcionalidade operacional associada no menu do console.

### 2. Metadados Gravados no Log
Cada entrada gerada no arquivo de log do sistema de auditoria documenta:
- **Carimbo de Data e Hora**: O momento preciso da chamada da função no padrão `AAAA-MM-DD HH:MM:SS`.
- **Nome da Função**: O identificador interno da rotina executada (ex: `depositar`, `sacar`, `criar_cliente`, `criar_conta`).
- **Argumentos de Entrada**: Parâmetros posicionais (`args`) e nomeados (`kwargs`) encaminhados à função. Para objetos complexos (clientes e contas), são utilizadas as representações textuais especializadas de forma a tornar o log inteligível.
- **Retorno da Função**: O valor devolvido pela função após a conclusão de sua execução.

### 3. Persistência de Dados
- **Arquivo de Log**: Todas as chamadas decoradas são gravadas no arquivo fisicamente denominado `log.txt`, localizado no mesmo diretório do arquivo executável.
- **Gravação Incremental (Append)**: Se o arquivo `log.txt` já existir na máquina, os novos logs são anexados ao final dele, garantindo a integridade dos dados históricos gravados anteriormente.
- **Formatação de Linha**: Cada entrada de log é gravada em uma nova linha, mantendo a estrutura clara para análise e backups contínuos.

---

## Detalhes Conceituais de Implementação

### 1. Decorador `@log_transacao`
Implementado utilizando uma função invólucro (*wrapper*) que envolve a execução da função de destino. O decorador captura o estado antes, durante e após a execução do bloco:
```python
def log_transacao(func):
    def envelope(*args, **kwargs):
        resultado = func(*args, **kwargs)
        data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(ROOT_PATH / "log.txt", "a", encoding="utf-8") as arquivo:
            arquivo.write(
                f"[{data_hora}] Função '{func.__name__}' executada com argumentos {args} e {kwargs}. "
                f"Retornou {resultado}\n"
            )
        return resultado
    return envelope
```

### 2. Sobrescrita de Representações Textuais (`__repr__`)
Para evitar logs poluídos com endereços de memória dos objetos complexos (como `<__main__.PessoaFisica object at 0x...>`), as seguintes representações foram definidas:
- **`PessoaFisica`**: Retorna `<PessoaFisica: ('Nome', 'CPF')>`.
- **`ContaCorrente`**: Retorna `<ContaCorrente: ('Agência', 'Número', 'Nome do Titular')>`.

---

## Estrutura de Diretórios

```
sist_bancario_decoradores/
├── README.md                      # Documentação técnica e instruções
├── log.txt                        # Arquivo de persistência gerado automaticamente
└── sist_bancario_decoradores.py    # Script principal contendo o sistema e o decorador
```

---

## Instruções de Execução

### Pré-requisitos
- Interpretador Python 3.10 ou superior.

### Execução do Script

1. Abra seu terminal de comandos.
2. Navegue até o diretório correspondente:
   ```bash
   cd "trilha-python-dio/sist_bancario_decoradores"
   ```
3. Inicie o sistema bancário interativo:
   ```bash
   python sist_bancario_decoradores.py
   ```

### Auditoria e Leitura de Logs

Após realizar operações de cadastro ou movimentação no terminal:
1. Abra o arquivo `log.txt` gerado automaticamente na mesma pasta.
2. Verifique os registros cronológicos inseridos, assegurando-se de que cada ação reflete a data/hora, a assinatura da função correspondente, os argumentos passados e os objetos retornados.
