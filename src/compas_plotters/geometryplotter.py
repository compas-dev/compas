import matplotlib.pyplot as plt

from compas_plotters import Artist

__all__ = ['GeometryPlotter']


class GeometryPlotter:
    """Plotter for the visualisation of COMPAS geometry.

    Parameters
    ----------
    view : tuple, optional
        The area of the axes that should be zoomed into view.
        DEfault is ``([-10, 10], [-3, 10])``.
    figsize : tuple, optional
        The size of the figure in inches.
        Default is ``(8, 5)``

    Attributes
    ----------

    Examples
    --------

    Notes
    -----

    """

    def __init__(self, view=[(-8, 16), (-5, 10)], figsize=(8, 5), dpi=100, bgcolor=(1.0, 1.0, 1.0), show_axes=False):
        self._show_axes = show_axes
        self._bgcolor = None
        self._viewbox = None
        self._axes = None
        self._artists = []
        self.viewbox = view
        self.figsize = figsize
        self.dpi = dpi
        self.bgcolor = bgcolor

    @property
    def viewbox(self):
        """([xmin, xmax], [ymin, ymax]): The area of the axes that is zoomed into view."""
        return self._viewbox

    @viewbox.setter
    def viewbox(self, view):
        xlim, ylim = view
        xmin, xmax = xlim
        ymin, ymax = ylim
        self._viewbox = [xmin, xmax], [ymin, ymax]

    @property
    def axes(self):
        """Returns the axes subplot matplotlib object.

        Returns
        -------
        Axes
            The matplotlib axes object.

        Notes
        -----
        For more info, see the documentation of the Axes class ([1]_) and the
        axis and tick API ([2]_).

        References
        ----------
        .. [1] https://matplotlib.org/api/axes_api.html
        .. [2] https://matplotlib.org/api/axis_api.html

        """
        if not self._axes:
            figure = plt.figure(facecolor=self.bgcolor,
                                figsize=self.figsize,
                                dpi=self.dpi)
            axes = figure.add_subplot(111, aspect='equal')
            if self.viewbox:
                xmin, xmax = self.viewbox[0]
                ymin, ymax = self.viewbox[1]
                axes.set_xlim(xmin, xmax)
                axes.set_ylim(ymin, ymax)
            axes.set_xscale('linear')
            axes.set_yscale('linear')
            if self._show_axes:
                axes.set_frame_on(True)
                # major_xticks = np.arange(0, 501, 20)
                # major_yticks = np.arange(0, 301, 20)
                # minor_xticks = np.arange(0, 501, 5)
                # minor_yticks = np.arange(0, 301, 5)
                # ax.tick_params(axis = 'both', which = 'major', labelsize = 6)
                # ax.tick_params(axis = 'both', which = 'minor', labelsize = 0)
                # ax.set_xticks(major_xticks)
                # ax.set_xticks(minor_yticks, minor = True)
                # ax.set_yticks(major_xticks)
                # ax.set_yticks(minor_yticks, minor = True)
                # axes.tick_params(labelbottom=False, labelleft=False)
                # axes.grid(axis='both', linestyle='--', linewidth=0.5, color=(0.7, 0.7, 0.7))
                axes.grid(False)
                axes.set_xticks([])
                axes.set_yticks([])
                axes.spines['top'].set_color('none')
                axes.spines['right'].set_color('none')
                axes.spines['left'].set_position('zero')
                axes.spines['bottom'].set_position('zero')
                axes.spines['left'].set_linestyle('-')
                axes.spines['bottom'].set_linestyle('-')
            else:
                axes.grid(False)
                axes.set_frame_on(False)
                axes.set_xticks([])
                axes.set_yticks([])
            axes.autoscale_view()
            plt.tight_layout()
            self._axes = axes
        return self._axes

    @property
    def figure(self):
        """Returns the matplotlib figure instance.

        Returns
        -------
        Figure
            The matplotlib figure instance.

        Notes
        -----
        For more info, see the figure API ([1]_).

        References
        ----------
        .. [1] https://matplotlib.org/2.0.2/api/figure_api.html

        """
        return self.axes.get_figure()

    @property
    def canvas(self):
        """Returns the canvas of the figure instance.
        """
        return self.figure.canvas

    @property
    def bgcolor(self):
        """Returns the background color.

        Returns
        -------
        str
            The color as a string (hex colors).

        """
        return self._bgcolor

    @bgcolor.setter
    def bgcolor(self, value):
        """Sets the background color.

        Parameters
        ----------
        value : str, tuple
            The color specififcation for the figure background.
            Colors should be specified in the form of a string (hex colors) or
            as a tuple of normalized RGB components.

        """
        self._bgcolor = value
        self.figure.set_facecolor(value)

    @property
    def title(self):
        """Returns the title of the plot.

        Returns
        -------
        str
            The title of the plot.

        """
        return self.figure.canvas.get_window_title()

    @title.setter
    def title(self, value):
        """Sets the title of the plot.

        Parameters
        ----------
        value : str
            The title of the plot.

        """
        self.figure.canvas.set_window_title(value)

    @property
    def artists(self):
        """list of :class:`compas_plotters.artists.Artist`"""
        return self._artists

    @artists.setter
    def artists(self, artists):
        self._artists = artists

    # =========================================================================
    # Methods
    # =========================================================================

    def pause(self, pause):
        if pause:
            plt.pause(pause)

    def zoom_extents(self):
        width, height = self.figsize
        fig_aspect = width / height
        data = []
        for artist in self.artists:
            data += artist.data
        x, y = zip(* data)
        xmin = min(x)
        xmax = max(x)
        ymin = min(y)
        ymax = max(y)
        xspan = xmax - xmin
        yspan = ymax - ymin
        data_aspect = xspan / yspan
        if data_aspect < fig_aspect:
            scale = fig_aspect / data_aspect
            self.axes.set_xlim(scale * (xmin - 0.1 * xspan), scale * (xmax + 0.1 * xspan))
            self.axes.set_ylim(ymin - 0.1 * yspan, ymax + 0.1 * yspan)
        else:
            scale = data_aspect / fig_aspect
            self.axes.set_xlim(xmin - 0.1 * xspan, xmax + 0.1 * xspan)
            self.axes.set_ylim(scale * (ymin - 0.1 * yspan), scale * (ymax + 0.1 * yspan))
        self.axes.autoscale_view()

    def add(self, item, artist=None, **kwargs):
        if not artist:
            artist = Artist.build(item, **kwargs)
        artist.plotter = self
        artist.draw()
        self._artists.append(artist)
        return artist

    def add_as(self, item, artist_type, **kwargs):
        artist = Artist.build_as(item, artist_type, **kwargs)
        artist.plotter = self
        artist.draw()
        self._artists.append(artist)
        return artist

    def add_from_list(self, items, **kwargs):
        artists = []
        for item in items:
            artist = self.add(item, **kwargs)
            artists.append(artist)
        return artists

    def find(self, item):
        for artist in self._artists:
            if item is artist.item:
                return artist

    def register_listener(self, listener):
        """Register a listener for pick events.

        Parameters
        ----------
        listener : callable
            The handler for pick events.

        Returns
        -------
        None

        Notes
        -----
        For more information, see the docs of ``mpl_connect`` ([1]_), and on event
        handling and picking ([2]_).

        References
        ----------
        .. [1] https://matplotlib.org/api/backend_bases_api.html#matplotlib.backend_bases.FigureCanvasBase.mpl_connect
        .. [2] https://matplotlib.org/users/event_handling.html

        """
        self.figure.canvas.mpl_connect('pick_event', listener)

    def draw(self, pause=None):
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()
        if pause:
            plt.pause(pause)

    def redraw(self, pause=None):
        """Updates and pauses the plot.

        Parameters
        ----------
        pause : float
            Ammount of time to pause the plot in seconds.

        """
        for artist in self._artists:
            artist.redraw()
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()
        if pause:
            plt.pause(pause)

    def show(self):
        """Displays the plot.

        """
        self.draw()
        plt.show()

    def save(self, filepath, **kwargs):
        """Saves the plot to a file.

        Parameters
        ----------
        filepath : str
            Full path of the file.

        Notes
        -----
        For an overview of all configuration options, see [1]_.

        References
        ----------
        .. [1] https://matplotlib.org/2.0.2/api/pyplot_api.html#matplotlib.pyplot.savefig

        """
        plt.savefig(filepath, **kwargs)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
