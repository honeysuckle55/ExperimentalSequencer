import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import datetime
from unique_values import get_df

# Parameters (normally from your dataframe)
meas_num = 1
date = '2025-02-02'

try:
    df, name = get_df(['2025','06','13'], meas_num)
    # Rydberg
    Ryd401ZS_time = df['Ryd401ZS_time']   
    Ryd401ZS_SP = df['Ryd401ZS_SP']
    PID411_SP = df['PID411_SP']
    OnOffTwduringRydbergTweezers = df['OnOffTwduringRydbergTweezers']
    IonizationPulseDuration = df['IonizationPulseDuration']
    FieldIonize = df['FieldIonize']
    # Tweezer loading
    DoTweezer583LACs = df['DoTweezer583LACs']
    LACs583_time = df['LACs583_time']
    MOT_loadtime = df['MOT_loadtime']
    # Imaging
    ImagingLight_wavelength = df['ImagingLight_wavelength']
    if 1==1:
        print(f"Ryd401ZS_time = {Ryd401ZS_time} ({type(Ryd401ZS_time)})")
        print(f"Ryd401ZS_SP = {Ryd401ZS_SP} ({type(Ryd401ZS_SP)})")
        print(f"PID411_SP = {PID411_SP} ({type(PID411_SP)})")
        print(f"OnOffTwduringRydbergTweezers = {OnOffTwduringRydbergTweezers} ({type(OnOffTwduringRydbergTweezers)})")
        print(f"IonizationPulseDuration = {IonizationPulseDuration} ({type(IonizationPulseDuration)})")
        print(f"FieldIonize = {FieldIonize} ({type(FieldIonize)})")
        print(f"DoTweezer583LACs = {DoTweezer583LACs} ({type(DoTweezer583LACs)})")
        print(f"LACs583_time = {LACs583_time} ({type(LACs583_time)})")
        print(f"MOT_loadtime = {MOT_loadtime} ({type(MOT_loadtime)})")
        print(f"ImagingLight_wavelength = {ImagingLight_wavelength} ({type(ImagingLight_wavelength)})")
except NameError:
    print('We are here')
    Ryd401ZS_time = 0.005
    Ryd401ZS_SP = 0.2
    PID411_SP = 120
    OnOffTwduringRydbergTweezers = 1
    IonizationPulseDuration = 0.005
    ImagingLight_wavelength = 583
    FieldIonize = 0
    DoTweezer583LACs = 1
    LACs583_time = 30
    MOT_loadtime = 100

# Step data
steps = [
    dict(name="Tweezers", start=0, duration=20, group="Prep", label=f"MOT load for {MOT_loadtime[1]} ms"),
    dict(name="LAC", start=10, duration=10, group="Control", label=f"t={LACs583_time[1]} ms"),
    dict(name="ZS 401", start=20, duration=10, group="Manipulation", label=f"P={Ryd401ZS_SP[1]} mW, t={Ryd401ZS_time[1]*1e3:.1f} µs"),
    dict(name="411", start=20, duration=10, group="Manipulation", label=f"P={PID411_SP[1]} mW"),
]

if ImagingLight_wavelength[1] == 1:
    steps.append(dict(name="Imaging (401)", start=35.005, duration=5, group="Readout", label="pulsed"))
elif ImagingLight_wavelength[1] == 2:
    steps.append(dict(name="Imaging (583)", start=35.005, duration=5, group="Readout", label="XX ms"))

if OnOffTwduringRydbergTweezers[1] == 0:
    steps.append(dict(name="Tweezers", start=20, duration=20, group="Prep", label=""))
else:
    steps.append(dict(name="Tweezers", start=30, duration=10, group="Prep", label="Recapture"))

if FieldIonize[1] == 1:
    steps.append(dict(name="HV", start=30, duration=5, group="Optional", label=f"1400 Vpp, t={IonizationPulseDuration[1]*1e3:.1f} µs"))

# Colors
colors = {
    "Prep": "turquoise",
    "Control": "orange",
    "Manipulation": "skyblue",
    "Optional": "violet",
    "Readout": "lightgreen"
}

# Unique y-axis positions per step (allows reuse of same name with diff labels)
y_labels = list(dict.fromkeys([step["name"] for step in steps]))
y_pos = {name: i for i, name in enumerate(reversed(y_labels))}

# Plot
fig, ax = plt.subplots(figsize=(10, 6))

for step in steps:
    y = y_pos[step["name"]]
    ax.barh(
        y=y,
        width=step["duration"],
        left=step["start"],
        height=0.6,
        color=colors[step["group"]],
        edgecolor='k'
    )
    # Add label inside bar
    ax.text(
        step["start"] + 0.3,
        y,
        step["label"],
        va='center',
        ha='left',
        fontsize=9,
        color='black'
    )

# Formatting
ax.set_yticks(list(y_pos.values()))
ax.set_yticklabels(reversed(y_labels))
ax.set_xlabel("Time (ms)")
ax.set_title("Experimental Sequence Timeline")
ax.invert_yaxis()
ax.set_xlim(0, 40)

# Legend
legend_patches = [mpatches.Patch(color=clr, label=grp) for grp, clr in colors.items()]
ax.legend(handles=legend_patches, loc='upper left')

plt.tight_layout()

# Save to file
#filename = f"date_{date}_meas_{meas_num}_timeline.pdf"
filename = f"date_{date}_meas_13_timeline.png"
plt.savefig(filename, format="png")
print(f"✅ Saved to {filename}")

plt.show()