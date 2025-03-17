const { useState, useEffect } = React;
const axios = window.axios;

const getCookie = (name) => {
    const match = document.cookie.match(new RegExp("(^| )" + name + "=([^;]+)"));
    return match ? match[2] : null;
};

const ChatBotDetail = () => {
    const [chatbot, setChatbot] = useState(null);
    const [error, setError] = useState(null);

    // Lấy ID từ URL
    const chatbotId = window.location.pathname.split("/")[2]; 
    const token = getCookie("access_token");

    useEffect(() => {
        if (!token) {
            alert("Bạn chưa đăng nhập! Hãy đăng nhập trước.");
            window.location.href = "/login-page/";
            return;
        }

        axios.get(`/api/chatbots/${chatbotId}/`, {
            headers: { Authorization: `Bearer ${token}` },
            withCredentials: true
        })
        .then(response => {
            setChatbot(response.data);
        })
        .catch(error => {
            console.error("Lỗi khi tải chi tiết ChatBot:", error);
            setError(error);
        });
    }, [chatbotId, token]);

    if (error) return <p style={{ color: "red" }}>Không thể tải chi tiết ChatBot.</p>;
    if (!chatbot) return <p>Đang tải...</p>;

    return (
        <div>
            <h2>{chatbot.name}</h2>
            <p>Giá: {chatbot.price} VND</p>
            <p>Mô tả: {chatbot.description}</p>
            <button onClick={() => alert(`Bạn đã chọn ${chatbot.name}`)}>Chọn</button>
        </div>
    );
};

// Render component vào id "root"
const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<ChatBotDetail />);
