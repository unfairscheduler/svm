import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from svm import fit
from smo import SVM


def main():
    """
    points = pd.read_csv("data.csv")
    data = points.to_numpy()
    """
    points = []

    fig, ax = plt.subplots()
    ax.set_title("SVM")
    ax.set_xlim([0, 10])
    ax.set_ylim([0, 10])

    def on_plot_click(event, points):
        if event.button == 1:
            points.append((event.xdata, event.ydata, -1))
            ax.plot(event.xdata, event.ydata, "rx")
            fig.canvas.draw()
        elif event.button == 3:
            points.append((event.xdata, event.ydata, 1))
            ax.plot(event.xdata, event.ydata, "go")
            fig.canvas.draw()
        elif event.button == 2:
            points = []
            ax.cla()
            ax.set_title("SVM")
            ax.set_xlim([0, 10])
            ax.set_ylim([0, 10])
            fig.canvas.draw()
        
    def on_plot_keypress(event):
        if event.key == "enter":
            print(f"total points {len(points)}")

            data = np.array(points)
            np.random.seed(42)
            np.random.shuffle(data)
            X = data[:, 0:2]
            y = data[:, -1]

            w, b = fit(X, y)
            print(f"qp found\n {w}\nand\n{b}\n")

            xx = np.linspace(0, 10, 100)
            yy = -(w[0] / w[1]) * xx - (b / w[1])

            ax.plot(xx, yy, linestyle="dashdot", color="tab:blue", label="cvxopt")
            fig.canvas.draw()

            classifier = SVM(X, y, C=0.5)
            alpha_vector, bias = classifier.smo()
            smo_w = (X * (alpha_vector * y).reshape(y.shape[0], 1)).sum(axis=0)
            S = (alpha_vector > 1e-3).flatten()

            bias = np.mean(y[S] - np.dot(X[S], smo_w))

            print(f"smo_w found\n {smo_w}\nand\n{bias}")
            xxx = np.linspace(0, 10, 100)
            yyy = -(smo_w[0] / smo_w[1]) * xxx - bias / smo_w[1]

            ax.plot(xxx, yyy, linestyle="dashdot", color="purple", label="smo")
            plt.legend(loc="upper right")
            fig.canvas.draw()
    
    cid = fig.canvas.mpl_connect("button_press_event", lambda event: on_plot_click(event, points))
    cid2 = fig.canvas.mpl_connect("key_press_event", on_plot_keypress)

    plt.show()


if __name__ == "__main__":
    main()
