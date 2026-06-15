-- ============================================================
-- Q1: Total percentage return per stock (full data period)
-- First available close → last available close
-- ============================================================
WITH first_date AS (
    SELECT ticker, MIN(trade_date) AS dt
    FROM daily_prices GROUP BY ticker
),
last_date AS (
    SELECT ticker, MAX(trade_date) AS dt
    FROM daily_prices GROUP BY ticker
)
SELECT
    s.ticker,
    s.company_name,
    s.market,
    s.sector,
    fp.close_price                                                      AS start_price,
    lp.close_price                                                      AS end_price,
    ROUND(((lp.close_price - fp.close_price) / fp.close_price)*100, 2) AS total_return_pct
FROM stocks s
JOIN first_date fd ON s.ticker = fd.ticker
JOIN daily_prices fp ON s.ticker = fp.ticker AND fp.trade_date = fd.dt
JOIN last_date  ld ON s.ticker = ld.ticker
JOIN daily_prices lp ON s.ticker = lp.ticker AND lp.trade_date = ld.dt
ORDER BY total_return_pct DESC;


-- ============================================================
-- Q2: Annual return per stock per year
-- First trading day of year → last trading day of year
-- ============================================================
WITH year_bounds AS (
    SELECT ticker,
           YEAR(trade_date) AS yr,
           MIN(trade_date)  AS first_date,
           MAX(trade_date)  AS last_date
    FROM daily_prices
    GROUP BY ticker, YEAR(trade_date)
)
SELECT
    yb.ticker,
    s.company_name,
    s.market,
    s.sector,
    yb.yr                                                                    AS year,
    fp.close_price                                                           AS year_open,
    lp.close_price                                                           AS year_close,
    ROUND(((lp.close_price - fp.close_price) / fp.close_price) * 100, 2)   AS annual_return_pct
FROM year_bounds yb
JOIN stocks      s  ON yb.ticker = s.ticker
JOIN daily_prices fp ON yb.ticker = fp.ticker AND fp.trade_date = yb.first_date
JOIN daily_prices lp ON yb.ticker = lp.ticker AND lp.trade_date = yb.last_date
ORDER BY yb.ticker, yb.yr;