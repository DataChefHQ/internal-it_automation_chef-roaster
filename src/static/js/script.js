
// var typewriter;
document.addEventListener('DOMContentLoaded', () => {
    const resp = document.getElementById("response");
    typewriter = new Typewriter(resp, {
        loop: false,
        delay: 30,
        cursor: '|',
    });
    typewriter
      .typeString("Let's get started! Describe your Chef and I'll roast them for you.")
      .start();
});



function submitForm() {
    // Show loading spinner and message
    document.getElementById("roast-button").style.display = 'none';
    document.getElementById("roast-button-loading").textContent = 'Roasting... 🔥';
    document.getElementById("roast-button-loading").style.display = 'block';
    document.getElementById("image-chef").style.display = 'none';
    document.getElementById("image-roast").style.display = 'none';
    document.getElementById("bg-image").style.display = 'block';
    document.getElementById("response").innerText = "";

    // Get the prompt text
    var prompt = document.getElementById("prompt").value;
    fetch('/find', {
        method: 'POST',
        body: JSON.stringify({ message: prompt }),
        headers: { 'Content-Type': 'application/json' }
    }).then(
        response => response.json()
    ).then(data => {
        // Show the Chef image
        document.getElementById("image-chef").src = data.url;
        document.getElementById("image-chef").style.display = 'block';
        document.getElementById("bg-image").style.display = 'none';

        //Start typing the response
        var resp = document.getElementById("response");
        var typewriter = new Typewriter(resp, {
            loop: false,
            delay: 30,
            cursor: '|',
        });
        typewriter
          .typeString(data.reason)
          .start();

        // Get the image describing the roast
        document.getElementById("roast-button-loading").textContent = 'Generating image... 🔥';
        fetch('/image', {
            method: 'POST',
            body: JSON.stringify({ roast: data.reason }),
            headers: { 'Content-Type': 'application/json' }
        }).then(
            response => response.json()
        ).then(data => {
            // Change the roasting button back for the next roast
            document.getElementById("roast-button").style.display = 'block';
            document.getElementById("roast-button-loading").style.display = 'none';
            document.getElementById("image-roast").src = data.roast_image_url;
            document.getElementById("image-roast").style.display = 'block';
        });

    });
}

function changeText(button) {
    button.textContent = "Roast 😈";
}

function resetText(button) {
    button.textContent = "Roast 👿";
}

function createSnowflake() {
    const snowflake = document.createElement('div');
    snowflake.classList.add('snowflake');
    snowflake.textContent = '❄';
    snowflake.style.left = Math.random() * window.innerWidth + 'px';
    snowflake.style.animationDuration = '20s';
    document.body.appendChild(snowflake);

    setTimeout(() => {
        snowflake.remove();
    }, 20000);
}
setInterval(createSnowflake, 600);