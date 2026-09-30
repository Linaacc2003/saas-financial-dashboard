import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set random seed for reproducibility
np.random.seed(42)

# Define date range (Past 12 months)
end_date = datetime.today().replace(day=1)
start_date = end_date - timedelta(days=365)
dates = pd.date_range(start=start_date, end=end_date, freq='MS')

# Mock data generation logic
data = []
customer_id_counter = 1000

for date in dates:
    # Simulate realistic monthly growth and churn
    new_signups = int(np.random.normal(loc=150, scale=20)) # Average 150 new users a month
    marketing_tier = np.random.choice(['Basic', 'Pro', 'Enterprise'], p=[0.6, 0.3, 0.1])
    
    for _ in range(new_signups):
        tier = np.random.choice(['Basic', 'Pro', 'Enterprise'], p=[0.6, 0.3, 0.1])
        if tier == 'Basic':
            price = 29
        elif tier == 'Pro':
            price = 99
        else:
            price = 499
            
        status = np.random.choice(['Active', 'Churned'], p=[0.93, 0.07]) # 7% monthly churn
        
        data.append({
            'Signup_Date': date.strftime('%Y-%m-%d'),
            'CustomerID': customer_id_counter,
            'Subscription_Tier': tier,
            'Monthly_Fee': price,
            'Status': status
        })
        customer_id_counter += 1

# Convert to DataFrame
df = pd.DataFrame(data)

# Save to a CSV file
df.to_csv('saas_data.csv', index=False)
print("Success! Generated 'saas_data.csv' with realistic SaaS metrics.")