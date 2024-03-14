import { showResponse } from "./showResponse.mjs";
const loginForm = document.querySelector('#login_form')
const data = {}

loginForm.addEventListener('submit', async (e) => {
  e.preventDefault()
  const inputs = document.querySelectorAll('input');
  inputs.forEach(input => {
    data[input.id] = input.value
  });
  try {
    const { responseData, statusCode } = await login(data);
    showResponse(responseData, statusCode);
  } catch (error) {
    console.error(error);
  }
})

async function login(loginData) {
  const url = "/api/auth/login";
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRF-Token": String(loginData.token)
    },
    body: JSON.stringify({
      'login_name': loginData.login_name,
      'login_password': loginData.login_password
    })
  });

  const responseData = await response.json();
  const statusCode = response.status;

  return { responseData, statusCode };
}