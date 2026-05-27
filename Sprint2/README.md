# ⚡ ChargeGrid Intelligence — Simulador de Load Balancing

> **EV Challenge 2026 | FIAP × GoodWe | Sprint 2 — Pensamento Computacional e Automação com Python**

---

## 👥 Integrantes

| Nome | RM |
|---|---|
| Arthur Micarelli Domingos | 571476 |
| Enzo Yudi de Oliveira Hino | 570173 |
| Felipe Elze da Silva | 572024 |
| Henrique Eduardo da Silva | 571803 |
| Inaldo Pereira Freitas | 569672 |

---

## 🔍 Problema

Eletropostos comerciais com múltiplos carregadores enfrentam um problema crítico: quando vários veículos estão conectados simultaneamente, a soma da potência solicitada pode ultrapassar o limite de energia contratado com a distribuidora. Sem um sistema de controle, isso gera:

- Multas por excesso de demanda contratada
- Risco de queda de energia no estabelecimento
- Interrupção abrupta do carregamento dos veículos
- Experiência negativa para o usuário final

> **Problema central:** Como distribuir a energia disponível de forma inteligente entre múltiplos carregadores, garantindo que todos os veículos carreguem simultaneamente sem ultrapassar o limite contratado?

---

## 💡 Justificativa

A Sprint 1 demonstrou, em Assembly x86, como registrar o consumo de energia por sessão com o menor custo computacional possível. A Sprint 2 evolui para o próximo nível: **o que fazer com essa energia quando ela é limitada?**

O algoritmo de **Dynamic Load Management (DLM)** resolve exatamente isso — e Python é a linguagem ideal para prototipá-lo porque:

- Permite simular lógica complexa de forma rápida e legível
- Facilita testes com múltiplos carregadores em tempo real
- Serve como base para futura integração com APIs e dashboards
- É amplamente usada em sistemas SCADA e automação industrial

| | Sprint 1 | Sprint 2 |
|---|---|---|
| Linguagem | Assembly x86 | Python 3 |
| Foco | Registro de kWh por sessão | Distribuição inteligente de energia |
| Entrega | Firmware embarcado | Simulador de Load Balancing |
| Evolução | Base de medição | Algoritmo de controle de demanda |

---

## 🛠️ Proposta de Solução

Simulador em Python que implementa o algoritmo de **Dynamic Load Management (DLM)**, redistribuindo automaticamente a energia disponível entre os carregadores ativos quando a demanda ultrapassa o limite contratado.

| Etapa | O que faz | Função principal |
|---|---|---|
| 1 — Monitorar | Soma a potência de todos os carregadores ativos | `calculate_total()` |
| 2 — Detectar | Compara o total com o limite contratado | `if total > power_limit_kw` |
| 3 — Balancear | Divide o limite igualmente entre os ativos | `apply_load_balancing()` |
| 4 — Simular | Carros chegam e saem aleatoriamente a cada ciclo | `for cycle in range(10)` |

---

## 🖥️ Arquitetura do Sistema

```
chargegrid.py
│
├── POWER_LIMIT_KW              → limite de energia do estabelecimento (100 kW)
├── chargers[]                  → lista de carregadores com id, potência e status
│
├── calculate_total(chargers)
│     └── soma power de todos os carregadores com active = True
│
├── apply_load_balancing(chargers, limit)
│     ├── filtra os carregadores ativos com .append()
│     ├── calcula power_per_charger = limit / active_count
│     └── atribui c["allocated"] para cada carregador
│
└── for cycle in range(10)
      ├── sorteia um carregador aleatório com random.choice()
      ├── inverte o estado com not (carro chega ou sai)
      ├── chama calculate_total()
      ├── chama apply_load_balancing() se necessário
      └── imprime o status de todos os carregadores
```

### Como funciona o algoritmo de Load Balancing

```
Total solicitado = soma de power de todos os carregadores com active = True

Se total > limite contratado:
    power_per_charger = limite / quantidade de ativos
    cada ativo recebe power_per_charger como "allocated"
    cada inativo recebe allocated = 0

Se total <= limite contratado:
    cada ativo recebe o próprio power como "allocated"
    cada inativo recebe allocated = 0
```

**Exemplo real com 7 carregadores:**

