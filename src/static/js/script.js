function submitForm() {
    // Show loading spinner and message
    document.getElementById("loading").style.display = 'block';
    document.getElementById("spinner").style.display = 'block';

    // Get the prompt text
    var prompt = document.getElementById("prompt").value;
    fetch('/submit', {
        method: 'POST',
        body: JSON.stringify({ prompt: prompt }),
        headers: { 'Content-Type': 'application/json' }
    }).then(response => response.json())
    .then(data => {
        if (data.status === "loading") {
            setTimeout(() => {
                document.getElementById("loading").style.display = 'none';
                document.getElementById("spinner").style.display = 'none';
                document.getElementById("image").src = "https://s3.amazonaws.com/your-bucket-name/generated_image.jpg";
                document.getElementById("image").style.display = 'block';
            }, 5000);
        }
    });
}

function changeText(button) {
    button.textContent = "Let's roast 😈";
}

function resetText(button) {
    button.textContent = "Show me the victim 👿";
}