-- ============================================================
-- Q3: Top 10 gainers (highest total return) — both markets
-- ============================================================
WITH first_date AS (SELECT ticker, MIN(trade_date) AS dt FROM daily_prices GROUP BY ticker),
     last_date  AS (SELECT ticker, MAX(trade_date) AS dt FROM daily_prices GROUP BY ticker)
SELECT
    s.ticker,
    s.company_name,
    s.market,
    s.sector,
    ROUND(((lp.close_price - fp.close_price) / fp.close_price)*100, 2) AS total_return_pct
FROM stocks s
JOIN first_date fd ON s.ticker = fd.ticker
JOIN daily_prices fp ON s.ticker = fp.ticker AND fp.trade_date = fd.dt
JOIN last_date  ld ON s.ticker = ld.ticker
JOIN daily_prices lp ON s.ticker = lp.ticker AND lp.trade_date = ld.dt
ORDER BY total_return_pct DESC
LIMIT 10;


-- ============================================================
-- Q4: Top 10 losers (lowest total return) — both markets
-- ============================================================
WITH first_date AS (SELECT ticker, MIN(trade_date) AS dt FROM daily_prices GROUP BY ticker),
     last_date  AS (SELECT ticker, MAX(trade_date) AS dt FROM daily_prices GROUP BY ticker)
SELECT
    s.ticker,
    s.company_name,
    s.market,
    s.sector,
    ROUND(((lp.close_price - fp.close_price) / fp.close_price)*100, 2) AS total_return_pct
FROM stocks s
JOIN first_date fd ON s.ticker = fd.ticker
JOIN daily_prices fp ON s.ticker = fp.ticker AND fp.trade_date = fd.dt
JOIN last_date  ld ON s.ticker = ld.ticker
JOIN daily_prices lp ON s.ticker = lp.ticker AND lp.trade_date = ld.dt
ORDER BY total_return_pct ASC
LIMIT 10;


-- ============================================================
-- Q5: Sector-wise performance — annualised return & volatility
-- Volatility = STD(daily_return) * SQRT(252) * 100
-- ============================================================
SELECT
    s.market,
    s.sector,
    COUNT(DISTINCT s.ticker)                             AS num_stocks,
    ROUND(AVG(sf.daily_return) * 252 * 100,    2)       AS annualised_return_pct,
    ROUND(STD(sf.daily_return) * SQRT(252)*100, 2)      AS annualised_volatility_pct
FROM stock_features sf
JOIN stocks s ON sf.ticker = s.ticker
WHERE sf.daily_return IS NOT NULL
GROUP BY s.market, s.sector
ORDER BY s.market, annualised_return_pct DESC;