import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import datetime
from unique_values import get_df


def flag_scanned_variables(df, var_list):
    flags = {}
    for var in var_list:
        if var in df.columns:
            unique_vals = df[var].unique()
            flags[var] = "scan" if len(unique_vals) > 1 else "constant"
        else:
            flags[var] = "missing"
    return flags

# Parameters (normally from your dataframe)
meas_num = 1
date = '2025-06-13'

# the next try-and-catch is in order to be able to work with preset values, not from the main computer
try:
    df, name = get_df(date.split('-'), meas_num)
    # searched, this feels a bit repeatative for now, cause I run through loop once in order to glag them and once to assign values.
    used_vars = [
    "Ryd401ZS_time", "Ryd401ZS_SP", "PID411_SP", "OnOffTwduringRydbergTweezers",
    "IonizationPulseDuration", "FieldIonize", "DoTweezer583LACs",
    "LACs583_time", "MOT_loadtime", "ImagingLight_wavelength"
    ]
    # blocks of parameters
    # Rydberg
    Ryd401ZS_time = df['Ryd401ZS_time'][1]
    Ryd401ZS_SP = df['Ryd401ZS_SP'][1]
    PID411_SP = df['PID411_SP'][1]
    OnOffTwduringRydbergTweezers = df['OnOffTwduringRydbergTweezers'][1]
    IonizationPulseDuration = df['IonizationPulseDuration'][1]
    FieldIonize = df['FieldIonize'][1]
    # Tweezer loading
    DoTweezer583LACs = df['DoTweezer583LACs'][1]
    LACs583_time = df['LACs583_time'][1]
    MOT_loadtime = df['MOT_loadtime'][1]
    # Imaging
    ImagingLight_wavelength = df['ImagingLight_wavelength'][1]
    if 1==1:
        flags = flag_scanned_variables(df, used_vars)
        for var, status in flags.items():
            if status == "scan":
                print(f"🔄 {var} is being scanned: {df[var].unique()}")
            elif status == "constant":
                print(f"✔️ {var} is constant.")
            elif status == "missing":
                print(f"❌ {var} is missing in df.")
    if 1==0:
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
    print('Reset to default')
    Ryd401ZS_time = 0.005
    Ryd401ZS_SP = 0.2
    PID411_SP = 120
    OnOffTwduringRydbergTweezers = 1
    IonizationPulseDuration = 0.005
    ImagingLight_wavelength = 583
    FieldIonize = 1
    DoTweezer583LACs = 1
    LACs583_time = 30
    MOT_loadtime = 100

# Step data
# somehow for now I can't put the value into the else loop, so it always prints it, even if a parameter was scanned
steps = [
    dict(name="Tweezers", start=0, duration=20, group="Prep", label=f"MOT load for {MOT_loadtime} ms"),
    dict(name="LAC", start=10, duration=10, group="Control", label=f"t={LACs583_time} ms"),
    dict(name="ZS 401", start=20, duration=10, group="Manipulation", 
         label=(":arrows_counterclockwise: t variable (scanned)"
                if flags['Ryd401ZS_time'] == "scan"
                else f"t={LACs583_time} ms")),
    dict(name="ZS 401", start=20, duration=10, group="Manipulation", 
         label=("t (scanned); "
                if flags['Ryd401ZS_time'] == "scan"
                else f"t={LACs583_time} ms; "
                f"P={Ryd401ZS_SP} mW, ")),
        #  label=(
        #     f"{'Scan ' if flags['Ryd401ZS_SP'] == 'scan' else ' '}"
        #     f"P={Ryd401ZS_SP} mW, "
        #     f"{'S ' if flags['Ryd401ZS_time'] == 'scan' else ''}"
        #     f"t={Ryd401ZS_time*1e3:.1f} µs")
        # ),
    # dict(name="ZS 401", start=20, duration=10, group="Manipulation", label=(
    #         f"{'Scan ' if flags['Ryd401ZS_SP'] == 'scan' else ' '}"
    #         f"P={Ryd401ZS_SP} mW, "
    #         f"{'S ' if flags['Ryd401ZS_time'] == 'scan' else ''}"
    #         f"t={Ryd401ZS_time*1e3:.1f} µs")
    #     ),
    dict(name="411", start=20, duration=10, group="Manipulation", label=f"P={PID411_SP} mW"),
]

if ImagingLight_wavelength == 1:
    steps.append(dict(name="Imaging (401)", start=35.005, duration=5, group="Readout", label="pulsed"))
elif ImagingLight_wavelength == 2:
    steps.append(dict(name="Imaging (583)", start=35.005, duration=5, group="Readout", label="XX ms"))

if OnOffTwduringRydbergTweezers == 0:
    steps.append(dict(name="Tweezers", start=20, duration=20, group="Prep", label=""))
else:
    steps.append(dict(name="Tweezers", start=30, duration=10, group="Prep", label="Recapture"))

if FieldIonize == 1:
    steps.append(dict(name="HV", start=30, duration=7, group="Optional", label=f"1400 Vpp, t={IonizationPulseDuration*1e3:.1f} µs"))

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
ax.set_title(f"Experiment date {date}, meas {meas_num}")
ax.invert_yaxis()
ax.set_xlim(0, 40)

# Legend
legend_patches = [mpatches.Patch(color=clr, label=grp) for grp, clr in colors.items()]
ax.legend(handles=legend_patches, loc='upper left')

plt.tight_layout()

# Save to file
#filename = f"date_{date}_meas_{meas_num}_timeline.pdf"
filename = f"date_{date}_meas_{meas_num}_timeline.png"
plt.savefig(filename, format="png")
print(f"✅ Saved to {filename}")

plt.show()