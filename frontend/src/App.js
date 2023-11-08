import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';

import Home from './Home';
import Login from './Login';
import Register from './Register';
import Detail from './Detail';
import CategoryAds from './CategoryAds';

function App() {
  const [isLoggedIn, setLoggedIn] = useState(false);

  useEffect(() => {
    const checkLoginStatus = async () => {
      const token = localStorage.getItem('access_token');

      if (token) {
        try {
          const response = await axios.get(
            'http://127.0.0.1:8000/api/v1/check_login/',
            {
              headers: {
                Authorization: `Token ${token}`,
              },
            }
          );
          setLoggedIn(response.data.authenticated);

        } catch (error) {
          console.error(error);
          // Обработка ошибки авторизации
        }
      }
    };

    checkLoginStatus();
  }, []);

  const handleLogout = () => {
    setLoggedIn(false);
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');


  };



  return (
    <Router>
      <header>
        <div className='header'>

          <p className='logo'>Логотип</p>
          <CategoryList />

          <div className='div-check'>

            <div>
              <Link className='active' to="/">Главная</Link>
            </div>
            {isLoggedIn ? (
              <div className='chek-auth'>
                <p className='p-div'>Вы вошли в систему</p>
                <Link className='active-check' to="/" onClick={handleLogout}>
                  Выход
                </Link>
              </div>
            ) : (
              <div className='chek-auth'>
                <p className='p-div'>Вы не вошли в систему</p>
                <Link className='active-check' to="/auth">Войти</Link>
              </div>
            )}
          </div>
        </div>
      </header>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/auth" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/detail/:id" element={<Detail />} />
        <Route path="/category/:id" element={<CategoryAds />} />
      </Routes>
    </Router>
  );
}

export default App;



class CategoryList extends React.Component {
  state = { details: [], }
  componentDidMount() {
    let data;
    axios.get('http://127.0.0.1:8000/api/v1/categories/').then(res => { data = res.data; this.setState({ details: data }); }).catch(err => { })

  }
  render() {
    return (

      <div className='category-list'>
        {this.state.details.map((output, id) => (
          <div key={id} >
            <div>
              <Link className='category' to={`/category/${output.id}`}>{output.title}</Link>
            </div>
          </div>
        ))}
      </div>
    );
  }
}