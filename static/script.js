// static/script.js

async function sendMessage() {
    const inputField = document.getElementById("user-input");
    const messageText = inputField.value.trim();
    
    if (messageText === "") return;

    // 1. 내 메시지 화면에 추가
    addMessage(messageText, "user");
    inputField.value = ""; // 입력창 비우기

    // 2. 로딩 표시 (선택사항)
    // const loadingId = addMessage("생각 중...", "ai");

    try {
        // 3. 서버로 전송 (Fetch API)
        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                query: messageText,
                user_id: "user_123",
                thread_id: "thread_1"
            })
        });

        const data = await response.json();

        // 4. AI 응답 화면에 추가
        addMessage(data.response, "ai");

    } catch (error) {
        console.error("Error:", error);
        addMessage("서버 오류가 발생했습니다.", "ai");
    }
}

// 화면에 말풍선 추가하는 함수
function addMessage(text, sender) {
    const chatBox = document.getElementById("chat-box");
    
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message");
    messageDiv.classList.add(sender === "user" ? "user-message" : "ai-message");

    const bubbleDiv = document.createElement("div");
    bubbleDiv.classList.add("bubble");
    bubbleDiv.innerText = text;

    messageDiv.appendChild(bubbleDiv);
    chatBox.appendChild(messageDiv);

    // 스크롤 맨 아래로 이동
    chatBox.scrollTop = chatBox.scrollHeight;
}

// 엔터키 입력 시 전송
function handleKeyPress(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
}