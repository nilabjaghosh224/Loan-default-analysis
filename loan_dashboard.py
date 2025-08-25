# loan_dashboard.py
# Example end-to-end script for analyzing loan distribution, defaults, and borrower demographics

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------
# 1. Generate Dummy Data
# -----------------------------
np.random.seed(42)

n_loans = 500
loan_types = ["Home", "Auto", "Personal", "Education"]

loan_df = pd.DataFrame({
    "LoanID": range(1, n_loans+1),
    "LoanAmount": np.random.randint(5000, 500000, n_loans),
    "LoanType": np.random.choice(loan_types, n_loans),
    "LoanStatus": np.random.choice(["Repaid", "Defaulted"], n_loans, p=[0.8, 0.2])
})

demo_df = pd.DataFrame({
    "BorrowerID": range(1, n_loans+1),
    "Age": np.random.randint(20, 65, n_loans),
    "Gender": np.random.choice(["Male", "Female"], n_loans),
    "Income": np.random.randint(20000, 200000, n_loans),
    "Defaulted": (loan_df["LoanStatus"] == "Defaulted").astype(int)
})

# -----------------------------
# 2. Analysis
# -----------------------------
# Default rate
default_rate = demo_df["Defaulted"].mean() * 100
print(f"Overall Default Rate: {default_rate:.2f}%")

# Average loan amount by type
loan_type_summary = loan_df.groupby("LoanType")["LoanAmount"].mean()
print("\nAverage Loan Amount by Type:\n", loan_type_summary)

# Default rate by gender
default_by_gender = demo_df.groupby("Gender")["Defaulted"].mean() * 100
print("\nDefault Rate by Gender (%):\n", default_by_gender)

# -----------------------------
# 3. Visualizations
# -----------------------------
sns.set(style="whitegrid")

# Loan Amount Distribution
plt.figure(figsize=(8,5))
sns.histplot(loan_df["LoanAmount"], bins=30, kde=True, color="skyblue")
plt.title("Loan Amount Distribution")
plt.xlabel("Loan Amount")
plt.ylabel("Count")
plt.tight_layout()
plt.show()

# Default Rate by Gender
plt.figure(figsize=(6,4))
sns.barplot(x="Gender", y="Defaulted", data=demo_df, estimator=lambda x: np.mean(x)*100, palette="pastel")
plt.title("Default Rate by Gender (%)")
plt.ylabel("Default Probability (%)")
plt.tight_layout()
plt.show()

# Income vs Default (boxplot)
plt.figure(figsize=(7,5))
sns.boxplot(x="Defaulted", y="Income", data=demo_df, palette="muted")
plt.title("Income Distribution vs Loan Default")
plt.xticks([0, 1], ["Repaid", "Defaulted"])
plt.tight_layout()
plt.show()

# -----------------------------
# 4. Export for Power BI
# -----------------------------
processed_df = demo_df.groupby("Age")["Defaulted"].mean().reset_index()
processed_df.rename(columns={"Defaulted": "DefaultRate"}, inplace=True)
processed_df.to_csv("processed_for_powerbi.csv", index=False)

print("\nProcessed borrower demographics exported to 'processed_for_powerbi.csv'.")
