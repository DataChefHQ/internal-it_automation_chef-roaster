function submitForm() {
    // Show loading spinner and message
    document.getElementById("loading").style.display = 'block';
    document.getElementById("spinner").style.display = 'block';
    document.getElementById("image").style.display = 'none';

    // Get the prompt text
    var prompt = document.getElementById("prompt").value;
    fetch('/find', {
        method: 'POST',
        body: JSON.stringify({ prompt: prompt }),
        headers: { 'Content-Type': 'application/json' }
    }).then(
        response => response.json()
    ).then(data => {
        document.getElementById("loading").style.display = 'none';
        document.getElementById("spinner").style.display = 'none';
        document.getElementById("image").src = data.url;
        document.getElementById("image").style.display = 'block';
        document.getElementById("prompt").value = data.reason;
    });
}

function changeText(button) {
    button.textContent = "Let's roast some chef 😈";
}

function resetText(button) {
    button.textContent = "Show me the victim 👿";
}

function createSnowflake() {
    const snowflake = document.createElement('div');
    snowflake.classList.add('snowflake');
    snowflake.textContent = '❄';
    snowflake.style.left = Math.random() * window.innerWidth + 'px';
    snowflake.style.animationDuration = (Math.random() * 5 + 3) + 's';
    snowflake.style.animationDelay = Math.random() * 5 + 's';
    document.body.appendChild(snowflake);

    setTimeout(() => {
        snowflake.remove();
    }, 8000);
}
setInterval(createSnowflake, 100);