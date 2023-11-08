import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import moment from 'moment';

const Detail = () => {
    const { id } = useParams();
    const [news, setNews] = useState(null);

    useEffect(() => {
        axios.get(`http://127.0.0.1:8000/api/v1/ads/${id}/`)
            .then(response => {
                const data = response.data;
                setNews(data);
            })
            .catch(error => {
                console.error(error);
            });
    }, [id]);

    if (news === null) {
        return <h2>Loading...</h2>;
    }
    const formattedDate = moment(news.create_at).format("D MMMM YYYY");

    return (
        <div>
            <div className="container-detail">
                <h1>{news.title}</h1>
                <img className='img-detail' src={`http://localhost:8000${news.img}`} alt="Ad Image"></img>
                <div className='div-detail'>
                    <p className='p-detail'>Просмотров: {news.count_views}</p>
                    <p className='p-detail'>Город: {news.city}</p>
                </div>
                <p>{news.descriptions}</p>
                <p className="price">Цена: {news.price} рублей</p>
                <p className="telephone">Телефон: {news.telephone}</p>
                <p className="date">Дата публикации: {formattedDate}</p>

                <h2>Комментарии</h2>
                <CommentForm advertisementId={id} />
                {news.comments.map((comment, index) => (
                    <Comment key={index} comment={comment} />
                ))}
            </div>

        </div>
    );
};

export default Detail;

const Comment = ({ comment }) => {


    // Преобразовать дату комментария в формат "День Месяц Год"
    const date = new Date(comment.create_at);
    const formattedDate = `${date.getDate()} ${date.toLocaleString('default', { month: 'long' })} ${date.getFullYear()}`;

    return (
        <div className="comment-container">
            <p>Пользователь: {comment.user}</p>
            <p>Комментарий: {comment.text}</p>
            <p>Дата публикации: {formattedDate}</p>
            <hr></hr>
        </div>

    );
};



const CommentForm = ({ advertisementId }) => {
    const [text, setText] = useState('');
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const token = localStorage.getItem('access_token'); // Получить токен из localStorage или другого места, где он хранится после авторизации
            if (!token) throw new Error('Пользователь не авторизован');

            const response = await axios.post('http://127.0.0.1:8000/api/v1/comments/', {
                user:2,
                advertisement: advertisementId,
                text
            }, {
                headers: {
                    'Authorization': `Token ${token}`
                }
            });

            if (response.status === 201) {
                setText('');
                setError('');
                // Обновить список комментариев в родительском компоненте, если необходимо
            } else {
                throw new Error('Ошибка при отправке комментария');
            }
        } catch (error) {
            setError(error.message);
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <div>
                <textarea
                    value={text}
                    onChange={(e) => setText(e.target.value)}
                    placeholder="Введите комментарий..."
                />
            </div>
            {error && <p>{error}</p>}
            <button type="submit">Отправить</button>
        </form>
    );
};