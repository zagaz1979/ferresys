// ============================================================
// FerreSys - Lógica de interfaz para el módulo de ventas
// ============================================================
(function () {
    "use strict";

    if (!window.FERRESYS_VENTAS) return;

    const tbody = document.getElementById("lineas");
    const btnAgregar = document.getElementById("btn-agregar-linea");
    const totalCell = document.getElementById("total-venta");

    function crearLinea() {
        const plantilla = tbody.querySelector(".linea");
        const clon = plantilla.cloneNode(true);
        clon.querySelector("select").value = "";
        clon.querySelector(".inp-cantidad").value = 1;
        clon.querySelector(".precio-unit").textContent = "$0.00";
        clon.querySelector(".subtotal").textContent = "$0.00";
        return clon;
    }

    function recalcularFila(fila) {
        const sel = fila.querySelector(".sel-producto");
        const cant = parseInt(fila.querySelector(".inp-cantidad").value, 10) || 0;
        const opt = sel.options[sel.selectedIndex];
        const precio = opt && opt.dataset.precio ? parseFloat(opt.dataset.precio) : 0;
        const subtotal = precio * cant;
        fila.querySelector(".precio-unit").textContent = "$" + precio.toFixed(2);
        fila.querySelector(".subtotal").textContent = "$" + subtotal.toFixed(2);
        return subtotal;
    }

    function recalcularTotal() {
        let total = 0;
        tbody.querySelectorAll(".linea").forEach(function (fila) {
            total += recalcularFila(fila);
        });
        totalCell.innerHTML = "<strong>$" + total.toFixed(2) + "</strong>";
    }

    // Delegación de eventos
    tbody.addEventListener("change", function (e) {
        if (e.target.classList.contains("sel-producto") ||
            e.target.classList.contains("inp-cantidad")) {
            recalcularTotal();
        }
    });

    tbody.addEventListener("input", function (e) {
        if (e.target.classList.contains("inp-cantidad")) {
            recalcularTotal();
        }
    });

    tbody.addEventListener("click", function (e) {
        if (e.target.classList.contains("btn-quitar")) {
            const filas = tbody.querySelectorAll(".linea");
            if (filas.length > 1) {
                e.target.closest(".linea").remove();
                recalcularTotal();
            } else {
                alert("Debe haber al menos una línea.");
            }
        }
    });

    btnAgregar.addEventListener("click", function () {
        tbody.appendChild(crearLinea());
        recalcularTotal();
    });

    // Validación antes de enviar
    document.getElementById("venta-form").addEventListener("submit", function (e) {
        const filas = tbody.querySelectorAll(".linea");
        let valido = false;
        for (const fila of filas) {
            const pid = fila.querySelector(".sel-producto").value;
            const cant = parseInt(fila.querySelector(".inp-cantidad").value, 10);
            if (pid && cant > 0) { valido = true; break; }
        }
        if (!valido) {
            e.preventDefault();
            alert("Debes agregar al menos un producto con cantidad mayor a 0.");
        }
    });
})();
