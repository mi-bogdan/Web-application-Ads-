import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate, Link } from 'react-router-dom';

function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    const body = { email, password };

    try {
      const response = await axios.post(
        'http://127.0.0.1:8000/auth/token/login/',
        body
      );
      console.log(response.data);

      if (response.data.auth_token) {
        localStorage.setItem('access_token', response.data.auth_token);
        navigate('/');
        window.location.reload();
      }
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>Авторизация</h1>
      <form onSubmit={handleSubmit} style={styles.form}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          style={styles.input}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          style={styles.input}
        />
        <input
          type="submit"
          value="Войти"
          style={styles.loginButton}
        />
      </form>
      <Link
        to="/register"
        style={styles.registerLink}
      >
        Зарегистрироваться
      </Link>
    </div>
  );
}

const styles = {
  container: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    height: '100vh',
    backgroundColor: '#f2f2f2',
  },
  title: {
    fontSize: 32,
    marginBottom: 16,
  },
  form: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    marginBottom: 16,
  },
  input: {
    padding: 8,
    marginBottom: 8,
    width: 300,
    fontSize: 16,
    border: 'none',
    borderBottom: '1px solid #ccc',
    outline: 'none',
  },
  loginButton: {
    padding: '8px 16px',
    fontSize: 16,
    backgroundColor: '#007bff',
    color: '#fff',
    border: 'none',
    borderRadius: 4,
    cursor: 'pointer',
  },
  registerLink: {
    fontSize: 14,
    color: '#007bff',
    textDecoration: 'none',
    marginTop: 8,
  },
};

export default Login;