import customtkinter as ctk
from components.cell_widget import CellWidget
from models.grid_model      import GridModel

BG_MAIN          = "#1a1a2e"
BG_HEADER        = "#12122a"
BG_BAR           = "#12122a"
FG_HEADER        = "#5a5a8a"
FG_REF           = "#7b8cde"
FG_FX            = "#7b8cde"
FG_INPUT         = "#e0e0ff"
BORDER           = "#2a2a4a"
BG_HEADER_ACTIVE = "#1c1c40"
FG_HEADER_ACTIVE = "#9090cc"


class FormulaBar(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=BG_BAR, height=34, corner_radius=0)
        self.grid_propagate(False)
        self.grid_columnconfigure(3, weight=1)

        self.ref_label = ctk.CTkLabel(
            self, text="A1", width=50,
            font=("Courier New", 12, "bold"),
            text_color=FG_REF, fg_color=BG_BAR,
        )
        self.ref_label.grid(row=0, column=0, padx=(10, 6), pady=6)

        sep = ctk.CTkFrame(self, width=1, height=20, fg_color=BORDER)
        sep.grid(row=0, column=1, padx=(0, 6), pady=6)

        fx = ctk.CTkLabel(self, text="fx", width=20,
                          font=("Georgia", 13, "italic"),
                          text_color=FG_FX, fg_color=BG_BAR)
        fx.grid(row=0, column=2, padx=(0, 4), pady=6, sticky="w")

        self.formula_label = ctk.CTkLabel(
            self, text="", anchor="w",
            font=("Courier New", 12),
            text_color=FG_INPUT, fg_color=BG_BAR,
        )
        self.formula_label.grid(row=0, column=3, padx=(0, 10), pady=6, sticky="ew")

    def update(self, ref: str, raw: str):
        self.ref_label.configure(text=ref)
        self.formula_label.configure(text=raw or "")


class HeaderCell(ctk.CTkLabel):
    def __init__(self, parent, text, is_corner=False, **kw):
        super().__init__(
            parent,
            text=text,
            font=("Courier New", 11, "bold"),
            text_color=FG_HEADER,
            fg_color=BG_HEADER,
            width=38 if is_corner else 0,
            anchor="center",
            **kw,
        )

    def set_active(self, active: bool):
        self.configure(
            fg_color=BG_HEADER_ACTIVE if active else BG_HEADER,
            text_color=FG_HEADER_ACTIVE if active else FG_HEADER,
        )


