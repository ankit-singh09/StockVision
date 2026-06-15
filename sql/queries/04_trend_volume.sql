-- ============================================================
-- Q8: Bull trend signals — stocks above their 200-day MA
-- as of the most recent trading day in the dataset
-- ============================================================
SELECT
    sf.ticker,
    s.company_name,
    s.market,
    s.sector,
    sf.close_price,
    ROUND(sf.ma_200, 2)                                             AS ma_200,
    ROUND(((sf.close_price - sf.ma_200) / sf.ma_200) * 100, 2)    AS pct_above_ma200,
    CASE WHEN sf.close_price > sf.ma_200 THEN 'Bull' ELSE 'Bear'
    END                                                             AS trend_signal
FROM stock_features sf
JOIN stocks s ON sf.ticker = s.ticker
WHERE sf.trade_date = (
    SELECT MAX(trade_date)
    FROM stock_features sf2
    WHERE sf2.ticker = sf.ticker
)
AND sf.ma_200 IS NOT NULL
ORDER BY s.market, pct_above_ma200 DESC;


-- ============================================================
-- Q9: Top 10 highest volume days per market
-- High volume = institutional activity or major news event
-- ============================================================
SELECT
    dp.ticker,
    s.company_name,
    s.market,
    dp.trade_date,
    dp.volume,
    dp.close_price,
    ROUND(sf.daily_return * 100, 2) AS daily_return_pct
FROM daily_prices dp
JOIN stocks        s  ON dp.ticker = s.ticker
JOIN stock_features sf ON dp.ticker = sf.ticker AND dp.trade_date = sf.trade_date
WHERE dp.market = 'India'      -- change to 'US' for US market
ORDER BY dp.volume DESC
LIMIT 10;