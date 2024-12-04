# Sistema de Sequenciador Móvel

Instalação e Execução
Requisitos
Python 3.8 ou superior.
Bibliotecas necessárias:
tkinter

## Descrição

O **Sistema de Sequenciador Móvel** organiza a transmissão de mensagens de clientes a receptores utilizando um **grupo sequenciador** responsável por garantir a ordem de entrega. Este projeto implementa um sistema distribuído baseado no modelo de anel lógico, com suporte a falhas e ordem de entrega garantida por tokens.

---

## Funcionamento

### Grupos do Sistema

1. **Grupo Sequenciador (S1, S2, S3)**  
   - **Composição**:  
     Formado por processos organizados em um anel lógico.  
     Apenas o sequenciador com o token pode repassar mensagens para o grupo receptor.

   - **Funções**:  
     - **Recepção**: Todos os sequenciadores recebem mensagens do grupo emissor.  
     - **Encaminhamento**: Apenas o detentor do token repassa as mensagens aos receptores.  
     - **Continuidade**: Caso o sequenciador falhe, o token é transferido para o próximo membro.

2. **Grupo Emissor (C1, C2, C3)**  
   - **Composição**:  
     Um conjunto de clientes que enviam mensagens para o grupo sequenciador.  
   - **Funções**:  
     Cada cliente pode enviar várias mensagens, que são processadas pelo sequenciador.

3. **Grupo Receptor (R1, R2, R3)**  
   - **Composição**:  
     Um conjunto de receptores que recebem mensagens na ordem garantida pelo sequenciador.  
   - **Funções**:  
     As mensagens são entregues de acordo com a ordem definida pelo token.

---

### Fluxo do Sistema

1. **Envio de Mensagens**:
   - Clientes enviam mensagens ao grupo sequenciador.  
   - A ordem de entrega é definida por tokens aleatórios gerados para cada cliente.

2. **Processamento**:
   - O sequenciador que possui o token organiza as mensagens e as envia aos receptores.

3. **Ordem Aleatória**:
   - Respeita regras específicas, garantindo que cada cliente tenha um token aleatório para suas mensagens.

4. **Exemplo de Execução**:
   - Cliente 1 envia \(M1, M2\) com ordem \(1, 2\).  
   - Cliente 2 envia \(M3, M4\) com ordem \(3, 4\).  
   - Cliente 3 envia \(M5, M6\) com ordem \(5, 6\).  

   No receptor, as mensagens são entregues como:  
   \[
   M1 -> M2 -> M3 -> M4 -> M6 -> M5
   \]

---

## Requisitos

### Funcionais

1. **Cliente**:
   - Geração e envio de mensagens para o grupo sequenciador.  
   - Respeito à ordem de entrega definida por tokens aleatórios.

2. **Sequenciador**:
   - Garantia de ordem total para entrega das mensagens.  
   - Redundância em caso de falhas, com troca de token.

3. **Receptor**:
   - Recebimento de mensagens de todos os clientes na ordem definida pelo sequenciador.

---

## Implementação

### Código Principal (`sequenciador_movel.py`)

Inclui:
- Lógica para geração de tokens aleatórios.
- Simulação da troca de mensagens entre clientes, sequenciadores e receptores.
- Interface em Tkinter para exibição dinâmica das tabelas de mensagens.

### Trechos de Código

#### Exemplo: Geração de Tokens Aleatórios
```python
for cliente in clientes:
    quantidade_mensagens = mensagens_por_cliente
    ordem_cliente = list(range(ordem_atual, ordem_atual + quantidade_mensagens))
    random.shuffle(ordem_cliente)  # Permutação aleatória
    ordem_aleatoria[cliente] = ordem_cliente
    ordem_atual += quantidade_mensagens