| Situação | Total solicitado | Limite | Ação |
|---|---|---|---|
| 6 carregadores ativos | 110 kW | 100 kW | Load Balancing → 16.67 kW cada |
| 4 carregadores ativos | 77 kW | 100 kW | Operação normal → cada um recebe seu power |

---

## 💻 Código Python — Trecho Principal

```python
def apply_load_balancing(chargers, power_limit_kw):
    active_chargers = []

    # filtra apenas os carregadores com carro conectado
    for c in chargers:
        if c["active"]:
            active_chargers.append(c)

    active_count = len(active_chargers)
    power_per_charger = power_limit_kw / active_count  # divide igualmente

    for c in chargers:
        if c["active"]:
            c["allocated"] = round(power_per_charger, 2)  # atribui a cota
        else:
            c["allocated"] = 0  # inativo não recebe energia

    return chargers
```

---

## ▶️ Como Rodar

### Pré-requisitos

- Python 3.8 ou superior instalado
- Nenhuma biblioteca externa necessária

### Instalação

```bash
# Clone o repositório
git clone https://github.com/1CCPWChallangeEquipe2/Pensamento-Computacional-e-Automacaoo-com-Python.git

# Acesse a pasta
cd Pensamento-Computacional-e-Automacaoo-com-Python
```

### Execução

```bash
python chargegrid.py
```

### Saída esperada

```
⏱️  Ciclo 1
🚗 C5 — carro conectou!
  C1 → 🔋 charging | allocated: 16.67 kW
  C2 → 🔋 charging | allocated: 16.67 kW
  C3 → 🔋 charging | allocated: 16.67 kW
  C4 → 🔋 charging | allocated: 16.67 kW
  C5 → 🔋 charging | allocated: 16.67 kW
  C6 → 🔋 charging | allocated: 16.67 kW
  C7 → ⚪ empty    | allocated:  0.00 kW
  Total: 117 kW / 100 kW

⏱️  Ciclo 2
🚙 C3 — carro saiu!
  C1 → 🔋 charging | allocated: 22.00 kW
  C2 → 🔋 charging | allocated: 22.00 kW
  C3 → ⚪ empty    | allocated:  0.00 kW
  C4 → 🔋 charging | allocated: 22.00 kW
  C5 → 🔋 charging | allocated:  7.00 kW
  C6 → 🔋 charging | allocated: 22.00 kW
  C7 → ⚪ empty    | allocated:  0.00 kW
  Total: 95 kW / 100 kW
```

---

## 📈 Impactos Esperados

- **Eliminação de multas** por excesso de demanda contratada
- **Todos os veículos carregam simultaneamente** — sem interrupção
- **Redistribuição automática** a cada ciclo conforme carros chegam e saem
- **Base para smart charging** — algoritmo pode ser evoluído com priorização solar, tarifação dinâmica e integração OCPP
- **Protótipo escalável** — testado com 7 carregadores, arquitetura suporta N carregadores

---

## 🌱 Relação com Sustentabilidade e Energias Renováveis

- O Load Balancing evita o desperdício de energia por desconexão forçada de carregadores
- Com o consumo controlado por sessão (Sprint 1) e a distribuição inteligente (Sprint 2), o sistema sabe **quanto de energia renovável foi entregue por veículo**
- Integrado ao inversor GoodWe, o algoritmo pode **priorizar carregadores quando há excedente solar** — reduzindo o uso da rede elétrica convencional
- Menos picos de demanda → menor necessidade de geração termelétrica de ponta → **menos CO₂**

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Uso |
|---|---|
| Python 3 | Linguagem principal |
| `random` | Simulação de carros chegando e saindo aleatoriamente |
| `time` | Intervalo de 2 segundos entre ciclos para simular tempo real |

---

## 📁 Arquivos do Repositório

```
Pensamento-Computacional-e-Automacaoo-com-Python/
├── chargegrid.py              # Simulador de Load Balancing — Sprint 2
├── ChargeGrid_Intelligence.pdf # Documentação técnica — Sprint 1
├── video.txt                  # Link do vídeo pitch — Sprint 1
└── README.md                  # Este documento
```

---

*ChargeGrid Intelligence — EV Challenge 2026 | FIAP × GoodWe | Sprint 2*
