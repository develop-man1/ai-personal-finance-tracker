// ==========================
// Управление экранами
// ==========================

// Три экрана: auth (логин/регистрация), dashboard
function showScreen(screenId) {
  document.querySelectorAll(".screen").forEach((s) => s.classList.add("hidden"));
  document.getElementById(screenId).classList.remove("hidden");
}

function showError(elementId, message) {
  const el = document.getElementById(elementId);
  el.textContent = message;
  el.classList.remove("hidden");
}

function hideError(elementId) {
  document.getElementById(elementId).classList.add("hidden");
}

// ==========================
// Инициализация
// ==========================

document.addEventListener("DOMContentLoaded", async () => {
  // Если токен уже есть — сразу в дашборд
  if (getToken()) {
    try {
      await getMe(); // проверяем что токен валидный
      await loadDashboard();
      showScreen("screen-dashboard");
    } catch {
      // токен протух — на логин
      logout();
      showScreen("screen-auth");
    }
  } else {
    showScreen("screen-auth");
  }

  bindAuthEvents();
  bindDashboardEvents();
});

// ==========================
// Auth события
// ==========================

function bindAuthEvents() {
  // Переключение между логином и регистрацией
  document.getElementById("btn-show-register").addEventListener("click", () => {
    document.getElementById("form-login").classList.add("hidden");
    document.getElementById("form-register").classList.remove("hidden");
    hideError("auth-error");
  });

  document.getElementById("btn-show-login").addEventListener("click", () => {
    document.getElementById("form-register").classList.add("hidden");
    document.getElementById("form-login").classList.remove("hidden");
    hideError("auth-error");
  });

  // Логин
  document.getElementById("form-login").addEventListener("submit", async (e) => {
    e.preventDefault();
    hideError("auth-error");

    const username = document.getElementById("login-username").value.trim();
    const password = document.getElementById("login-password").value;

    try {
      await login(username, password);
      await loadDashboard();
      showScreen("screen-dashboard");
    } catch (err) {
      showError("auth-error", err.message);
    }
  });

  // Регистрация
  document.getElementById("form-register").addEventListener("submit", async (e) => {
    e.preventDefault();
    hideError("auth-error");

    const username = document.getElementById("reg-username").value.trim();
    const password = document.getElementById("reg-password").value;

    try {
      await register(username, password);
      // После регистрации сразу логиним
      await login(username, password);
      await loadDashboard();
      showScreen("screen-dashboard");
    } catch (err) {
      showError("auth-error", err.message);
    }
  });
}

// ==========================
// Dashboard
// ==========================

async function loadDashboard() {
  const [me, balance, categories, transactions] = await Promise.all([
    getMe(),
    getBalance(),
    getCategories(),
    getTransactions(),
  ]);

  // Имя пользователя
  document.getElementById("username-display").textContent = me.username;

  // Баланс
  document.getElementById("balance-total").textContent = formatMoney(balance.balance);
  document.getElementById("balance-income").textContent = formatMoney(balance.income);
  document.getElementById("balance-expense").textContent = formatMoney(balance.expense);

  // Список категорий в select
  renderCategorySelect(categories);

  // Список транзакций
  renderTransactions(transactions, categories);
}

function renderCategorySelect(categories) {
  const select = document.getElementById("tx-category");
  select.innerHTML = '<option value="">— Выберите категорию —</option>';
  categories.forEach((cat) => {
    const option = document.createElement("option");
    option.value = cat.id;
    option.textContent = `${cat.name} (${cat.type === "Income" ? "Доход" : "Расход"})`;
    select.appendChild(option);
  });
}

function renderTransactions(transactions, categories) {
  const list = document.getElementById("transactions-list");

  if (transactions.length === 0) {
    list.innerHTML = '<p class="empty-state">Транзакций пока нет</p>';
    return;
  }

  list.innerHTML = transactions
    .slice()
    .reverse() // новые сверху
    .map((tx) => {
      const cat = categories.find((c) => c.id === tx.category_id);
      const isIncome = cat?.type === "Income";
      const date = new Date(tx.date).toLocaleDateString("ru-RU");

      return `
      <div class="transaction-item" data-id="${tx.id}">
        <div class="tx-left">
          <span class="tx-category">${cat?.name || "—"}</span>
          <span class="tx-desc">${tx.description || ""}</span>
          <span class="tx-date">${date}</span>
        </div>
        <div class="tx-right">
          <span class="tx-amount ${isIncome ? "income" : "expense"}">
            ${isIncome ? "+" : "−"}${formatMoney(tx.amount)}
          </span>
          <button class="btn-delete" data-id="${tx.id}">✕</button>
        </div>
      </div>
    `;
    })
    .join("");

  // Удаление транзакции
  list.querySelectorAll(".btn-delete").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const id = btn.dataset.id;
      try {
        await deleteTransaction(id);
        await loadDashboard(); // перезагружаем всё
      } catch (err) {
        alert("Ошибка удаления: " + err.message);
      }
    });
  });
}

// ==========================
// Dashboard события
// ==========================

function bindDashboardEvents() {
  // Выход
  document.getElementById("btn-logout").addEventListener("click", () => {
    logout();
    showScreen("screen-auth");
  });

  // Создать транзакцию
  document.getElementById("form-transaction").addEventListener("submit", async (e) => {
    e.preventDefault();
    hideError("tx-error");

    const amount = parseFloat(document.getElementById("tx-amount").value);
    const categoryId = parseInt(document.getElementById("tx-category").value);
    const description = document.getElementById("tx-description").value.trim();

    if (!categoryId) {
      showError("tx-error", "Выберите категорию");
      return;
    }

    try {
      await createTransaction(amount, categoryId, description);
      document.getElementById("form-transaction").reset();
      await loadDashboard();
    } catch (err) {
      showError("tx-error", err.message);
    }
  });

  // Создать категорию
  document.getElementById("form-category").addEventListener("submit", async (e) => {
    e.preventDefault();
    hideError("cat-error");

    const name = document.getElementById("cat-name").value.trim();
    const type = document.getElementById("cat-type").value;

    try {
      await createCategory(name, type);
      document.getElementById("form-category").reset();
      await loadDashboard();
    } catch (err) {
      showError("cat-error", err.message);
    }
  });
}

// ==========================
// Утилиты
// ==========================

function formatMoney(amount) {
  return new Intl.NumberFormat("ru-RU", {
    style: "currency",
    currency: "RUB",
    maximumFractionDigits: 2,
  }).format(amount);
}