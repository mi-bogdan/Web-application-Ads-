import React from 'react';
import axios from 'axios'
import './style.css';
import Detail from './Detail';

import { BrowserRouter as Router, Switch, Route, Link, Routes } from 'react-router-dom';


class Home extends React.Component {
    state = { details: [], }
    componentDidMount() {
        let data;
        axios.get('http://127.0.0.1:8000/api/v1/ads/').then(res => { data = res.data; this.setState({ details: data }); }).catch(err => { })

    }
    
    render() {
        return (

            <div className='container'>

                {this.state.details.map((output, id) => (
                    <div key={id} className="card">
                        <img src={`http://localhost:8000${output.img}`} alt={output.title} className="card-image" key={id} />

                        <div className="card-content">
                            <h2 className="card-title">{output.title}</h2>
                            <p className="card-description">Город: {output.city}</p>
                            <p className="card-price">Цена: {output.price} RUB</p>
                            <Link to={`/detail/${output.id}`}>Подробнее</Link>
                        </div>
                    </div>
                ))}

              

            </div>

     
        );
    }

}

export default Home;