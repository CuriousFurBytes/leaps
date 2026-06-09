# Module 06: Renda Fixa

[← Module 05: E-commerce and Marketplace](../05_ecommerce-and-marketplace/) | [Topic Home](../../README.md) | [Next → Module 07: Renda Variável](../07_renda-variavel/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-Intermediate-yellow)
![Time](https://img.shields.io/badge/time-8--10h-orange)

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Objectives](#objectives)
4. [Theory](#theory)
5. [Key Concepts](#key-concepts)
6. [Examples](#examples)
7. [Common Pitfalls](#common-pitfalls)
8. [Cross-Links](#cross-links)
9. [Summary](#summary)

---

## Overview

Renda fixa is the foundation of every Brazilian investment portfolio. Unlike renda variável (where returns are uncertain), renda fixa investments have predetermined or formula-based returns. In Brazil's high-interest-rate environment, renda fixa has historically offered real (inflation-adjusted) returns that would require significant equity risk in most other countries.

This module provides a thorough understanding of every major renda fixa instrument available to Brazilian retail investors: Tesouro Direto (all three types), CDB, LCI, LCA, and debentures. For each instrument, you will understand the mechanics, risk profile, tax treatment, liquidity characteristics, and appropriate use case.

The central skill this module develops is **net yield comparison** — the ability to correctly compare any renda fixa instrument against any other on an after-tax, after-cost basis, for a specific time horizon. This skill determines whether you earn 1–3 percentage points more per year, which compounds to enormous differences over long investment horizons.

---

## Prerequisites

- [[side-gigs-passive-income-investments/modules/01_introduction]] — specifically: CDI/SELIC concepts, tabela regressiva overview, the investment pyramid framework

---

## Objectives

By the end of this module, you will be able to:

1. Explain the mechanics, risk, and appropriate use case for each major Brazilian renda fixa instrument (Tesouro Selic, Tesouro IPCA+, Tesouro Prefixado, CDB, LCI, LCA, debêntures)
2. Calculate after-tax net yield for any renda fixa investment for any holding duration using the tabela regressiva
3. Compare CDB, LCI, and LCA on a net yield basis and identify which is superior for a given investment horizon
4. Explain the FGC (Fundo Garantidor de Créditos) coverage and its implications for portfolio construction across multiple institutions
5. Explain the mark-to-market risk of Tesouro IPCA+ and Prefixado bonds and why it matters for investors who may need to sell before maturity
6. Construct a renda fixa "ladder" (escalonamento de vencimentos) for a specific financial goal with varying liquidity needs

---

## Theory

> [!NOTE]
> This module is a stub. Full theory content will be expanded in a future update.

### Tesouro Direto: Three Bond Types

The Brazilian government offers three types of bonds through Tesouro Direto:

**Tesouro Selic (LFT)** — Post-fixed bond that tracks the SELIC rate daily. Key properties:
- Yield: approximately SELIC rate (minus 0.20% annual Treasury fee, minus 0.10–0.30% broker fee if applicable)
- Mark-to-market risk: essentially zero (daily restatement means always close to par)
- Ideal for: emergency fund (Level 1), short-term savings, capital preservation
- Minimum purchase: approximately R$ 30
- Tax: tabela regressiva applies

**Tesouro IPCA+ (NTN-B)** — Hybrid bond paying IPCA inflation + a fixed annual spread.
- Yield: IPCA + X% (where X is the rate at time of purchase, locked in for the bond's life)
- Mark-to-market risk: SIGNIFICANT — if market rates rise after purchase, the bond's market value falls, even though the final yield is guaranteed if held to maturity
- Ideal for: long-term goals (retirement, independence), inflation protection
- Tax: tabela regressiva applies; note that only the NOMINAL gain is taxed, not the IPCA inflation correction portion (this is a tax advantage)

**Tesouro Prefixado (LTN)** — Fixed nominal rate bond.
- Yield: fixed at purchase (e.g., 13% per year regardless of future SELIC or inflation)
- Mark-to-market risk: SIGNIFICANT — even more sensitive to rate changes than IPCA+
- Ideal for: falling interest rate environments (bond prices rise as rates fall), specific future nominal value needs
- Tax: tabela regressiva applies

### CDB: The Bank Deposit Alternative

CDB (Certificado de Depósito Bancário) is the most widely-held renda fixa instrument after Tesouro Direto. Banks issue CDBs to fund their lending operations.

Key parameters:
- **Rate:** Usually expressed as % of CDI (e.g., 110% CDI, 115% CDI). Large banks typically offer lower rates (95–100% CDI); smaller digital banks offer higher rates (110–130% CDI) to attract deposits.
- **Protection:** FGC covers up to R$ 250.000 per CPF per institution (not per account). This limit includes principal AND accumulated interest.
- **Liquidity:** Varies. Some CDBs have daily liquidity (liquidez diária, lower rates); others have lock-up periods until maturity (higher rates).
- **Tax:** Tabela regressiva applies.

### LCI and LCA: The Tax-Exempt Alternatives

LCI (Letra de Crédito Imobiliário) and LCA (Letra de Crédito do Agronegócio) are bank-issued instruments that fund specific sectors. The key advantage: **complete IR exemption** for individual investors.

Key parameters:
- **Rate:** Usually 85–95% CDI, but this must be compared on a net basis (see worked examples)
- **Protection:** FGC covers up to R$ 250.000 per CPF per institution
- **Minimum lock-up:** 90 days for LCI, 90 days for LCA (by regulatory requirement)
- **Tax:** Exempt (this is the defining advantage)

The equivalence formula: `LCI_equivalent_rate = CDB_rate × (1 - IR_rate)`
For a 1-year CDB at 110% CDI (IR = 17.5%): `110% × (1 - 0.175) = 90.75% CDI net`
An LCI at 90% CDI is slightly worse; LCI at 92% CDI is better.

### Debentures

Corporate bonds issued by companies. Two types:
- **Debêntures comuns:** Subject to tabela regressiva IR. Higher yields than government bonds but with credit risk.
- **Debêntures incentivadas (Lei 12.431):** IR-exempt for individuals. Issued by infrastructure companies (energy, transport, sanitation). Usually pay IPCA + spread. Excellent for long-term inflation protection with no IR.

---

## Key Concepts

**Marcação a mercado** — Mark-to-market pricing. When interest rates change, the market price of a fixed-rate or IPCA+ bond changes inversely. Rising rates → falling bond prices; falling rates → rising bond prices. Tesouro Selic bonds have negligible mark-to-market risk; Tesouro Prefixado and IPCA+ bonds have significant mark-to-market risk for early redemption.

**FGC (Fundo Garantidor de Créditos)** — Deposit insurance fund covering CDB, LCI, LCA, and savings accounts up to R$ 250.000 per CPF per institution. Not a government guarantee — funded by the institutions themselves. The R$ 250.000 limit includes accumulated interest.

**CDI (Certificado de Depósito Interbancário)** — The overnight interbank lending rate; tracks SELIC very closely. The standard benchmark for renda fixa comparison. When a CDB is "110% CDI," it means the annual yield is 1.10 × the CDI rate.

**Liquidez** — Liquidity. The ability to convert the investment to cash. Tesouro Selic has D+1 liquidez. CDB com liquidez diária has D+0. LCI/LCA have carência (lock-up period) of at least 90 days.

---

## Examples

> [!NOTE]
> Full worked examples will be added when this module is expanded.

### Net yield comparison: 2-year investment horizon

| Instrument | Gross Yield | IR Rate | Net Yield |
|------------|------------|---------|-----------|
| CDB 120% CDI | 120% | 15% | 102% CDI |
| LCI 98% CDI | 98% | Exempt | 98% CDI |
| LCA 99% CDI | 99% | Exempt | 99% CDI |
| Tesouro IPCA+ IPCA+6% | IPCA+6% | 15% on nominal gain | IPCA+5.1% (approx net) |
| Debênture incentivada IPCA+7% | IPCA+7% | Exempt | IPCA+7% |

For a purely nominal comparison on a 2-year horizon, the CDB at 102% CDI net beats the LCI at 98% and LCA at 99%. But the IPCA+-linked instruments protect against inflation scenarios — a different type of return.

---

## Common Pitfalls

- **Comparing gross rates across different tax regimes** — Always convert to net. A CDB at 130% CDI does not beat an LCI at 95% CDI for short investment periods once IR is applied.
- **Ignoring FGC concentration limits** — Keeping R$ 400.000 at one bank means R$ 150.000 is not covered. Spread across institutions.
- **Selling Tesouro IPCA+ before maturity in a rising rate environment** — The mark-to-market loss can be severe. IPCA+ bonds are only predictable if held to maturity.
- **Assuming all "daily liquidity" CDBs are equivalent** — CDB liquidez diária at 100% CDI from a large bank vs. 105% CDI from a smaller digital bank represent different risk-return trade-offs. Assess the issuing bank's health.
- **Not considering IOF for sub-30-day redemptions** — IOF on renda fixa income is charged at high rates for redemptions within 30 days. Budget accordingly.

---

## Cross-Links

- [[side-gigs-passive-income-investments/modules/01_introduction]] — The emergency fund, investment pyramid Level 1 and 2, and tax overview from Module 01 are the foundation for all concepts here
- [[side-gigs-passive-income-investments/modules/10_tax-optimization-and-compliance]] — Detailed IR declaration procedures for renda fixa income, including IRPF annual declaration
- [[side-gigs-passive-income-investments/modules/11_financial-independence-in-brazil]] — Tesouro IPCA+ is a core instrument for long-term financial independence portfolios in Brazil

---

## Summary

- Renda fixa encompasses government bonds (Tesouro Direto), bank instruments (CDB, LCI, LCA), and corporate bonds (debentures) — each with different risk, return, and tax profiles
- Tesouro Selic is the safest, most liquid option — ideal for emergency fund and short-term capital; Tesouro IPCA+ is the best long-term inflation protection
- CDB carries credit risk mitigated by FGC (up to R$250k per institution); LCI/LCA are IR-exempt but have lock-up minimums
- Always compare net yields (after IR) on a matched time horizon — gross rate comparisons are misleading
- Mark-to-market risk of IPCA+ and Prefixado bonds is real and significant for early redemptions; only invest with money you will not need before maturity
- Building a renda fixa ladder (escalonamento) matching maturities to specific future financial needs is the professional approach to portfolio construction
