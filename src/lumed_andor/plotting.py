import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np

from lumed_andor.andor_control import MultiTrack, RandomTrack, SingleTrack


class AndorPlot:
    def __init__(self, data: np.ndarray):
        self.data = data
        self.n_figures = self.get_figure_number()
        self.is_image_plot: bool = self.data_is_image()
        self.figures: list[plt.figure] = []

    def get_figure_number(self) -> int:
        n, y, _ = self.data.shape

        if y == 1:
            return 1

        return n

    def data_is_image(self) -> bool:
        _, y, _ = self.data.shape

        return y != 1

    def plot_data(self, fig_width=12):

        self.figures = []
        for i in range(self.n_figures):

            if self.is_image_plot:
                # Create figure
                im = self.data[i, :, :]
                fig_width = 12
                nx, ny = im.shape
                fig_height = max(fig_width * nx / ny, 0.1 * fig_width)
                fig = plt.figure(figsize=(fig_width, fig_height))

                # Plot images
                self.plot_image(im, fig)
                fig.show()
            else:
                spectra = self.data[:, 0, :]
                fig = self.plot_spectra(spectra)

            self.figures.append(fig)

    def plot_spectra(self, spectra) -> plt.figure:
        fig = plt.figure()
        for spectrum in spectra:
            plt.plot(spectrum)
        fig.show()

        return fig

    def plot_image(self, im, fig):
        nx, ny = im.shape

        # spacing for the axes
        left, width = 0.1, 0.65
        bottom, height = 0.1, 0.65
        spacing = 0

        rect_im = [left, bottom, width, height]
        rect_sumx = [left, bottom + height + spacing, width, 0.2]
        rect_sumy = [left + width + spacing, bottom, 0.2, height]

        # Add Axes
        ax_img = fig.add_axes(rect_im)
        ax_img.tick_params(direction="in", top=True, right=True)
        ax_sumx = fig.add_axes(rect_sumx)
        ax_sumx.tick_params(direction="in", labelbottom=False)
        ax_sumy = fig.add_axes(rect_sumy)
        ax_sumy.tick_params(direction="in", labelleft=False)

        # Plot axes
        ax_img.imshow(im, aspect="auto", interpolation="None")
        ax_sumx.plot(range(ny), im.sum(axis=0))
        ax_sumy.plot(im.sum(axis=1), range(nx))

        # Ajust axes
        ax_sumx.sharex(ax_img)
        ax_sumy.sharey(ax_img)
        ax_sumx.set_yticks([])
        ax_sumy.set_xticks([])

    def plot_fvb_bounds(self):
        if not self.is_image_plot:
            return

        fig = self.figures[0]
        ax_img: plt.axes = fig.get_axes()[0]
        y2, y1 = ax_img.get_ylim()
        height = y2 - y1
        center = height // 2
        self.plot_singletrack_bounds(
            single_track=SingleTrack(center=center, height=height)
        )

    def plot_singletrack_bounds(self, single_track: SingleTrack):
        if not self.is_image_plot:
            return

        height = single_track.height
        center = single_track.center - 1

        for im, fig in zip(self.data, self.figures):
            fig.clear()

            y1 = center - height // 2
            y2 = center + height // 2
            x1 = 0
            x2 = im.shape[1]
            self.plot_image(im, fig)
            self.plot_bounds(fig, xs=[x1, x2], ys=[y1, y2])

            fig.canvas.draw()

    def plot_multitrack_bounds(self, multi_track: MultiTrack):
        if not self.is_image_plot:
            return

        n_track = multi_track.number
        bottom = multi_track.bottom
        gap = multi_track.gap
        height = multi_track.height

        for im, fig in zip(self.data, self.figures):
            fig.clear()

            x1 = 0
            x2 = im.shape[1]
            self.plot_image(im, fig)

            for i in range(n_track):
                y1 = i * (gap + height) + bottom
                y2 = y1 + height
                self.plot_bounds(fig, xs=[x1, x2], ys=[y1, y2])

            fig.canvas.draw()

    def plot_randomtrack_bounds(self, random_track: RandomTrack):
        if not self.is_image_plot:
            return

        for im, fig in zip(self.data, self.figures):
            fig.clear()

            x1 = 0
            x2 = im.shape[1]
            self.plot_image(im, fig)

            tracks = random_track.tracks

            for i in range(0, len(tracks), 2):
                y1, y2 = tracks[i : i + 2]
                self.plot_bounds(fig, xs=[x1, x2], ys=[y1, y2])

            fig.canvas.draw()

    def plot_bounds(self, fig: plt.figure, xs: tuple[int, int], ys: tuple[int, int]):
        x1, x2 = xs
        y1, y2 = ys

        x1 = x1 - 0.5
        x2 = x2 + 0.5
        y1 = y1 - 0.5
        y2 = y2 + 0.5

        # Add patch to image
        ax_img: plt.axes = fig.get_axes()[0]
        og_ylim = ax_img.get_ylim()
        og_xlim = ax_img.get_xlim()

        # Create a red rectangle patch
        red_square = patches.Rectangle(
            (x1, y1),
            width=x2 - x1,
            height=y2 - y1,
            linewidth=4,
            edgecolor=[1, 0, 0, 1],
            facecolor=[1, 0, 0, 0.3],
        )
        ax_img.add_patch(red_square)
        ax_img.set_xlim(og_xlim)
        ax_img.set_ylim(og_ylim)

        # Add lines to xhist
        ax_sumx: plt.axes = fig.get_axes()[2]
        og_ylim = ax_sumx.get_ylim()
        og_xlim = ax_sumx.get_xlim()

        ax_sumx.plot(og_xlim, [y1, y1], color="red")
        ax_sumx.plot(og_xlim, [y2, y2], color="red")

        ax_sumx.set_xlim(og_xlim)
        ax_sumx.set_ylim(og_ylim)


if __name__ == "__main__":

    data_ = np.random.rand(1, 256, 1024)

    andor_plot = AndorPlot(data_)
    andor_plot.plot_data()
    # andor_plot.plot_singletrack_bounds(SingleTrack(center=128, height=20))

    # andor_plot.plot_multitrack_bounds(MultiTrack(number=2, height=100, gap=1))
    andor_plot.plot_randomtrack_bounds(RandomTrack(tracks=[1, 12, 13, 44]))

    plt.show()
