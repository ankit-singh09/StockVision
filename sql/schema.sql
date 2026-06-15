-- ============================================================
-- StockVision — Database Schema
-- ============================================================

USE stockvision;

-- ── Table 1: stocks (dimension) ──────────────────────────────
-- One row per stock. Stores all metadata in one place.
CREATE TABLE IF NOT EXISTS stocks (
    stock_id     INT                  AUTO_INCREMENT PRIMARY KEY,
    ticker       VARCHAR(20)          NOT NULL UNIQUE,
    company_name VARCHAR(100)         NOT NULL,
    market       ENUM('India', 'US')  NOT NULL,
    sector       VARCHAR(50)          NOT NULL,
    exchange     VARCHAR(10)          NOT NULL,
    created_at   TIMESTAMP            DEFAULT CURRENT_TIMESTAMP
);

-- ── Table 2: daily_prices (fact) ─────────────────────────────
-- One row per stock per trading day. ~300K rows total.
CREATE TABLE IF NOT EXISTS daily_prices (
    price_id     BIGINT               AUTO_INCREMENT PRIMARY KEY,
    stock_id     INT                  NOT NULL,
    ticker       VARCHAR(20)          NOT NULL,
    market       ENUM('India', 'US')  NOT NULL,
    trade_date   DATE                 NOT NULL,
    open_price   DECIMAL(12, 4),
    high_price   DECIMAL(12, 4),
    low_price    DECIMAL(12, 4),
    close_price  DECIMAL(12, 4),      -- adjusted close (splits + dividends)
    volume       BIGINT,
    FOREIGN KEY  (stock_id) REFERENCES stocks(stock_id) ON DELETE CASCADE,
    UNIQUE KEY   uq_ticker_date  (ticker, trade_date),
    INDEX        idx_ticker      (ticker),
    INDEX        idx_market_date (market, trade_date),
    INDEX        idx_trade_date  (trade_date)
);