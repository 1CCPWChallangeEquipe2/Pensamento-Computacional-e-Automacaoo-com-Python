import time
import random


# LIMITE DE ENERGIA DO ESTABELECIMEN
power_limit_kw = 100

# LISTA DE CARREGADORES
# o active se for "true" é porque o carro está plugado no carregador e ao contrário é false e não está plugado
chargers = [
    {"id": "C1", "power": 22, "active": True},
    {"id": "C2", "power": 22, "active": True},
    {"id": "C3", "power": 11, "active": True},
    {"id": "C4", "power": 22, "active": True},
    {"id": "C5", "power": 7,  "active": False},
    {"id": "C6", "power": 22, "active": True},
    {"id": "C7", "power": 11, "active": True},
]


# CALCULANDO O TOTAL PEDIDO
def calculate_total(chargers):
    total_requested = 0
    for c in chargers:
        if c["active"]:
            total_requested += c["power"]
    return total_requested

# APLICA O LOADING BALANCE
def apply_load_balancing(chargers, power_limit_kw):
 active_chargers = []

 for c in chargers:
     if c["active"]:
         active_chargers.append(c)

 active_count = len(active_chargers)
 power_per_charger = power_limit_kw / active_count
 for c in chargers:
     if c["active"]:
         c["allocated"] = power_per_charger
     else:
         c["allocated"] = 0
 return chargers

# SIMULAÇÃO AO VIVO
for cycle in range(10):
    print(f"\n⏱️  Ciclo {cycle + 1}")

    random_charger = random.choice(chargers)
    random_charger["active"] = not random_charger["active"]

    if random_charger["active"]:
        print(f"🚗 {random_charger['id']} — carro conectou!")
    else:
        print(f"🚙 {random_charger['id']} — carro saiu!")

    total_requested = calculate_total(chargers)

    if total_requested > power_limit_kw:
        chargers = apply_load_balancing(chargers, power_limit_kw)

    for c in chargers:
        if c["active"]:
            status = "🔋 charging"
        else:
            status = "⚪ empty"
        print(f"  {c['id']} → {status} | allocated: {c.get('allocated', c['power']):.2f} kW")

        if total_requested > power_limit_kw:
            chargers = apply_load_balancing(chargers, power_limit_kw)
        else:
            for c in chargers:
                if c["active"]:
                    c["allocated"] = c["power"]
                else:
                    c["allocated"] = 0

    print(f"  Total: {total_requested} kW / {power_limit_kw} kW")
    time.sleep(2)



# RESULTADO
print("=== ChargeGrid Intelligence ===")
print(f"Limite de potências: {power_limit_kw} kW")
total_requested = calculate_total(chargers)
print(f"Total solicitado  : {total_requested} kW")


if total_requested > power_limit_kw:
    print("⚠️  ALERTA: Demanda acima do limite! Balanceamento de carga necessário.")
else:
    print("✅  Dentro dos limites. Tudo bem.")

if total_requested > power_limit_kw:
    chargers = apply_load_balancing(chargers, power_limit_kw)
else:
    for c in chargers:
        if c["active"]:
            c["allocated"] = c["power"]
        else:
            c["allocated"] = 0