class GridView(ctk.CTkFrame):
    def __init__(self, parent, rows=10, cols=10):
        super().__init__(parent, fg_color=BG_MAIN, corner_radius=0)
        self.rows        = rows
        self.cols        = cols
        self.grid_model  = GridModel(rows, cols)
        self.cells: dict[str, CellWidget]  = {}
        self.col_headers: list[HeaderCell] = []
        self.row_headers: list[HeaderCell] = []
        self._active_r   = 0
        self._active_c   = 0

        self._build_formula_bar()
        self._build_grid()
        self.after(100, lambda: self._focus_cell(0, 0))

    # ── construcción ─────────────────────────────────────

    def _build_formula_bar(self):
        self.formula_bar = FormulaBar(self)
        self.formula_bar.grid(row=0, column=0, sticky="ew")
        self.grid_columnconfigure(0, weight=1)

    def _build_grid(self):
        container = ctk.CTkFrame(self, fg_color=BG_MAIN, corner_radius=0)
        container.grid(row=1, column=0, sticky="nsew")
        self.grid_rowconfigure(1, weight=1)

        container.grid_columnconfigure(0, minsize=38)
        for c in range(self.cols):
            container.grid_columnconfigure(c + 1, weight=1, minsize=70)

        # encabezados de columna
        HeaderCell(container, "", is_corner=True).grid(
            row=0, column=0, sticky="nsew", padx=(0, 1), pady=(0, 1))
        for c in range(self.cols):
            h = HeaderCell(container, self._col_letter(c))
            h.grid(row=0, column=c + 1, sticky="nsew", padx=(0, 1), pady=(0, 1))
            self.col_headers.append(h)

        # filas de datos
        for r in range(self.rows):
            container.grid_rowconfigure(r + 1, weight=1, minsize=30)
            rh = HeaderCell(container, str(r + 1), is_corner=True)
            rh.grid(row=r + 1, column=0, sticky="nsew", padx=(0, 1), pady=(0, 1))
            self.row_headers.append(rh)

            for c in range(self.cols):
                ref  = f"{self._col_letter(c)}{r+1}"
                cell = CellWidget(
                    container, ref,
                    on_change=self._on_cell_change,
                    on_select=self._on_cell_select,
                    on_navigate=self._on_navigate,
                )
                cell._get_cell_cb = self.grid_model.get_cell
                cell.grid(row=r + 1, column=c + 1, sticky="nsew",
                          padx=(0, 1), pady=(0, 1))
                self.cells[ref] = cell

    # ── navegación ────────────────────────────────────────

    def _on_navigate(self, from_ref: str, direction: str, raw_value=None):
        """
        El widget ya desactivó su estilo y nos pasa el raw_value si cambió.
        1. Evaluamos el modelo si hay cambio.
        2. Refrescamos todo (incluyendo from_ref, que ya no tiene foco).
        3. Movemos el foco.
        """
        if raw_value is not None:
            self.grid_model.set_cell(from_ref, raw_value)

        self._refresh_all()

        r, c = self._ref_to_rc(from_ref)
        deltas = {"up": (-1,0), "down": (1,0), "left": (0,-1), "right": (0,1)}
        dr, dc = deltas.get(direction, (0, 0))
        new_r  = max(0, min(self.rows - 1, r + dr))
        new_c  = max(0, min(self.cols - 1, c + dc))
        self._focus_cell(new_r, new_c)

    def _focus_cell(self, r: int, c: int):
        self._update_headers(r, c)
        ref    = f"{self._col_letter(c)}{r+1}"
        widget = self.cells.get(ref)
        if widget:
            widget.focus_set()
            self._active_r = r
            self._active_c = c

    def _update_headers(self, r: int, c: int):
        if 0 <= self._active_c < len(self.col_headers):
            self.col_headers[self._active_c].set_active(False)
        if 0 <= self._active_r < len(self.row_headers):
            self.row_headers[self._active_r].set_active(False)
        if 0 <= c < len(self.col_headers):
            self.col_headers[c].set_active(True)
        if 0 <= r < len(self.row_headers):
            self.row_headers[r].set_active(True)

    # ── callbacks del modelo ──────────────────────────────

    def _on_cell_change(self, ref: str, raw_value: str):
        """
        Llamado por FocusOut normal (click en otro lado, no navegación por teclado).
        El widget ya no tiene foco aquí, así que podemos refrescar todo.
        """
        self.grid_model.set_cell(ref, raw_value)
        self._refresh_all()

    def _on_cell_select(self, ref: str, raw_value: str):
        self.formula_bar.update(ref, raw_value)
        r, c = self._ref_to_rc(ref)
        self._update_headers(r, c)
        self._active_r = r
        self._active_c = c

    # ── refresco ──────────────────────────────────────────

    def _refresh_all(self):
        """Refresca todas las celdas sin excepción."""
        for ref, widget in self.cells.items():
            cell = self.grid_model.get_cell(ref)
            widget.set_display(cell.value, cell.type or "")

    # ── utilidades ────────────────────────────────────────

    def _ref_to_rc(self, ref: str) -> tuple[int, int]:
        import re
        m = re.match(r'^([A-Z]+)(\d+)$', ref)
        if not m:
            return 0, 0
        col_str, row_str = m.groups()
        col = 0
        for ch in col_str:
            col = col * 26 + (ord(ch) - ord('A') + 1)
        return int(row_str) - 1, col - 1

    @staticmethod
    def _col_letter(idx: int) -> str:
        result = ""
        idx += 1
        while idx:
            idx, rem = divmod(idx - 1, 26)
            result = chr(ord('A') + rem) + result
        return result