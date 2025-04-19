import pandas as pd


def load_data(products_file, sales_file):
    """Load and merge product and sales data"""
    products = pd.read_csv(products_file)
    sales = pd.read_csv(sales_file)

    # Merge product and sales data on SKU
    merged = pd.merge(products, sales, on='sku', how='left')

    # Fill NaN values for quantity_sold with 0 (if a product has no sales)
    merged['quantity_sold'] = merged['quantity_sold'].fillna(0)

    return merged


def apply_pricing_rules(data):
    """Apply pricing rules to each product"""
    updated_prices = []

    for _, row in data.iterrows():
        sku = row['sku']
        current_price = row['current_price']
        cost = row['cost_']
        stock = row['stock']
        quantity_sold = row['quantity_sold']

        new_price = current_price
        rule_applied = None

        # Rule 1: Low Stock, High Demand
        if stock < 20 and quantity_sold > 30:
            new_price = current_price * 1.15
            rule_applied = 1

        # Rule 2: Dead Stock (only if Rule 1 wasn't applied)
        elif rule_applied is None and stock > 200 and quantity_sold == 0:
            new_price = current_price * 0.7
            rule_applied = 2

        # Rule 3: Overstocked Inventory (only if Rules 1-2 weren't applied)
        elif rule_applied is None and stock > 100 and quantity_sold < 20:
            new_price = current_price * 0.9
            rule_applied = 3

        # Rule 4: Minimum Profit Constraint (always applied)
        min_price = cost * 1.2
        if new_price < min_price:
            new_price = min_price
            if rule_applied is not None:
                rule_applied = f"{rule_applied}+4"
            else:
                rule_applied = 4

        # Final rounding
        new_price = round(new_price, 2)

        updated_prices.append({
            'sku': sku,
            'old_price': f"{current_price} USD",
            'new_price': f"{new_price} USD"
        })

    return pd.DataFrame(updated_prices)


def main():
    # Load and process data
    data = load_data('products.csv', 'sales.csv')

    # Apply pricing rules
    updated_prices = apply_pricing_rules(data)

    # Save to CSV
    updated_prices.to_csv('updated_prices.csv', index=False)
    print("Updated prices saved to updated_prices.csv")


if __name__ == "__main__":
    main()