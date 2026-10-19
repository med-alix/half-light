"""Chart one synthetic run from hearth_controller_test.json (dark game palette)."""
import json, numpy as np, datetime as dt, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BG, LINE, TXT, MUTED = "#14110f", "#4a3f37", "#f1e7dc", "#a8998b"
EMBER, WARDEN, DRIFTER, HEARTH, ICE = "#e8743b", "#3eb3a8", "#b08ce6", "#ffb35c", "#8fb8d8"
plt.rcParams.update({"font.size": 10, "axes.facecolor": BG, "figure.facecolor": BG, "axes.edgecolor": LINE,
                     "axes.labelcolor": MUTED, "xtick.color": MUTED, "ytick.color": MUTED, "text.color": TXT,
                     "axes.grid": True, "grid.color": "#2b2420", "grid.linewidth": 0.6, "legend.frameon": False})

J = json.load(open("hearth_controller_test.json"))
ex = J["example"]; d0 = dt.date.fromisoformat(J["day0"])
n = len(ex["none"]["tot"]); days = [d0 + dt.timedelta(3 * i) for i in range(n)]
floor = d0 + dt.timedelta(J["d_floor"]); tend = d0 + dt.timedelta(J["d_tend"])
sm = lambda x, k=10: np.convolve(x, np.ones(k) / k, mode="same")

fig, ax = plt.subplots(3, 1, figsize=(10, 8.6), sharex=True, gridspec_kw={"height_ratios": [2.2, 1.2, 1]})
a = ax[0]
a.semilogy(days, np.maximum(sm(ex["none"]["tot"]), 1e-3), color=MUTED, lw=1.2, label="no Granary")
a.semilogy(days, np.maximum(sm(ex["escrow"]["tot"]), 1e-3), color=ICE, lw=1.0, label="fixed rule, escrow pays")
a.semilogy(days, np.maximum(sm(ex["bots"]["tot"]), 1e-3), color=WARDEN, lw=2.6, label="auction only")
a.semilogy(days, np.maximum(sm(ex["hybrid"]["tot"]), 1e-3), color=HEARTH, lw=1.6, label="auction + small escrow (hybrid)")
a.set_ylabel("DBXen batches per cycle\n(today's normal = 1)")
a.set_title("One synthetic world: bull and bear cycles, DXN disinflation, AMP floor", color=TXT, loc="left")
a.legend(loc="lower left", fontsize=9)
b = ax[1]
w = np.array(ex["none"]["w"])
b.fill_between(days, 0, w, where=w < 0, color=ICE, alpha=0.5, lw=0)
b.fill_between(days, 0, w, where=w >= 0, color=EMBER, alpha=0.5, lw=0)
b.set_ylabel("weather w\n(burns per DXN: short vs long)"); b.set_ylim(-1, 1)
c = ax[2]
for k, col, lab, lw in [("escrow", ICE, "escrow", 1.4), ("bots", WARDEN, "auction only", 2.6), ("hybrid", HEARTH, "hybrid", 1.4)]:
    c.plot(days, ex[k]["G"], color=col, lw=lw, label=lab)
c.set_ylabel("Granary store\n(days of today's burns)"); c.legend(fontsize=9, loc="upper right")
for a_ in ax:
    a_.axvline(floor, color=MUTED, lw=1, ls=":"); a_.axvline(tend, color=MUTED, lw=1, ls=":")
ax[0].text(floor, ax[0].get_ylim()[1] * 0.6, " AMP = 1", color=MUTED)
ax[0].text(tend, ax[0].get_ylim()[1] * 0.6, " horizon", color=MUTED)
fig.tight_layout(); fig.savefig("hearth_controller_example.png", dpi=130)
print("saved")
