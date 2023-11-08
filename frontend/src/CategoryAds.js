import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import axios from 'axios';


const CategoryAds = () => {
    const { id } = useParams();
    const [dataList, setDataList] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await axios.get(`http://127.0.0.1:8000/api/v1/ads-categories/${id}/`);
                setDataList(response.data);
            } catch (error) {
                console.error(error);
            }
        };

        fetchData();
    }, [id]);


    return (
        <div>
            {dataList.map((data) => (
                <div key={id} className="card">
                    <img src={data.img} alt={data.title} className="card-image" key={id} />

                    <div className="card-content">
                        <h2 className="card-title">{data.title}</h2>
                        <p className="card-description">Город: {data.city}</p>
                        <p className="card-price">Цена: {data.price} RUB</p>
                        <Link to={`/detail/${data.id}`}>Подробнее</Link>
                    </div>
                </div>
            ))}
        </div>
    );
};

export default CategoryAds;