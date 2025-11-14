function handleCredentialResponse(response) {
    console.log("Credential Google:", response.credential);

    fetch("/auth/callback/google", {   // aca se deberia llamar a un endpoint del backend pero hago front por ahora
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ credential: response.credential })
    })
    .then(res => res.json())
    .then(data => {
        console.log("Respuesta del servidor:", data);

        if (data.status === "ok") {
            window.location.href = data.redirect;
        } else {
            alert("Error al iniciar sesión con Google.");
        }
    });
}

window.onload = function () {
    google.accounts.id.initialize({
        client_id: "826779228169-rpf8cnbbu9vue0gtfd2phi78tvn6sj0s.apps.googleusercontent.com",
        callback: handleCredentialResponse
    });

    google.accounts.id.renderButton(
        document.getElementById("googleLoginDiv"),
        { theme: "outline", size: "large" }
    );
};