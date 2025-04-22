$(document).ready(function () {
    $.ajax({
        url: "/api/chatbots/",
        type: "GET",
        headers: {
            "Authorization": "Bearer " + accessToken
        },
        success: function (data) {
            const chatbotList = $("#chatbot-list");
            chatbotList.empty(); 

            if (data.length === 0) {
                chatbotList.append("<li>Không có chatbot nào.</li>");
            } else {
                data.forEach(function (chatbot) {
                    chatbotList.append(`
                        <li>
                            <strong>${chatbot.name}</strong> - ${chatbot.description || "Không có mô tả"}
                        </li>
                    `);
                });
            }
        },
        error: function (xhr, status, error) {
            $("#error-message").text("Lỗi khi tải danh sách chatbots: " + error);
        }
    });
});
