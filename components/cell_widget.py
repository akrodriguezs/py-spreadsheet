import customtkinter as ctk

C = {
    "bg":           "#1e1e38",
    "bg_active":    "#1e2a4a",
    "border":       "#2a2a4a",
    "border_active":"#4a7aff",
    "border_hover": "#3a3a6a",
    # colores de display (valor calculado)
    "col_number":   "#c9d4ff",
    "col_formula":  "#78d5b0",
    "col_text":     "#f0c070",
    "col_error":    "#ff6060",
    "col_empty":    "#3a3a6a",
    # color al escribir — blanco puro, máximo contraste
    "col_editing":  "#ffffff",
}

def _format_number(v) -> str:
    if isinstance(v, float):
        if v == int(v):
            return str(int(v))
        return f"{v:.6g}"
    return str(v)


class CellWidget(ctk.CTkEntry):
    def __init__(self, parent, ref: str, on_change, on_select=None, on_navigate=None):
        super().__init__(
            parent,
            height=30,
            corner_radius=0,
            border_width=1,
            justify="center",
            font=("Courier New", 12),
            fg_color=C["bg"],
            border_color=C["border"],
            text_color=C["col_empty"],
        )
        self.ref         = ref
        self.on_change   = on_change
        self.on_select   = on_select
        self.on_navigate = on_navigate
        self.raw_value   = ""
        self._focused    = False
        self._get_cell_cb = None

        self.bind("<FocusIn>",      self._on_focus_in)
        self.bind("<FocusOut>",     self._on_focus_out)
        self.bind("<Enter>",        self._on_hover)
        self.bind("<Leave>",        self._on_leave)
        # cualquier tecla que el usuario escriba → poner color de edición
        self.bind("<Key>",          self._on_key)

        self.bind("<Return>",       self._nav_down)
        self.bind("<Shift-Return>", self._nav_up)
        self.bind("<Tab>",          self._nav_right)
        self.bind("<Shift-Tab>",    self._nav_left)
        self.bind("<Up>",           self._nav_up)
        self.bind("<Down>",         self._nav_down)
        self.bind("<Left>",         self._nav_left_arrow)
        self.bind("<Right>",        self._nav_right_arrow)
        self.bind("<Escape>",       self._on_escape)
        self.bind("<Delete>",       self._on_delete_key)

    # ── estilo de foco ────────────────────────────────────

    def _apply_focused_style(self):
        self.configure(
            border_width=2,
            border_color=C["border_active"],
            fg_color=C["bg_active"],
            text_color=C["col_editing"],   # blanco al entrar
        )

    def _apply_idle_style(self):
        self.configure(
            border_width=1,
            border_color=C["border"],
            fg_color=C["bg"],
        )
        # el color de texto lo pone set_display() después

    # ── eventos de foco ───────────────────────────────────

    def _on_focus_in(self, event):
        self._focused = True
        self._apply_focused_style()
        self.delete(0, "end")
        self.insert(0, self.raw_value)
        if self.on_select:
            self.on_select(self.ref, self.raw_value)

    def _on_focus_out(self, event):
        """
        FocusOut siempre limpia el estilo y guarda.
        Esto cubre el caso de click con mouse a otra celda.
        La navegación por teclado ya guardó antes de llamar focus_set(),
        así que _save() aquí es un no-op si raw_value no cambió.
        """
        self._focused = False
        self._apply_idle_style()
        self._save()

    def _on_key(self, event):
        """Mientras el usuario escribe, mantener texto blanco."""
        if self._focused:
            self.configure(text_color=C["col_editing"])

    def _on_hover(self, event):
        if not self._focused:
            self.configure(border_color=C["border_hover"])

    def _on_leave(self, event):
        if not self._focused:
            self.configure(border_color=C["border"])

    # ── guardado ──────────────────────────────────────────

    def _save(self):
        current = self.get().strip()
        if current == self.raw_value:
            return
        self.raw_value = current
        self.on_change(self.ref, current)

    # ── navegación ────────────────────────────────────────

    def _nav(self, direction: str):
        """
        Guarda el valor actual ANTES de mover el foco,
        y desactiva el estilo para que no quede atascado.
        """
        current = self.get().strip()
        changed = current != self.raw_value
        if changed:
            self.raw_value = current

        # quitar estilo activo inmediatamente
        self._focused = False
        self._apply_idle_style()

        if self.on_navigate:
            # pasamos el valor crudo para que el grid lo evalúe
            self.on_navigate(self.ref, direction, current if changed else None)
        return "break"

    def _nav_down(self,  event): return self._nav("down")
    def _nav_up(self,    event): return self._nav("up")
    def _nav_right(self, event): return self._nav("right")
    def _nav_left(self,  event): return self._nav("left")

    def _nav_left_arrow(self, event):
        try:
            idx = self.index("insert")
        except Exception:
            idx = 0
        if idx == 0:
            return self._nav("left")

    def _nav_right_arrow(self, event):
        try:
            idx = self.index("insert")
            end = len(self.get())
        except Exception:
            idx, end = 0, 0
        if idx >= end:
            return self._nav("right")

    # ── escape y delete ───────────────────────────────────

    def _on_escape(self, event):
        self._focused = False
        self._apply_idle_style()
        # restaurar display del modelo
        if self._get_cell_cb:
            cell = self._get_cell_cb(self.ref)
            self.set_display(cell.value, cell.type or "")
        self.master.focus_set()
        return "break"

    def _on_delete_key(self, event):
        if len(self.get()) > 0:
            return None
        self.raw_value = ""
        self.on_change(self.ref, "")
        return "break"

    # ── display ───────────────────────────────────────────

    def set_display(self, value, cell_type: str):
        """Muestra el valor calculado. Solo se llama cuando la celda NO está en foco."""
        self.delete(0, "end")
        if value is None:
            self.configure(text_color=C["col_empty"])
            return
        display = _format_number(value) if cell_type != "text" else str(value)
        self.insert(0, display)
        color_map = {
            "number":  C["col_number"],
            "formula": C["col_formula"],
            "text":    C["col_text"],
            "error":   C["col_error"],
        }
        self.configure(text_color=color_map.get(cell_type, C["col_empty"]))