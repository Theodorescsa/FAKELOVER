const { useState } = React;
const { createRoot } = ReactDOM;
const axios = window.axios; // Đảm bảo axios được tải trong base.html

const Login = () => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    const handleLogin = async (event) => {
        event.preventDefault();
        setError("");

        try {
            const response = await axios.post("/api/login/", {
                username: username,
                password: password,
            });
            alert("Đăng nhập thành công!");
            window.location.href = "/"; 
        } catch (error) {
            setError("Đăng nhập thất bại! Vui lòng kiểm tra lại thông tin.");
            console.error("Login error:", error.response?.data || error.message);
        }
    };

    return (
        <div>
            <h2>Đăng nhập</h2>
            {error && <p style={{ color: "red" }}>{error}</p>}
            <form onSubmit={handleLogin}>
                <input type="text" placeholder="Username" value={username} onChange={(e) => setUsername(e.target.value)} />
                <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} />
                <button type="submit">Đăng nhập</button>
            </form>
        </div>
    );
};

// React 18: Sử dụng createRoot
const root = createRoot(document.getElementById("root"));
root.render(<Login />);
