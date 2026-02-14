// ==========================
// Настройки
// ==========================

const API_URL = "http://localhost:8000";

// ==========================
// Хранение токена
// ==========================

function getToken() {
  return localStorage.getItem("access_token");
}

function saveToken(token) {
  localStorage.setItem("access_token", token);
}

function removeToken() {
  localStorage.removeItem("access_token");
}

// Заголовки для авторизованных запросов
function authHeaders() {
  return {
    "Content-Type": "application/json",
    Authorization: `Bearer ${getToken()}`,
  };
}

// ==========================
// Обработка ошибок
// ==========================

async function handleResponse(response) {
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Что-то пошло не так");
  }
  // 204 No Content — тело пустое
  if (response.status === 204) return null;
  return response.json();
}

// ==========================
// Auth
// ==========================

// POST /auth/register
async function register(username, password) {
  const response = await fetch(`${API_URL}/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });
  return handleResponse(response);
}

// POST /auth/login
// Логин требует form-data, не JSON — так работает OAuth2
async function login(username, password) {
  const formData = new URLSearchParams();
  formData.append("username", username);
  formData.append("password", password);

  const response = await fetch(`${API_URL}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: formData,
  });

  const data = await handleResponse(response);
  saveToken(data.access_token); // сохраняем токен
  return data;
}

function logout() {
  removeToken();
}

// ==========================
// Categories
// ==========================

// GET /categories/
async function getCategories() {
  const response = await fetch(`${API_URL}/categories/`, {
    headers: authHeaders(),
  });
  return handleResponse(response);
}

// POST /categories/
async function createCategory(name, type) {
  const response = await fetch(`${API_URL}/categories/`, {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify({ name, type }),
  });
  return handleResponse(response);
}

// ==========================
// Transactions
// ==========================

// GET /transactions/
async function getTransactions(category = null, dateFrom = null) {
  let url = `${API_URL}/transactions/`;
  const params = new URLSearchParams();
  if (category) params.append("category", category);
  if (dateFrom) params.append("date_from", dateFrom);
  if (params.toString()) url += `?${params.toString()}`;

  const response = await fetch(url, { headers: authHeaders() });
  return handleResponse(response);
}

// POST /transactions/
async function createTransaction(amount, categoryId, description = "") {
  const response = await fetch(`${API_URL}/transactions/`, {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify({
      amount,
      category_id: categoryId,
      description,
    }),
  });
  return handleResponse(response);
}

// DELETE /transactions/{id}
async function deleteTransaction(id) {
  const response = await fetch(`${API_URL}/transactions/${id}`, {
    method: "DELETE",
    headers: authHeaders(),
  });
  return handleResponse(response);
}

// GET /transactions/balance
async function getBalance() {
  const response = await fetch(`${API_URL}/transactions/balance`, {
    headers: authHeaders(),
  });
  return handleResponse(response);
}

// GET /users/me
async function getMe() {
  const response = await fetch(`${API_URL}/users/me`, {
    headers: authHeaders(),
  });
  return handleResponse(response);
}