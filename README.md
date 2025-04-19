# Pricing Engine Project

An automated pricing engine that adjusts product prices based on inventory levels and sales performance while ensuring minimum profit margins.

## Approach

### 1. Rule-Based Pricing Logic
Implemented a 4-tiered rule system with strict precedence:
1. **High Demand/Low Stock** (15% price increase)
2. **Dead Stock** (30% price reduction)
3. **Overstocked Inventory** (10% price reduction)
4. **Minimum Profit Constraint** (20% above cost)

Rules are evaluated sequentially, with only the first applicable rule being executed (except Rule 4 which always applies last).

### 2. Data Processing Pipeline
- **Inputs**: Merged product catalog (`products.csv`) with sales data (`sales.csv`) on SKU
- **Transformations**:
  - Filled missing sales with 0 (assuming no sales = 0 quantity sold)
  - Applied pricing rules row-wise
  - Enforced minimum profit margins
- **Output**: Generated `updated_prices.csv` with old/new prices

### 3. Error Handling
- Silent NaN handling for missing sales data
- Implicit type conversion for numeric fields
- No hard failures (graceful execution with potential warnings)

## Key Assumptions

1. **Data Structure**:
   - `products.csv` must contain: `sku, current_price, cost_, stock`
   - `sales.csv` must contain: `sku, quantity_sold`

2. **Business Rules**:
   - All products must maintain ≥20% profit margin
   - "Dead stock" threshold: >200 units with 0 sales
   - "Overstocked" threshold: >100 units with <20 sales

3. **Edge Cases**:
   - Products without sales records are treated as zero sales
   - Negative prices are prevented by minimum profit constraint
   - Floating-point rounding to 2 decimal places for currency

## Repository Structure
/pricing-engine
├── products.csv # Product catalog with prices/costs 
├── sales.csv # Recent sales data (30-day period) 
├── pricing_engine.py # Core pricing logic implementation 
├── updated_prices.csv # Generated output (after script execution) 
└── README.md # This documentation 

