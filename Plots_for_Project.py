import matplotlib.pyplot as plt

# Daten für Komorbiditäten
comorbidities = [
    "Cardiovascular disease", "Myocardial infarction", "Stroke", "Chronic heart failure",
    "Coronary artery disease", "Atrial fibrillation", "Peripheral artery disease",
    "Chronic obstructive pulmonary disease", "Deep vein thrombosis", "Chronic kidney disease",
    "Chronic lung disease", "Cancer"
]
percentages = [61, 42, 13, 98, 69, 78, 1, 32, 73, 12, 50, 51]

# Definition der Risikofaktoren und deren Vorhandensein für die Tabelle
risk_factors = ['Diabetes', 'Obesity', 'Smoking', 'Hypertension', 'Dyslipidemia', 'Family history of MI/Stroke']
presence = ['Yes', 'No', 'No', 'No', 'Yes', 'Yes']

# Erstellen einer Figur und zwei Subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

# Plot für Komorbiditäten auf der linken Seite
bars = ax1.barh(comorbidities, percentages, color='blue')
ax1.set_xlabel('Percent')
ax1.set_title('Comorbidities Percentages')
for bar in bars:
    width = bar.get_width()
    ax1.text(width - 5, bar.get_y() + bar.get_height()/2, f'{width}%',
             ha='center', va='center', color='white', fontsize=10)

# Tabelle mit Risikofaktoren auf der rechten Seite
the_table = ax2.table(cellText=list(zip(risk_factors, presence)),
                      colLabels=['Cardiovascular Risk Factor', 'Presence'],
                      colColours=['lightgray']*2,
                      cellLoc='center',
                      loc='center',
                      bbox=[0, 0, 1, 1])
the_table.scale(1, 2)
ax2.axis('off')
ax2.set_title('Cardiovascular Risk Factors')

plt.tight_layout()
plt.show()
