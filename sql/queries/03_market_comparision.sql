-- ============================================================
-- Q6: India vs US — head-to-head market comparison
-- ============================================================
SELECT
    market,
    COUNT(DISTINCT ticker)                                          AS num_stocks,
    ROUND(AVG(daily_return) * 252 * 100,              4)           AS annualised_return_pct,
    ROUND(STD(daily_return) * SQRT(252) * 100,        4)           AS annualised_volatility_pct,
    ROUND(AVG(daily_return) / NULLIF(STD(daily_return),0) * SQRT(252), 4) AS sharpe_proxy
FROM stock_features
WHERE daily_return IS NOT NULL
GROUP BY market;


-- ============================================================
-- Q7: Monthly seasonality — which months give best returns?
-- Averaged across all stocks and all years
-- ============================================================
SELECT
    market,
    MONTH(trade_date)                            AS month_num,
    DATE_FORMAT(trade_date, '%b')                AS month_name,
    ROUND(AVG(daily_return) * 100, 4)            AS avg_daily_return_pct,
    ROUND(STD(daily_return) * 100, 4)            AS avg_volatility_pct,
    COUNT(*)                                     AS total_observations
FROM stock_features
WHERE daily_return IS NOT NULL
GROUP BY market, MONTH(trade_date), DATE_FORMAT(trade_date, '%b')
ORDER BY market, month_num;