import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

data = {
    "Protein": ["1BV8","1L8K","1M4K","1ZT3","2BT2","2F9L","2F9M","2JTK","2MGS","2NLS",
                "2NMS","2QKQ","2V0V","3B2U","3C09","3FA7","3H8M","3TN2","4ET7","5K38",
                "6FNL","7MN6","7RDB","7SZL","8DGR"],
    "DeltaG": [-17.903,-14.955,-16.382,-9.973,-15.398,-19.453,-12.816,-17.369,-16.619,
               -14.667,-15.292,-12.818,-15.646,-15.043,-17.007,-19.225,-11.214,-16.042,
               -15.729,-17.144,-10.925,-13.540,-15.986,-23.991,-22.433],
    "Graphomer": [11.02685,11.00280,11.19658,10.85048,11.18133,10.99188,10.92630,
                  11.18137,10.72221,10.85191,11.04282,10.92862,11.05726,11.51953,
                  11.46450,11.03603,10.92323,10.90382,11.12185,10.90492,11.12580,
                  11.68320,11.03140,10.92031,11.57089]
}

df = pd.DataFrame(data)
df = df.sort_values("DeltaG")  # most negative at top

plt.figure(figsize=(8,10))
plt.barh(df["Protein"], df["DeltaG"])
plt.xlabel("Predicted ΔG (kcal/mol)")
plt.ylabel("Paired Protein")
plt.title("Predicted Binding Free Energy of Protein Pairs 26-50")

ax = plt.gca()
plt.grid(axis="x")
ax.grid(True, which='major', axis='x', linestyle='-', linewidth=0.5)
ax.grid(True, which='minor', axis='x', linestyle=':', linewidth=0.4)
ax.xaxis.set_minor_locator(ticker.MultipleLocator(0.25))
ax.xaxis.set_major_locator(ticker.MultipleLocator(1))

ax.grid(True, which='major', axis='x', linestyle='-', linewidth=0.6)
ax.grid(True, which='minor', axis='x', linestyle=':', linewidth=0.4)

ax.yaxis.tick_right()
ax.yaxis.set_label_position("right")
ax.tick_params(axis='y', which='both', left=True, right=True,
               labelleft=True, labelright=True)

plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()