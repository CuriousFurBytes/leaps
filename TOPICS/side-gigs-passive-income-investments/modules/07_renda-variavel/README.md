# Module 07: Renda Variável

[← Module 06: Renda Fixa](../06_renda-fixa/) | [Topic Home](../../README.md) | [Next → Module 08: Fundos Imobiliários](../08_fundos-imobiliarios/)

---

![Status](https://img.shields.io/badge/status-not--started-lightgrey)
![Difficulty](https://img.shields.io/badge/difficulty-Intermediate--Advanced-orange)
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

Renda variável is where long-term wealth acceleration happens. While renda fixa provides safety, predictability, and inflation protection, equities (ações) and equity funds (ETFs, FIIs) have historically generated higher real returns over long time horizons — compensating investors for accepting volatility.

The B3 (Brasil, Bolsa, Balcão) is Brazil's stock exchange, home to over 400 publicly listed companies. Every Brazilian with a CPF and a brokerage account (free at dozens of brokers) can buy fractional shares in any of these companies, participate in IPOs, and trade ETFs that provide broad market exposure with a single purchase.

This module demystifies the B3. You will understand how the market operates, what drives stock prices, the difference between fundamentalist analysis (valuing companies based on financials) and technical analysis (reading charts), how to use ETFs for low-cost diversification, and how dividends and capital gains are taxed for Brazilian individual investors.

---

## Prerequisites

- [[side-gigs-passive-income-investments/modules/06_renda-fixa]] — understanding of risk-return trade-off, CDI benchmark, IR treatment
- [[side-gigs-passive-income-investments/modules/01_introduction]] — compound interest, investment pyramid, GCAP tax overview

---

## Objectives

By the end of this module, you will be able to:

1. Explain how the B3 functions: trading sessions, order types, circuit breakers, settlement (D+2)
2. Distinguish between ações ordinárias (ON) and preferenciais (PN) and explain their different rights
3. Calculate Dividend Yield (DY) and explain its limitations as a sole investment criterion
4. Apply a basic fundamentalist framework (P/L, P/VP, ROE, Dívida/EBITDA) to evaluate a Brazilian company
5. Explain the role of ETFs (BOVA11, IVVB11, SMAL11) as diversification tools and when to use them vs. individual stocks
6. Calculate GCAP for a stock sale scenario and determine whether DARF payment is required

---

## Theory

> [!NOTE]
> This module is a stub. Full theory content will be expanded in a future update.

### How the B3 Works

The B3 operates with standard equity market mechanics. Trading hours: 10:00–17:00 (pregão regular), with a pre-open auction and after-market session. Settlement is D+2 (shares and cash settle two business days after the trade).

Shares are identified by 4-letter + digit codes: PETR4 (Petrobras PN), VALE3 (Vale ON), ITUB4 (Itaú PN), BBAS3 (Banco do Brasil ON). The digit:
- 3 = ação ordinária (ON) — voting rights
- 4 = ação preferencial (PN) — no voting rights but priority in dividends/liquidation (historically)
- 11 = BDR, FII, or ETF

Fractional shares (mercado fracionário) allow buying any quantity (e.g., 1 share instead of the standard lot of 100). Essential for small investors.

### Análise Fundamentalista (Fundamental Analysis)

Fundamental analysis values companies based on their financial fundamentals. Key metrics for Brazilian stocks:

| Metric | Formula | Interpretation |
|--------|---------|----------------|
| P/L (P/E ratio) | Preço / Lucro por ação | How many years of current earnings to pay off purchase price. Lower = cheaper (but context matters) |
| P/VP (P/B ratio) | Preço / Valor Patrimonial por ação | Market price vs. book value. P/VP < 1 = buying below book |
| ROE | Lucro Líquido / Patrimônio Líquido | Return on equity. Higher = more profitable use of capital |
| Dividend Yield (DY) | Dividendos por ação / Preço da ação | Annual dividend as % of price. Higher = more current income |
| Dívida Líquida/EBITDA | Net Debt / EBITDA | Leverage ratio. < 2x is generally safe; > 4x is concerning |

### ETFs: The Low-Effort Option

Exchange-Traded Funds (ETFs) allow single-instrument exposure to a broad index. Key Brazilian ETFs:

| ETF | Tracks | Tax treatment | Notes |
|-----|--------|---------------|-------|
| BOVA11 | IBOVESPA (B3's main index) | 15% GCAP on gains (no isenção) | Core Brazil equity exposure |
| SMAL11 | IBOVESPA Small Cap | 15% GCAP on gains (no isenção) | Small and mid-cap exposure |
| IVVB11 | S&P 500 (USD via BDR) | 15% GCAP, no isenção | US equity exposure without offshore account |
| TITH11, FIXA11 | Fixed income indices | Renda fixa taxation | Renda fixa ETFs |

> [!IMPORTANT]
> ETFs on B3 do NOT benefit from the R$ 20.000/mês isenção that applies to individual ações. All gains on ETF sales are taxable at 15%, regardless of sale size. This is a frequently misunderstood rule.

### Dividends in Brazil

Brazilian companies must distribute at least 25% of adjusted net profit as dividends (Lei das S.A.). Many companies distribute more. Dividends are currently **exempt from IR** for individual investors.

This creates the "dividendo trap": optimizing solely for high DY without regard to capital quality can lead to investing in declining companies that pay high dividends because they have no better use for the cash. A company paying 15% DY while its stock falls 20%/year is not an attractive investment.

---

## Key Concepts

**IBOVESPA** — Brazil's main stock market index, comprising approximately 87 stocks that together represent ~80% of B3's total trading volume. Used as the primary benchmark for Brazilian equity performance.

**Ação ordinária (ON)** — Common share with voting rights at shareholder meetings. The "type 3" shares (PETR3, VALE3).

**Ação preferencial (PN)** — Preferred share, typically with no voting rights but priority in dividend distribution and (historically) liquidation. The "type 4" shares (PETR4, ITUB4).

**Dividend Yield (DY)** — Annual dividends divided by current stock price. Expressed as a percentage. A high DY must be evaluated in context: is it sustainable? Is the payout ratio too high? Is the stock price depressed because of business problems?

**Análise técnica** — Technical analysis: using charts, price patterns, and volume data to predict future price movements. Academically controversial but widely practiced by Brazilian day traders. Module 07 provides an introduction; deep TA is beyond this topic's scope.

**GCAP (Ganho de Capital)** — Capital gain. Taxable at 15% for ações when monthly sales exceed R$ 20.000. See [[side-gigs-passive-income-investments/modules/10_tax-optimization-and-compliance]] for complete rules.

---

## Examples

> [!NOTE]
> Full worked examples will be added when this module is expanded.

### DY calculation example

Stock ITUB4 is trading at R$ 32,00. Last 12 months' dividends: R$ 2,40 per share.

`DY = R$ 2,40 / R$ 32,00 = 7.5% per year`

Interpretation: Buying ITUB4 today gives a 7.5% yield on current price, tax-free. If the stock price rises or dividends increase, your yield on cost improves further.

---

## Common Pitfalls

- **Investing without an emergency fund** — Volatility forces panic selling when unexpected expenses arise. Build Level 1 first.
- **Confusing trading with investing** — Day trading is a zero-sum game dominated by algorithms and professionals. Buy-and-hold long-term investing in quality companies is a different, sustainable activity.
- **ETF isenção misunderstanding** — ETFs do NOT qualify for the R$ 20k monthly exemption. Pay DARF on all ETF capital gains.
- **Chasing DY without analyzing fundamentals** — High DY can indicate a company in trouble. Analyze payout sustainability before buying for income.
- **Overconcentration** — Owning 5+ stocks in the same sector eliminates diversification benefit. Spread across sectors and market caps.

---

## Cross-Links

- [[side-gigs-passive-income-investments/modules/06_renda-fixa]] — Renda fixa provides the safety foundation; renda variável is the growth engine above it
- [[side-gigs-passive-income-investments/modules/08_fundos-imobiliarios]] — FIIs are a hybrid: traded on B3 like ações but generating renda-fixa-like income; this module's B3 concepts apply directly
- [[side-gigs-passive-income-investments/modules/10_tax-optimization-and-compliance]] — The GCAP tax, DARF payment, and isenção rules for ações are fully detailed in Module 10

---

## Summary

- The B3 provides access to 400+ listed companies; fractional shares (mercado fracionário) make entry accessible from R$ 10
- Ações ON (type 3) carry voting rights; ações PN (type 4) traditionally have dividend priority — most retail investors focus on type 3 or 11
- ETFs (BOVA11, IVVB11, SMAL11) offer diversified market exposure with single instruments and very low management fees
- Fundamental analysis uses P/L, P/VP, ROE, and DY to assess company value — all metrics must be read in context, not in isolation
- ETF gains are NOT exempt from the R$ 20k monthly isenção — all gains taxable at 15%, a frequently-violated rule
- Dividends from Brazilian companies are currently IR-exempt for individuals — but high DY alone is not a sufficient investment thesis
