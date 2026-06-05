document.addEventListener("DOMContentLoaded", () => {
    const FLASH_DURATION = 2000;

    function dismissFlash(flash) {
        flash.classList.add("flash-hide");
        setTimeout(() => {
            flash.remove();
            const container = document.querySelector(".flash-messages");
            if (container && container.children.length === 0) {
                container.remove();
            }
        }, 300);
    }

    document.querySelectorAll(".flash").forEach((flash) => {
        const closeBtn = flash.querySelector(".flash-close");
        let timer = setTimeout(() => dismissFlash(flash), FLASH_DURATION);

        closeBtn?.addEventListener("click", () => {
            clearTimeout(timer);
            dismissFlash(flash);
        });
    });

    const loginNotice = document.getElementById("login-notice");
    const loginNoticeClose = loginNotice?.querySelector(".login-notice-close");

    if (loginNotice && sessionStorage.getItem("login-notice-dismissed") === "1") {
        loginNotice.hidden = true;
    }

    loginNoticeClose?.addEventListener("click", () => {
        loginNotice.hidden = true;
        sessionStorage.setItem("login-notice-dismissed", "1");
    });

    function updateCartCount(count) {
        const navCart = document.getElementById("nav-cart-count");
        if (navCart) {
            navCart.textContent = `Carrinho (${count})`;
        }
    }

    document.querySelectorAll(".add-cart-form").forEach((form) => {
        form.addEventListener("submit", async (event) => {
            event.preventDefault();

            const button = form.querySelector("button[type=submit]");
            const originalText = button.textContent;
            button.disabled = true;
            button.textContent = "Adicionando...";

            try {
                const response = await fetch(form.action, {
                    method: "POST",
                    headers: { "X-Requested-With": "XMLHttpRequest" },
                });
                const data = await response.json();

                if (data.success) {
                    const sidebarContainer = document.getElementById("cart-sidebar-container");
                    if (sidebarContainer && data.sidebar_html) {
                        sidebarContainer.innerHTML = data.sidebar_html;
                    }
                    updateCartCount(data.cart_count);
                } else {
                    alert(data.message);
                }
            } catch {
                alert("Erro ao adicionar ao carrinho.");
            } finally {
                button.disabled = false;
                button.textContent = originalText;
            }
        });
    });
});
