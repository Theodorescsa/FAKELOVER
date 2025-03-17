const { useState, useEffect } = React;
const axios = window.axios;

const getCookie = (name) => {
    const match = document.cookie.match(new RegExp("(^| )" + name + "=([^;]+)"));
    return match ? match[2] : null;
};
const token = getCookie("access_token");

const ChatBotList = () => {
    const [chatbots, setChatbots] = useState([]);
    const [selectedChatbot, setSelectedChatbot] = useState(null);
    const [socialAccounts, setSocialAccounts] = useState([]);
    const [selectedAccount, setSelectedAccount] = useState("");
    const [chatApps, setChatApps] = useState([]);
    const [useNewAccount, setUseNewAccount] = useState(false);
    const [selectedChatApp, setSelectedChatApp] = useState("");

    const [botSettings, setBotSettings] = useState({
        response_speed: 1.0,
        personality: "friendly",
        joke_frequency: 3,
        username: "",
        password: "",
        chat_app: ""
    });

    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState("");

    useEffect(() => {
        axios.get("/api/chatbots/", { headers: { Authorization: `Bearer ${token}` }, withCredentials: true })
            .then(response => setChatbots(response.data))
            .catch(() => setError("Không thể tải danh sách ChatBot."));

        axios.get("/api/social-accounts/", { headers: { Authorization: `Bearer ${token}` }, withCredentials: true })
            .then(response => {
                setSocialAccounts(response.data);
                if (response.data.length === 0) setUseNewAccount(true);
            });

        axios.get("/api/chat-apps/", { headers: { Authorization: `Bearer ${token}` }, withCredentials: true })
            .then(response => setChatApps(response.data));
    }, []);

    const fetchChatbotDetails = (id) => {
        setLoading(true);
        axios.get(`/api/chatbots/${id}/`, { headers: { Authorization: `Bearer ${token}` }, withCredentials: true })
            .then(response => setSelectedChatbot(response.data))
            .finally(() => setLoading(false));
    };

    const closeModal = () => {
        setSelectedChatbot(null);
        setMessage("");
    };

    const handleRegister = (e) => {
        e.preventDefault();
        setMessage("");

        let requestData = {
            chatbot: selectedChatbot.id,
            bot_settings: {
                response_speed: botSettings.response_speed,
                personality: botSettings.personality,
                joke_frequency: botSettings.joke_frequency
            }
        };

        if (useNewAccount) {
            requestData.social_account = {
                username: botSettings.username,
                password: botSettings.password,
                chat_app: botSettings.chat_app
            };
        } else {
            requestData.social_account = selectedAccount || null;
        }
        console.log("Dữ liệu gửi đi:", requestData);

        axios.post("/chat/api/chatsessions/", requestData, {
            headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
            withCredentials: true
        })
        .then(() => setMessage("Đăng ký thành công!"))
        .catch(() => setMessage("Đăng ký thất bại, vui lòng thử lại!"));
    };

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setBotSettings(prev => ({ ...prev, [name]: value }));
    };
    const modalStyle = {
        position: "fixed",
        top: 0,
        left: 0,
        width: "100%",
        height: "100%",
        backgroundColor: "rgba(0, 0, 0, 0.5)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center"
    };
    
    const modalContentStyle = {
        backgroundColor: "white",
        padding: "20px",
        borderRadius: "10px",
        width: "50%",
        maxWidth: "600px",
        textAlign: "center"
    };
    return (
        <div>
            <h2>Danh sách ChatBot</h2>
            {error && <p style={{ color: "red" }}>{error}</p>}
            <ul>
                {chatbots.map(bot => (
                    <li key={bot.id}>
                        <span 
                            onClick={() => fetchChatbotDetails(bot.id)}
                            style={{ cursor: "pointer", color: "blue", textDecoration: "underline" }}
                        >
                            {bot.name}
                        </span>
                    </li>
                ))}
            </ul>

            {selectedChatbot && (
                <div style={{
                    position: "fixed", top: 0, left: 0, width: "100%", height: "100%",
                    backgroundColor: "rgba(0, 0, 0, 0.5)", display: "flex",
                    alignItems: "center", justifyContent: "center"
                }}>
                    <div style={{
                        backgroundColor: "white", padding: "20px", borderRadius: "10px",
                        width: "50%", maxWidth: "600px", textAlign: "center"
                    }}>
                        <h3>{selectedChatbot.name}</h3>
                        <p>Giá: {selectedChatbot.price} VND</p>
                        <p>Mô tả: {selectedChatbot.description}</p>

                        <form onSubmit={handleRegister}>
                            <h4>Cài đặt ChatBot</h4>
                            <label>Tốc độ phản hồi:
                                <input type="number" name="response_speed" step="0.1" min="0.5" max="3"
                                    value={botSettings.response_speed} onChange={handleInputChange} required />
                            </label>
                            <label>Tính cách:
                                <select name="personality" value={botSettings.personality} onChange={handleInputChange}>
                                    <option value="friendly">Thân thiện</option>
                                    <option value="romantic">Lãng mạn</option>
                                    <option value="serious">Nghiêm túc</option>
                                </select>
                            </label>
                            <label>Tần suất kể chuyện cười:
                                <input type="number" name="joke_frequency" min="0" max="10"
                                    value={botSettings.joke_frequency} onChange={handleInputChange} required />
                            </label>

                            <hr />

                            {socialAccounts.length > 0 && (
                                <>
                                    <label>
                                        <input type="radio" name="account_option" checked={!useNewAccount} onChange={() => setUseNewAccount(false)} />
                                        Chọn tài khoản có sẵn:
                                    </label>
                                    <select value={selectedAccount} onChange={(e) => setSelectedAccount(e.target.value)}>
                                        <option value="">-- Không chọn --</option>
                                        {socialAccounts.map(acc => (
                                            <option key={acc.id} value={acc.id}>{acc.username}</option>
                                        ))}
                                    </select>
                                </>
                            )}

                            <label>
                                <input type="radio" name="account_option" checked={useNewAccount} onChange={() => setUseNewAccount(true)} />
                                Nhập tài khoản mới:
                            </label>

                            {useNewAccount && (
                                <>
                                    <label>Username: <input type="text" name="username" value={botSettings.username} onChange={handleInputChange} required /></label>
                                    <label>Password: <input type="password" name="password" value={botSettings.password} onChange={handleInputChange} required /></label>
                                    <label>Chat App:
                                        <select name="chat_app" value={botSettings.chat_app} onChange={handleInputChange} required>
                                            <option value="">-- Chọn ChatApp --</option>
                                            {chatApps.map(app => (
                                                <option key={app.id} value={app.id}>{app.name}</option>
                                            ))}
                                        </select>
                                    </label>
                                </>
                            )}

                            <button type="submit">Đăng ký</button>
                            <button type="button" onClick={closeModal}>Đóng</button>
                        </form>

                        {message && <p style={{ color: message.includes("thành công") ? "green" : "red" }}>{message}</p>}
                    </div>
                </div>
            )}

            {loading && <p>Đang tải...</p>}
        </div>
    );
};

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<ChatBotList />);
