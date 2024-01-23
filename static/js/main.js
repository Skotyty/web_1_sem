function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function sendLikeRequest(itemId, itemType, likeValue) {
    const formData = new FormData();
    formData.append(itemType + '_id', itemId);
    formData.append('like_value', likeValue);

    fetch('/like/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
        },
    })
        .then(response => response.json())
        .then(data => {
            const counter = document.querySelector(`#like-counter-${itemType}-${itemId}`);
            if (counter) {
                counter.textContent = data.count;
            }
        });
}

document.querySelectorAll('.like-button, .dislike-button').forEach(button => {
    button.addEventListener('click', () => {
        const {id: itemId, type: itemType} = button.dataset;
        const likeValue = button.classList.contains('like-button') ? 1 : -1;
        sendLikeRequest(itemId, itemType, likeValue);
    });
});

function handleCorrectAnswer(button, cancel = false) {
    const questionId = button.getAttribute('data-question-id');
    const answerId = cancel ? null : button.getAttribute('data-answer-id');
    const body = JSON.stringify(cancel ? {
        'question_id': questionId,
        'cancel_correct': true
    } : {'question_id': questionId, 'answer_id': answerId});

    fetch('/mark-correct/', {
        method: 'POST',
        body: body,
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        },
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.querySelectorAll('.card .form-check.form-switch').forEach(container => {
                    container.style.display = 'none';
                });
                document.querySelectorAll('.mark-correct-btn').forEach(btn => {
                    btn.style.display = 'block';
                });
                document.querySelectorAll('.cancel-correct-btn').forEach(btn => {
                    btn.style.display = 'none';
                });

                const selectedAnswerContainer = document.querySelector(`#answer-${data.correct_answer_id} .card-text`);
                let correctCheckboxContainer = selectedAnswerContainer.nextElementSibling;

                if (!correctCheckboxContainer || !correctCheckboxContainer.classList.contains('form-check')) {
                    correctCheckboxContainer = document.createElement('div');
                    correctCheckboxContainer.className = 'form-check form-switch';
                    selectedAnswerContainer.after(correctCheckboxContainer);
                }

                correctCheckboxContainer.innerHTML = `
                <input class="form-check-input" type="checkbox" id="correctAnswer${data.correct_answer_id}" checked disabled>
                <label class="form-check-label" for="correctAnswer${data.correct_answer_id}">Правильный ответ!</label>
            `;
                correctCheckboxContainer.style.display = 'block';

                const markButton = document.querySelector(`#answer-${data.correct_answer_id} .mark-correct-btn`);
                const cancelButton = document.querySelector(`#answer-${data.correct_answer_id} .cancel-correct-btn`);
                if (markButton) markButton.style.display = 'none';
                if (cancelButton) cancelButton.style.display = 'block';
            }
        });
}

document.querySelectorAll('.mark-correct-btn').forEach(button => {
    button.addEventListener('click', () => handleCorrectAnswer(button));
});

document.querySelectorAll('.cancel-correct-btn').forEach(button => {
    button.addEventListener('click', () => handleCorrectAnswer(button, true));
});
