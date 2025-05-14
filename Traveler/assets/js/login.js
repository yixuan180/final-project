function showForm(type) {
  document.getElementById('login-form').style.display = 'none';
  document.getElementById('register-form').style.display = 'none';

  if (type === 'login') {
    document.getElementById('login-form').style.display = 'block';
  } else if (type === 'register') {
    document.getElementById('register-form').style.display = 'block';
  }
}
