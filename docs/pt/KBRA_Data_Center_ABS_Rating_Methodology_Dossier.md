# Dossiê Técnico: Metodologia Oficial de Rating de Data Center ABS (KBRA & S&P)
**Referência:** KBRA Data Center ABS Global Rating Methodology (Edição Atualizada 2026) e S&P Global Structured Finance Criteria.

---

## 1. Visão Geral da Metodologia KBRA

A Kroll Bond Rating Agency (KBRA) é a agência líder e pioneira na avaliação de títulos lastreados em centros de processamento de dados (*Data Center Asset-Backed Securities - ABS*). Diferente de hipotecas residenciais ou comerciais tradicionais, a avaliação de data centers envolve uma híbrida entre **crédito imobiliário, risco operacional de infraestrutura crítica e tecnologia**.

### Os Quatro Pilares de Análise da KBRA:
1. **Qualidade do Colateral Físico (Critical Facility & Power):** Redundância de energia (N+1, 2N), eficiência energética (PUE - *Power Usage Effectiveness*), contratos de fornecimento com a concessionária de energia elétrica (*PPAs - Power Purchase Agreements*) e sistemas de resfriamento.
2. **Durabilidade do Fluxo de Caixa (KNCF - KBRA Net Cash Flow):** Fluxo de caixa operacional auditado, aplicando descontos de estresse para despesas operacionais não recuperáveis, capex de reposição (*Capital Expenditures*) e vacância técnica.
3. **Perfil de Crédito dos Inquilinos & Concentração de Contratos:** Classificação de risco de cada locatário, duração média ponderada dos contratos (*WALT*) e teste de risco de inadimplência simultânea (*Tenant Default & Rollover Simulation*).
4. **Mecânica Estrutural e Gatilhos de Liquidez (*Covenants*):** Subordinação de tranches (Classe B e C), contas de reserva de liquidez (*Debt Service Reserve Accounts - DSRA*), testes de cobertura (*DSCR*) e gatilhos de amortização acelerada (*Cash Sweep / Rapid Amortization*).

---

## 2. A Fórmula do KNCF e os Testes de Estresse para Tranches "AAA / A"

Para que uma Tranche Sênior receba rating **AAA (sf)** ou **A / A- (sf)**, a KBRA submete o fluxo de caixa a cenários de estresse severo:

$$KNCF = Receita\ Bruta\ Contratada - (Despesas\ Operacionais + Capex\ de\ Manuten\ccedil\tilde{a}o + Desconto\ de\ Vac\hat{a}ncia\ For\ccedil ada)$$

### Parâmetros de Estresse Aplicados:
* **Cenário AAA / A:**
  * Simulação de falência imediata dos 2 maiores inquilinos da carteira sem reposição de receita por um período de 12 a 24 meses (*Dark Period*).
  * Desconto de 15% a 30% nas taxas de renegociação de aluguel por kW/mês (*Mark-to-Market Rent Haircut*).
  * Aumento nas despesas operacionais de energia e manutenção de 10% a 20%.
  * O fluxo de caixa residual deve ser capaz de cobrir 100% do serviço da dívida da Classe A (DSCR >= 1.0x sob estresse extremo).

---

## 3. O Fator Crítico: Concentração de Inquilinos e "Risco Binário"

A KBRA divide o mercado de Data Center ABS em dois segmentos fundamentais, com perfis de risco radicalmente distintos:

| Segmento | Características de Inquilinos | Concentração Típica | Avaliação de Risco pela KBRA | Exemplo de Emissões |
| :--- | :--- | :--- | :--- | :--- |
| **Hyperscale ABS / Single-Asset** | 1 a 3 inquilinos gigantes (Microsoft, AWS, Google, Oracle, Meta). Contratos longos (10 a 15 anos) *Triple Net (NNN)*. | **80% a 95%** concentrado nos Top 2 locatários. | **Risco Binário (*Binary Default Risk*):** O rating da dívida fica estritamente atrelado à solvência do Hyperscaler. Se o locatário não renovar, o data center fica sem receita. | CONE 2026-DFW3, Lohrasp Enterprise II, STACK Issuer. |
| **Colocation (Colo) Master Trust** | Dezenas a centenas de locatários corporativos, provedores de telecom, neoclouds e startups de software. | Top 1 inquilino costuma representar **< 15%**; carteira diversificada. | **Risco de Churn Operacional:** Menor risco binário, mas maior sensibilidade à rotatividade de clientes (*churn*), risco de crédito de pequenas empresas e custos variáveis de energia. | DataBank Issuer (Série 2021/2024/2026 com ~1.750 tenants), TierPoint, Centersquare. |

---

## 4. Onde Mora a Fragilidade Oculta: A Conexão com o Ciclo de IA

Embora o modelo matemático da KBRA pareça robusto, os relatórios recentes apontam **3 vetores de vulnerabilidade estrutural não previstos nos modelos históricos de 2018–2022**:

1. **Correlação Sistêmica Oculta:** O modelo assume independência entre os locatários. No entanto, com a explosão do ciclo de IA, grande parte da receita de neoclouds e provedores de colocation depende direta ou indiretamente do sucesso comercial dos modelos fundacionais de poucas companhias (OpenAI, Anthropic, Meta, Microsoft).
2. **Obsolescência da Infraestrutura de Resfriamento:** Data centers construídos antes de 2023 foram dimensionados para densidades de 8 kW a 15 kW por rack. Clusters de GPUs de alta performance (Nvidia H100, B200, GB200) exigem **40 kW a 120 kW por rack com resfriamento líquido direto**. Ativos que não conseguirem converter sua infraestrutura física perdem atratividade e valor de avaliação colateral (*LTV degradation*).
3. **Gargalo de Interconexão Elétrica:** A KBRA exige que a energia esteja contratada. Porém, atrasos de 24 a 36 meses na entrega de subestações pelas concessionárias podem postergar o início dos contratos de aluguel, pressionando a liquidez das tranches subordinadas antes do fluxo de caixa estabilizar.

---
*Documento compilado a partir dos parâmetros oficiais da KBRA Data Center Rating Methodology e notas técnicas regulatórias.*
