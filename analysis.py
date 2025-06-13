import pandas as pd

def analisar_variacoes(df: pd.DataFrame, moeda: str):
    if len(df) < 20:
        return {"moeda": moeda, "erro": "Dados insuficientes"}

    preco_hoje = df["price"].iloc[-1]
    preco_ontem = df["price"].iloc[-2]
    preco_inicio = df["price"].iloc[0]

    # Retornos
    retorno_hoje = ((preco_hoje - preco_ontem) / preco_ontem) * 100
    retorno_10d = ((preco_hoje - df["price"].iloc[-11]) / df["price"].iloc[-11]) * 100
    retorno_30d = ((preco_hoje - preco_inicio) / preco_inicio) * 100

    # Z-score
    variacoes = df["price"].pct_change().dropna()
    media = variacoes.mean()
    desvio = variacoes.std()
    z_score = ((preco_hoje / preco_ontem) - 1 - media) / desvio if desvio > 0 else 0

    # Quantis
    p95 = variacoes.quantile(0.95)
    p05 = variacoes.quantile(0.05)

    # Máxima/mínima das últimas 20 velas
    max_20 = df["price"].iloc[-21:-1].max()
    min_20 = df["price"].iloc[-21:-1].min()

    # Volatilidade
    rolling_std = variacoes.rolling(window=10).std()
    vol_atual = rolling_std.iloc[-1] if not rolling_std.empty else 0
    vol_med = rolling_std.mean() if not rolling_std.empty else 0

    alerta = []
    tipo = "alta" if z_score > 0 else "queda"

    # Regras
    if abs(z_score) >= 2:
        alerta.append(f"📊 Variação estatística fora do padrão (z = {z_score:.2f}, {tipo})")

    if retorno_10d < 0 and retorno_hoje > abs(retorno_10d):
        alerta.append("🔁 Reversão após sequência negativa")

    if retorno_hoje > p95 * 100:
        alerta.append("🚀 Explosão de preço (acima do percentil 95)")

    if retorno_hoje < p05 * 100:
        alerta.append("⚠️ Queda forte (abaixo do percentil 5)")

    if preco_hoje > max_20:
        alerta.append("📈 Rompimento de máxima recente")

    if preco_hoje < min_20:
        alerta.append("📉 Rompimento de mínima recente")

    if vol_med > 0 and vol_atual < vol_med * 0.5:
        alerta.append("💤 Baixa volatilidade (pode antecipar movimento forte)")

    return {
        "moeda": moeda,
        "preco_hoje": round(preco_hoje, 2),
        "retorno_hoje": round(retorno_hoje, 2),
        "retorno_10d": round(retorno_10d, 2),
        "retorno_30d": round(retorno_30d, 2),
        "z_score": round(z_score, 2),
        "alertas": alerta or ["Sem sinais relevantes hoje"]
    }

# Teste
if __name__ == "__main__":
    from crypto_data import obter_historico_preco
    df = obter_historico_preco("solana", quantidade=100, intervalo="1h")
    resultado = analisar_variacoes(df, "solana")
    print(resultado)
